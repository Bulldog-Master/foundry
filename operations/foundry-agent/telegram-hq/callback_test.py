#!/usr/bin/env python3
"""Simulation-only Telegram button acknowledgment. NEVER a Foundry approval service."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def check_callback(cb, pending):
    if not isinstance(cb, dict) or not isinstance(pending, dict):
        return None
    message = cb.get("message") or {}
    chat = message.get("chat") or {}
    if str(chat.get("id")) != str(pending.get("chat_id")):
        return None
    if message.get("message_id") != pending.get("message_id"):
        return None
    data = cb.get("data", "")
    if data == "test_yes:" + str(pending.get("test_id")):
        return "APPROVE_TEST"
    if data == "test_no:" + str(pending.get("test_id")):
        return "REJECT_TEST"
    return None


def process(updates, pending, acknowledged, answer):
    """Return new high-water mark and single test result; duplicate taps have no effect."""
    high = int(acknowledged.get("offset", 0))
    prior = acknowledged.get("decision")
    for u in sorted(updates, key=lambda x: x.get("update_id", -1)):
        uid = u.get("update_id")
        if not isinstance(uid, int) or uid < high:
            continue
        cb = u.get("callback_query") or {}
        action = check_callback(cb, pending)
        if action and not prior:
            # Do not confirm or advance cursor until Telegram acknowledged callback.
            answer(cb["id"], "Test selection received. No Foundry authority granted.")
            prior = action
        elif action:
            answer(cb["id"], "Already recorded. This was a simulation only.")
        high = uid + 1
    return {"offset": high, "decision": prior}


def api(token, method, args, opener=urlopen):
    # Never print URL: it includes token.
    url = f"https://api.telegram.org/bot{token}/{method}"
    req = Request(url, data=urlencode(args).encode(), method="POST")
    with opener(req, timeout=20) as response:
        doc = json.load(response)
    if doc.get("ok") is not True:
        raise ValueError("Telegram rejected request")
    return doc["result"]


def secured(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o077:
        raise ValueError("unsafe local file")
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token-file", required=True)
    parser.add_argument("--pending-file", required=True)
    parser.add_argument("--result-file", required=True)
    args = parser.parse_args()
    try:
        token = secured(args.token_file).read_text().strip()
        pending = json.loads(secured(args.pending_file).read_text())
        result_path = Path(args.result_file)
        if result_path.is_symlink() or (result_path.exists() and result_path.stat().st_mode & 0o077):
            raise ValueError("unsafe result path")
        previous = json.loads(result_path.read_text()) if result_path.exists() else {"offset": 0, "decision": None}
        incoming = api(token, "getUpdates", {
            "offset": previous["offset"], "timeout": 0,
            "allowed_updates": json.dumps(["callback_query"])})
        updated = process(incoming, pending, previous,
                          lambda ident, message: api(token, "answerCallbackQuery",
                                                     {"callback_query_id": ident, "text": message}))
        if updated != previous:
            tmp = result_path.with_name(result_path.name + ".tmp")
            if tmp.exists() or tmp.is_symlink():
                raise ValueError("unsafe temp file")
            fd = os.open(str(tmp), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd, "w") as f:
                json.dump(updated, f, sort_keys=True)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, result_path)
        print("Test callback check completed. No real approval recorded.")
        return 0
    except Exception:
        print("BLOCKED: test callback handler failed; no real approval recorded", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
