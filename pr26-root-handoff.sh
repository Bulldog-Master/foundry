#!/usr/bin/env bash
set -euo pipefail
umask 077
[[ $EUID -eq 0 ]] || exit 2
src=$(cd -- "$(dirname -- "$0")" && pwd -P)
cd "$src"
sha256sum --check --strict MANIFEST.sha256
case "${1:-}" in
install-publish)
  bash "$src/install-runtime.sh"
  /opt/foundry-evaluator/current/venv/bin/python - <<'CHECK'
import sys
sys.path.insert(0,'/opt/foundry-evaluator/current/bin')
from runtime_contract import read_root,parse,canon,sha
from pathlib import Path
run=Path('/var/lib/foundry-evaluator/runs/f1efc313cd27a05e84b85c48438137aae2ea8bcb32f4b7b10a928a3aeffebf8b/attempt-2')
expected=parse(read_root(Path.cwd()/'evidence/pr26-authoritative-result.json'))
actual=parse(read_root(run/'result.json'))
if actual!=expected: raise SystemExit('retained authoritative result mismatch')
if actual['head_sha']!='f949d06fa43581b8851b789e28d108b7da9950b5' or actual['overall']!='FAIL' or actual['routing']!='HARD_STOP': raise SystemExit('retained failure binding')
CHECK
  /opt/foundry-evaluator/current/venv/bin/python /opt/foundry-evaluator/current/bin/foundry-evaluator-publish --retained-release /opt/foundry-evaluator/releases/258fdf6813af1353efebd134e2a3ba46cbfbe4e24776ae1307e300ab460e224a /var/lib/foundry-evaluator/packets/f1efc313cd27a05e84b85c48438137aae2ea8bcb32f4b7b10a928a3aeffebf8b /var/lib/foundry-evaluator/runs/f1efc313cd27a05e84b85c48438137aae2ea8bcb32f4b7b10a928a3aeffebf8b/attempt-2
  /opt/foundry-evaluator/current/venv/bin/python - <<'CHECK'
import sys,pathlib
sys.path.insert(0,'/opt/foundry-evaluator/current/bin')
from runtime_contract import read_root,parse,put
journal=parse(read_root('/var/lib/foundry-evaluator/runs/f1efc313cd27a05e84b85c48438137aae2ea8bcb32f4b7b10a928a3aeffebf8b/attempt-2/publication/completed.json'))
if any(journal[k]!=v for k,v in {'head_sha':'f949d06fa43581b8851b789e28d108b7da9950b5','packet_sha256':'f1efc313cd27a05e84b85c48438137aae2ea8bcb32f4b7b10a928a3aeffebf8b','conclusion':'failure','review_event':'REQUEST_CHANGES'}.items()):raise SystemExit('publication completion mismatch')
name='foundry-pr26-bd78909848c07e7f9cfea04f761fd9981640874e.bundle'
source=read_root(pathlib.Path.cwd()/'pr26-remediation.bundle')
target=pathlib.Path('/tmp')/name
if target.exists():
    if read_root(target)!=source:raise SystemExit('bundle collision')
else:
    put('/tmp',name,source);target.chmod(0o444)
CHECK
  ;;
seal)
  exec /opt/foundry-evaluator/current/venv/bin/python /opt/foundry-evaluator/current/bin/foundry-evaluator-run 26 --seal-only 4c2c611b61a1947bef409e5357f5426703bca452 bd78909848c07e7f9cfea04f761fd9981640874e
  ;;
*) exit 2;;
esac
