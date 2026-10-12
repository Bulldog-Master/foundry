"""Read-only local Foundry service and journal metadata for Telegram digests.

Never exports raw journal messages, invocation data, credentials, paths from log
content, or sealed evidence. Host-local coverage only.
"""
import datetime as dt
import json
import subprocess

UNITS = (
    "foundry-evaluator.service",
    "foundry-evaluator.timer",
    "foundry-telegram-watch.service",
    "foundry-telegram-watch.timer",
    "foundry-telegram-digest-daily.timer",
    "foundry-telegram-digest-weekly.timer",
    "foundry-telegram-digest-monthly.timer",
)
EVENT_UNITS = ("foundry-evaluator.service", "foundry-telegram-watch.service",
               "foundry-telegram-digest@daily.service",
               "foundry-telegram-digest@weekly.service",
               "foundry-telegram-digest@monthly.service")
UTC = dt.timezone.utc


def command(argv, runner=subprocess.run):
    result = runner(argv, check=True, capture_output=True, text=True, timeout=25)
    return result.stdout


def snapshot(runner=subprocess.run):
    states = {}
    for unit in UNITS:
        try:
            raw = command(["systemctl", "show", unit, "--property=LoadState,ActiveState,UnitFileState",
                           "--no-pager"], runner)
            values = dict(line.split("=", 1) for line in raw.splitlines() if "=" in line)
            states[unit] = (values.get("LoadState", "unknown"),
                            values.get("ActiveState", "unknown"),
                            values.get("UnitFileState", "unknown"))
        except (subprocess.SubprocessError, OSError, ValueError):
            states[unit] = ("unavailable", "unavailable", "unavailable")
    return states


def counts(start, end, runner=subprocess.run):
    # Journal format is parsed locally. MESSAGE and all unrestricted fields
    # are deliberately ignored; only priority, trusted unit, timestamp used.
    result = {}
    since, until = (x.astimezone(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
                    for x in (start, end))
    for unit in EVENT_UNITS:
        try:
            raw = command(["journalctl", "--unit", unit, "--since", since, "--until", until,
                           "--no-pager", "--output=json", "--quiet"], runner)
            seen = errors = 0
            for line in raw.splitlines():
                entry = json.loads(line)
                actual_unit = entry.get("_SYSTEMD_UNIT")
                if actual_unit != unit:
                    continue
                micros = int(entry["__REALTIME_TIMESTAMP"])
                when = dt.datetime.fromtimestamp(micros / 1_000_000, UTC)
                if not start <= when < end:
                    continue
                seen += 1
                if int(entry.get("PRIORITY", "6")) <= 3:
                    errors += 1
            result[unit] = (seen, errors)
        except (subprocess.SubprocessError, OSError, ValueError, KeyError, OverflowError):
            result[unit] = None
    return result


def section(start, end, runner=subprocess.run):
    states = snapshot(runner)
    events = counts(start, end, runner)
    lines = ["Local WSL service health (point-in-time):"]
    for unit, (loaded, active, enabled) in states.items():
        lines.append(f"- {unit}: {active} ({loaded}; {enabled})")
    lines.append("Journal metadata events in period (messages never exported):")
    for unit, count in events.items():
        if count is None:
            lines.append(f"- {unit}: UNAVAILABLE")
        else:
            lines.append(f"- {unit}: {count[0]} journal entries, {count[1]} priority-error entries")
    lines.append("Coverage: WSL host only; journal entries are not task counts or evaluation verdicts. Caller/Sandbox/Standalone remote events not connected.")
    return "\n".join(lines)
