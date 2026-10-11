#!/usr/bin/env bash
set -euo pipefail
umask 077
[[ $EUID -eq 0 ]] || { echo 'must run as root' >&2; exit 2; }
install -d -o root -g root -m 0700 /var/lib/foundry-evaluator/install-evidence
install_log=$(mktemp /var/lib/foundry-evaluator/install-evidence/install-XXXXXXXX.log)
exec > >(tee -a "$install_log") 2>&1
src=$(cd -- "$(dirname -- "$0")" && pwd -P)
cd "$src"
# Installation is commissioning-only. An active timer or service is a hard stop.
if systemctl is-active --quiet foundry-evaluator.timer || systemctl is-enabled --quiet foundry-evaluator.timer || systemctl is-active --quiet foundry-evaluator.service; then
  echo 'refusing installation over enabled or running evaluator; no activation authority' >&2
  exit 2
fi
sha256sum --check --strict MANIFEST.sha256
python3 - <<'CHECK'
import pathlib
rows=pathlib.Path('MANIFEST.sha256').read_text().splitlines()
names=[row.split('  ',1)[1] for row in rows]
actual={str(p) for p in pathlib.Path('.').rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and str(p)!='MANIFEST.sha256'}
if len(names)!=len(set(names)) or set(names)!=actual: raise SystemExit('release file set differs from manifest')
if any(p.is_symlink() for p in pathlib.Path('.').rglob('*') if '.git' not in p.parts): raise SystemExit('release symlink')
CHECK
[[ $(git --version) == 'git version 2.53.0' ]] || { echo 'requires Git 2.53.0' >&2; exit 2; }
release_hash=$(sha256sum MANIFEST.sha256 | cut -d' ' -f1)
release="/opt/foundry-evaluator/releases/$release_hash"
install -d -o root -g root -m 0700 /opt/foundry-evaluator /opt/foundry-evaluator/releases /etc/foundry-evaluator /var/lib/foundry-evaluator
exec 9>/opt/foundry-evaluator/install.lock
flock -n 9
if [[ -e "$release" ]]; then
  [[ -f "$release/INSTALL-COMPLETE" ]] || { echo 'incomplete release retained; refuses reuse' >&2; exit 2; }
  (cd "$release/source" && sha256sum --check --strict MANIFEST.sha256)
else
  install -d -o root -g root -m 0700 "$release" "$release/bin" "$release/schemas" "$release/source"
  while IFS= read -r row; do
    name=${row#*  }
    install -d -o root -g root -m 0500 "$release/source/$(dirname -- "$name")"
    install -o root -g root -m 0400 -- "$name" "$release/source/$name"
  done < MANIFEST.sha256
  install -o root -g root -m 0400 MANIFEST.sha256 "$release/source/"
  if ! python3 -c 'import ensurepip' >/dev/null 2>&1; then
    apt-get update
    apt-get install -y python3-venv
  fi
  python3 -m venv "$release/venv"
  "$release/venv/bin/python" -m pip --isolated install --disable-pip-version-check -r requirements-runtime.txt
  "$release/venv/bin/python" verify-conformance-v0.1.py
  "$release/venv/bin/python" -m unittest -v test_runtime.py
  install -o root -g root -m 0500 foundry-packet-builder foundry-evaluator-invoke foundry-evaluator-publish foundry-evaluator-run foundry-evaluator-poll "$release/bin/"
  install -o root -g root -m 0400 runtime_contract.py runtime_invoke.py provider_envelope.py "$release/bin/"
  install -o root -g root -m 0400 bootstrap0b-profile.json "$release/profile.json"
  install -o root -g root -m 0400 evaluator-task.md provider-terms.json config.json MANIFEST.sha256 "$release/"
  install -o root -g root -m 0400 schemas/*.json "$release/schemas/"
  "$release/venv/bin/python" - "$release" <<'IMAGE'
import hashlib,json,os,pathlib,sys
release=pathlib.Path(sys.argv[1]); image={}
for path in (release/'venv').rglob('*'):
    if '__pycache__' in path.parts or path.suffix=='.pyc': continue
    if not path.is_file() and not path.is_symlink(): continue
    row={}
    if path.is_symlink(): row['symlink']=os.readlink(path)
    if path.is_file(): row['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    image[str(path.relative_to(release))]=row
(release/'RUNTIME.json').write_text(json.dumps(image,sort_keys=True,separators=(',',':')))
IMAGE
  touch "$release/INSTALL-COMPLETE"
  chmod -R a-w "$release"
fi
# Existing provider and GitHub App files are neither read nor replaced by installation.
install -o root -g root -m 0644 foundry-evaluator.service /etc/systemd/system/foundry-evaluator.service
install -o root -g root -m 0644 foundry-evaluator.timer /etc/systemd/system/foundry-evaluator.timer
ln -s "$release" "/opt/foundry-evaluator/current-$release_hash"
mv -Tf "/opt/foundry-evaluator/current-$release_hash" /opt/foundry-evaluator/current
systemctl daemon-reload
printf 'installed_release=%s\n' "$release_hash"
printf 'timer_enabled=false\n'
