#!/usr/bin/env bash
set -euo pipefail
umask 077
[[ $EUID -eq 0 ]] || { echo 'must run as root' >&2; exit 2; }
src=$(cd -- "$(dirname -- "$0")" && pwd -P)
bash "$src/install-runtime.sh"
exec /opt/foundry-evaluator/current/venv/bin/python /opt/foundry-evaluator/current/bin/foundry-evaluator-run 26 --seal-only 4c2c611b61a1947bef409e5357f5426703bca452 f949d06fa43581b8851b789e28d108b7da9950b5
