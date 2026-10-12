#!/usr/bin/env python3
"""P0 constrained execution-transport *preflight*; no agent execution or activation.

Offline, read-only probes run only as the commissioned unprivileged Foundry-Agent.
Output contains no secrets. Do not run as root.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ALLOWED_UID = 1000
WORK = Path("/home/foundry-agent/work")
CONTRACT = WORK / "AGENTS.md"
PROTECTED = (Path("/opt/foundry-evaluator/current"),
             Path("/etc/foundry-evaluator"),
             Path("/etc/foundry-telegram"))


def inspect(uid, work, contract, which, check, expected_owner_uid=ALLOWED_UID):
    if uid != ALLOWED_UID:
        raise RuntimeError("wrong actor uid")
    if not work.is_dir() or not contract.is_file():
        raise RuntimeError("commissioned workspace contract missing")
    if not (work.stat().st_uid == expected_owner_uid and
            contract.stat().st_uid in (0, expected_owner_uid)):
        raise RuntimeError("workspace or contract ownership drift")
    codex = which("codex")
    if not codex:
        raise RuntimeError("Codex CLI not installed in actor PATH")
    # Avoid executing Codex or inspecting credentials on initial preflight.
    return {
        "actor_uid": uid,
        "workspace": str(work),
        "contract_present": True,
        "codex_available": True,
        "production_targets": "NOT_TOUCHED",
        "provider_call": "NOT_ATTEMPTED",
        "task_execution": "NOT_ACTIVATED",
        "read_only_preflight": "PASS",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", help="write preflight record; default stdout")
    args = p.parse_args()
    try:
        result = inspect(os.geteuid(), WORK, CONTRACT, shutil.which, subprocess.run)
        record = json.dumps(result, sort_keys=True) + "\n"
        if args.output:
            path = Path(args.output)
            if not path.is_relative_to(WORK) or path.is_symlink() or path.exists():
                raise RuntimeError("unsafe result destination")
            fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w") as f:
                f.write(record)
        else:
            sys.stdout.write(record)
        return 0
    except (OSError, RuntimeError, ValueError):
        print("BLOCKED: actor identity, workspace or candidate preflight failed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
