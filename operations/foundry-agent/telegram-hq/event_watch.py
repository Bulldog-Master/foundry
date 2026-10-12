#!/usr/bin/env python3
"""Foundry HQ read-only GitHub state watcher; no actions or approvals."""
import argparse
import json
import os
from pathlib import Path
import sys
import urllib.request
from notify import notify, render

REPO = "Bulldog-Master/foundry"
TARGETS = (("pulls", 28), ("pulls", 30), ("issues", 29))


def get_state(fetch=urllib.request.urlopen):
    state = {}
    for kind, number in TARGETS:
        url = f"https://api.github.com/repos/{REPO}/{kind}/{number}"
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json", "User-Agent": "foundry-hq-notifier/0.1"
        })
        with fetch(req, timeout=15) as resp:
            payload = json.load(resp)
        key = f"{kind}/{number}"
        if kind == "pulls":
            state[key] = {
                "state": payload["state"],
                "draft": payload["draft"],
                "merged": payload["merged"],
                "head_sha": payload["head"]["sha"],
                "updated_at": payload["updated_at"],
            }
        else:
            state[key] = {
                "state": payload["state"],
                "updated_at": payload["updated_at"],
                "comments": payload["comments"],
            }
    return state


def changes(old, new):
    return {key: value for key, value in new.items()
            if key in old and old[key] != value}


def summarize(delta):
    names = {"pulls/28": "Foundry architecture PR #28",
             "pulls/30": "Telegram HQ PR #30",
             "issues/29": "Scanner review Issue #29"}
    return "\n".join(f"{names[k]} changed. Review exact GitHub record."
                     for k in sorted(delta))


def watch(state_path, *, fetch=urllib.request.urlopen, send=notify, token=None, chat_id=None):
    state_path = Path(state_path)
    if state_path.is_symlink() or (state_path.exists() and not state_path.is_file()):
        raise ValueError("unsafe state file")
    current = get_state(fetch=fetch)
    previous = json.loads(state_path.read_text()) if state_path.exists() else {}
    delta = changes(previous, current)
    if delta:
        lines = []
        for key in sorted(delta):
            kind, number = key.split("/")
            link_kind = "pull" if kind == "pulls" else "issues"
            link = f"https://github.com/{REPO}/{link_kind}/{number}"
            lines.append(summarize({key: delta[key]}) + "\n" + link)
        msg = render("INFO", "Foundry workstream update",
                     "\n\n".join(lines), None)
        # One atomic notice per observed snapshot; never advance on failed delivery.
        send(msg, token=token, chat_id=chat_id)
    if current != previous:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = state_path.with_name(state_path.name + ".tmp")
        if temporary.exists() or temporary.is_symlink():
            raise ValueError("unsafe temporary file")
        fd = os.open(str(temporary), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(fd, "w") as stream:
                json.dump(current, stream, sort_keys=True)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, state_path)
        finally:
            if temporary.exists():
                temporary.unlink()
    return len(delta)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--state-file", required=True)
    p.add_argument("--token-file", required=True)
    p.add_argument("--chat-file", required=True)
    args = p.parse_args()
    try:
        token_file, chat_file = Path(args.token_file), Path(args.chat_file)
        for path in (token_file, chat_file):
            if path.is_symlink() or path.stat().st_mode & 0o077:
                raise ValueError("insecure credential file")
        count = watch(args.state_file, token=token_file.read_text().strip(),
                      chat_id=chat_file.read_text().strip())
        print(f"Checked {len(TARGETS)} GitHub records; delivered {count} update(s)")
        return 0
    except Exception:
        # Fail closed; no token, chat ID or network response printed
        print("BLOCKED: GitHub watch or Telegram delivery failed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
