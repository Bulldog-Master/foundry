#!/usr/bin/env bash
set -euo pipefail
umask 077

if [[ ${EUID} -ne 0 ]]; then
  echo "must run as root" >&2
  exit 2
fi

src=$(cd -- "$(dirname -- "$0")" && pwd -P)
cd "$src"
sha256sum --check --strict MANIFEST.sha256

release_hash=$(sha256sum MANIFEST.sha256 | awk '{print $1}')
release="/opt/foundry-evaluator/releases/$release_hash"
if [[ -e "$release" ]]; then
  echo "release already installed: $release_hash"
else
  install -d -o root -g root -m 0555 "$release" "$release/bin" "$release/schemas"
  install -o root -g root -m 0555 foundry-packet-builder foundry-evaluator-invoke foundry-evaluator-publish foundry-evaluator-run foundry-evaluator-poll "$release/bin/"
  install -o root -g root -m 0444 bootstrap0b-profile.json "$release/profile.json"
  install -o root -g root -m 0444 evaluator-task.md provider-terms.json RUNTIME-POLICY.md MANIFEST.sha256 "$release/"
  install -o root -g root -m 0444 schemas/*.json "$release/schemas/"
fi

install -d -o root -g root -m 0700 /etc/foundry-evaluator
install -o root -g root -m 0600 config.json /etc/foundry-evaluator/config.json
install -o root -g root -m 0400 evaluator-task.md /etc/foundry-evaluator/evaluator-task.md
install -o root -g root -m 0400 provider-terms.json /etc/foundry-evaluator/provider-terms.json
ln -sfn "$release" /opt/foundry-evaluator/current
install -o root -g root -m 0644 foundry-evaluator.service /etc/systemd/system/foundry-evaluator.service
install -o root -g root -m 0644 foundry-evaluator.timer /etc/systemd/system/foundry-evaluator.timer
systemctl daemon-reload

echo "installed_release=$release_hash"
echo "timer_enabled=$(systemctl is-enabled foundry-evaluator.timer 2>/dev/null || true)"
