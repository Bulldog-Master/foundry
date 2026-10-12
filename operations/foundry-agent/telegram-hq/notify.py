#!/usr/bin/env python3
"""Foundry HQ: outbound notification-only Telegram transport.

Candidate only. No polling, webhook, command processing, authorization, or signing.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urlsplit

MAX_MESSAGE = 3500
GITHUB_REPO = "Bulldog-Master/foundry"


def validate_link(link):
    if not link:
        return None
    try:
        u = urlsplit(link)
    except ValueError as exc:
        raise ValueError("invalid review link") from exc
    if (u.scheme != "https" or u.netloc != "github.com"
            or u.username or u.password or u.port
            or u.query or u.fragment
            or not re.fullmatch(
                r"/Bulldog-Master/foundry/(issues|pull)/[1-9][0-9]*", u.path)):
        raise ValueError("link must be a Foundry GitHub issue or PR URL")
    return link


def render(kind, title, summary, link):
    if kind not in {"INFO", "ACTION_REQUIRED", "BLOCKED", "COMPLETE"}:
        raise ValueError("unsupported notification category")
    if not title.strip() or not summary.strip():
        raise ValueError("title and summary required")
    link = validate_link(link)
    message = f"Foundry HQ | {kind}\n{title.strip()}\n\n{summary.strip()}"
    if link:
        message += f"\n\nReview: {link}"
    if len(message) > MAX_MESSAGE:
        raise ValueError("notification too long")
    return message


def notify(message, *, token, chat_id, opener=urllib.request.urlopen):
    if not token or not chat_id:
        raise ValueError("Telegram credentials not configured")
    if not re.fullmatch(r"[0-9]+:[A-Za-z0-9_-]+", token):
        raise ValueError("invalid bot token syntax")
    if not re.fullmatch(r"-?[0-9]+", chat_id):
        raise ValueError("invalid chat id syntax")
    body = json.dumps({"chat_id": chat_id, "text": message,
                       "disable_web_page_preview": True}).encode()
    request = urllib.request.Request(
        "https://api.telegram.org/bot" + token + "/sendMessage",
        data=body, method="POST",
        headers={"Content-Type": "application/json"})
    response = opener(request, timeout=15)
    with response:
        data = json.loads(response.read(8192))
    if data.get("ok") is not True:
        raise ValueError("Telegram delivery not confirmed")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Foundry HQ outbound Telegram notice")
    parser.add_argument("--kind", required=True, choices=["INFO", "ACTION_REQUIRED", "BLOCKED", "COMPLETE"])
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--link")
    parser.add_argument("--send", action="store_true", help="requires independently approved secret provisioning")
    args = parser.parse_args(argv)
    try:
        message = render(args.kind, args.title, args.summary, args.link)
        if not args.send:
            print(message)
            return 0
        notify(message, token=os.environ.get("FOUNDRY_TELEGRAM_BOT_TOKEN"),
               chat_id=os.environ.get("FOUNDRY_TELEGRAM_CHAT_ID"))
        print("Delivery confirmed")
        return 0
    except (ValueError, urllib.error.URLError, TimeoutError, OSError):
        print("Notification failed; no approval or action was inferred", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
