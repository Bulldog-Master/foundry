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


def write_record(path, record, work=WORK):
    """Create a new record below work without following directory symlinks."""
    path = Path(path)
    if not path.is_absolute() or ".." in path.parts:
        raise RuntimeError("unsafe result destination")
    try:
        relative = path.relative_to(work)
    except ValueError:
        raise RuntimeError("unsafe result destination") from None
    if not relative.parts:
        raise RuntimeError("unsafe result destination")
    directory = os.open(work, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in relative.parts[:-1]:
            next_directory = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                     dir_fd=directory)
            os.close(directory)
            directory = next_directory
        fd = os.open(relative.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     0o600, dir_fd=directory)
        with os.fdopen(fd, "w") as f:
            f.write(record)
    finally:
        os.close(directory)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", help="write preflight record; default stdout")
    args = p.parse_args()
    try:
        result = inspect(os.geteuid(), WORK, CONTRACT, shutil.which, subprocess.run)
        record = json.dumps(result, sort_keys=True) + "\n"
        if args.output:
            write_record(args.output, record)
        else:
            sys.stdout.write(record)
        return 0
    except (OSError, RuntimeError, ValueError):
        print("BLOCKED: actor identity, workspace or candidate preflight failed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
