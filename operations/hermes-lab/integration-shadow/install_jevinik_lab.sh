#!/usr/bin/env bash
# Pinned, non-root staging only; NO provider call, daemon or production deployment.
set -euo pipefail
umask 077
root=/srv/hermes-lab/foundry-agent
rev=${JEVINIK_COMMIT:-}
[[ "$EUID" -ne 0 ]] || { echo "REFUSED: root" >&2; exit 2; }
[[ "${USER:-}" == foundry-agent ]] || { echo "REFUSED: foundry-agent only" >&2; exit 2; }
[[ "$rev" =~ ^[a-fA-F0-9]{40}$ ]] || { echo "REFUSED: reviewed 40-character JEVINIK_COMMIT required" >&2; exit 2; }
[[ -d "$root" && ! -L "$root" && ! -e "$root/jevinik-candidate" ]] || { echo "REFUSED: expected unused lab target unavailable" >&2; exit 2; }
for cmd in git node npm; do command -v "$cmd" >/dev/null || { echo "REFUSED: missing $cmd" >&2; exit 2; }; done
node -e 'let [a,b]=process.versions.node.split(".").map(Number); if(a<20||(a===20&&b<9))process.exit(1)' || { echo "REFUSED: Node >=20.9 required" >&2; exit 2; }
mkdir -m 700 "$root/jevinik-candidate"
git -C "$root/jevinik-candidate" init -q
git -C "$root/jevinik-candidate" remote add origin https://github.com/unicodeveloper/jevocks.git
git -C "$root/jevinik-candidate" fetch --no-tags --depth=1 origin "$rev"
actual=$(git -C "$root/jevinik-candidate" rev-parse FETCH_HEAD)
[[ "$actual" == "$rev" ]] || { echo "REFUSED: source SHA mismatch" >&2; exit 2; }
git -C "$root/jevinik-candidate" checkout -q --detach "$actual"
[[ -f "$root/jevinik-candidate/package-lock.json" ]] || { echo "REFUSED: npm lockfile missing" >&2; exit 2; }
(cd "$root/jevinik-candidate" && npm ci --ignore-scripts --no-audit --no-fund)
printf 'STAGED_JEVINIK_COMMIT=%s\nNO_APP_STARTED=1\nNO_PROVIDER_CALLS=1\n' "$actual"
