#!/usr/bin/env python3
"""Foundry HQ repository digest: read-only GitHub, outbound Telegram only.

Scopes: repository commits, PRs and issues. Does not assert coverage of agent,
host, evaluator or Telegram activity until those durable event sources exist.
"""
import argparse
import calendar
import datetime as dt
import json
import os
from pathlib import Path
import sys
import urllib.request

from notify import notify, render
from local_activity import section as local_section

REPO = "Bulldog-Master/foundry"
UTC = dt.timezone.utc


def period(mode, now):
    now = now.astimezone(UTC)
    if mode == "daily":
        return now - dt.timedelta(hours=24), now
    if mode == "weekly":
        return now - dt.timedelta(days=7), now
    if mode == "monthly":
        first = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        prev = (first - dt.timedelta(days=1)).replace(day=1)
        return prev, first
    raise ValueError("unknown period")


def api_page(path, page, fetch):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/{path}" +
        ("&" if "?" in path else "?") + f"per_page=100&page={page}",
        headers={"Accept": "application/vnd.github+json",
                 "User-Agent": "foundry-hq-digest/0.1"})
    with fetch(req, timeout=20) as response:
        value = json.load(response)
    if not isinstance(value, list):
        raise ValueError("GitHub returned an unexpected response")
    return value


def collect(path, fetch, max_pages=10):
    result = []
    for page in range(1, max_pages + 1):
        chunk = api_page(path, page, fetch)
        result.extend(chunk)
        if len(chunk) < 100:
            return result
    raise ValueError("GitHub pagination cap reached; refusing incomplete summary")


def parse_time(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def gather(start, end, fetch=urllib.request.urlopen):
    # issue list includes PRs; exclude PRs here to prevent double-counting.
    stamp = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    commits = collect(f"commits?since={stamp}", fetch)
    issues = collect(f"issues?state=all&since={stamp}&sort=updated&direction=desc", fetch)
    prs = collect("pulls?state=all&sort=updated&direction=desc", fetch)
    included = lambda time: start <= parse_time(time) < end
    commits = [c for c in commits if included(c["commit"]["committer"]["date"])]
    issues = [i for i in issues if "pull_request" not in i and included(i["updated_at"])]
    prs = [p for p in prs if included(p["updated_at"])]
    return commits, issues, prs


def reviews_for(prs, start, end, fetch=urllib.request.urlopen):
    """Fetch actual submitted review events, not just PR updated timestamps."""
    events = []
    for pr in prs:
        review_list = collect(f"pulls/{pr['number']}/reviews", fetch, max_pages=4)
        for review in review_list:
            submitted = review.get("submitted_at")
            if submitted and included(start, end, submitted):
                events.append((pr["number"], review.get("state", "UNKNOWN"), submitted))
    return sorted(events, key=lambda row: row[2], reverse=True)


def summary(mode, start, end, commits, issues, prs, reviews=None, local=None):
    label = {"daily": "24-hour", "weekly": "7-day",
             "monthly": "previous-month"}[mode]
    reviews = [] if reviews is None else reviews
    merged = [p for p in prs if p.get("merged_at") and included(start, end, p["merged_at"])]
    closed = [p for p in prs if not p.get("merged_at") and p.get("closed_at")
              and included(start, end, p["closed_at"])]
    opened = [p for p in prs if p.get("created_at") and included(start, end, p["created_at"])]
    new_issues = [i for i in issues if i.get("created_at") and included(start, end, i["created_at"])]
    lines = [
        f"Window (UTC): {start:%Y-%m-%d %H:%M} to {end:%Y-%m-%d %H:%M}",
        f"Commits: {len(commits)} | PRs updated: {len(prs)} | Issues updated: {len(issues)}",
        f"New PRs: {len(opened)} | Merged: {len(merged)} | Closed without merge: {len(closed)}",
        f"New issues: {len(new_issues)} | Submitted reviews: {len(reviews)}",
    ]
    for number, state, _ in reviews[:5]:
        lines.append(f"Review {state} on PR #{number} — https://github.com/{REPO}/pull/{number}")
    for item in merged[:5]:
        lines.append(f"MERGED PR #{item['number']} — https://github.com/{REPO}/pull/{item['number']}")
    for item in prs[:5]:
        lines.append(f"PR #{item['number']}: {item['state']}" +
                     (" (draft)" if item.get("draft") else "") +
                     f" — https://github.com/{REPO}/pull/{item['number']}")
    for item in issues[:4]:
        lines.append(f"Issue #{item['number']}: {item['state']}" +
                     f" — https://github.com/{REPO}/issues/{item['number']}")
    if len(prs) > 5 or len(issues) > 4 or len(reviews) > 5 or len(merged) > 5:
        lines.append("Additional records exist; review GitHub for the full set.")
    lines.append("Coverage: GitHub repository activity; review events use GitHub submission timestamps.")
    lines.append(local if local is not None else
                 "Host/agent/evaluator activity not yet connected.")
    return render("INFO", f"Foundry {label} activity summary",
                  "\n".join(lines), None)


def included(start, end, timestamp):
    return start <= parse_time(timestamp) < end


def run(mode, now, fetch=urllib.request.urlopen, include_local=False):
    start, end = period(mode, now)
    commits, issues, prs = gather(start, end, fetch)
    reviews = reviews_for(prs, start, end, fetch)
    local = local_section(start, end) if include_local else None
    return summary(mode, start, end, commits, issues, prs, reviews, local)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--period", choices=["daily", "weekly", "monthly"], required=True)
    parser.add_argument("--token-file", required=True)
    parser.add_argument("--chat-file", required=True)
    args = parser.parse_args()
    try:
        credential_files = [Path(args.token_file), Path(args.chat_file)]
        for p in credential_files:
            if p.is_symlink() or not p.is_file() or p.stat().st_mode & 0o077:
                raise ValueError("unsafe credential file")
        text = run(args.period, dt.datetime.now(UTC), include_local=True)
        notify(text, token=credential_files[0].read_text().strip(),
               chat_id=credential_files[1].read_text().strip())
        print("Digest delivered")
        return 0
    except Exception:
        print("BLOCKED: digest collection or Telegram delivery failed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
