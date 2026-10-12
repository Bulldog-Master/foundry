"""Foundry workstream accountability: deterministic, read-only GitHub snapshots.

Progress means observed transition on a tracked GitHub issue/PR, not timer activity.
This cannot commission agents or infer founder approvals.
"""
import datetime as dt

UTC = dt.timezone.utc
WORKSTREAMS = (
    {"name": "Evaluator scanner remediation", "kind": "issues", "number": 29,
     "owner": "Security review workstream", "next": "Provide exact candidate to independent reviewer",
     "threshold_hours": 24},
    {"name": "Foundry organization review", "kind": "pulls", "number": 28,
     "owner": "Foundry Lead", "next": "Obtain valid independent evaluator verdict after scanner release",
     "threshold_hours": 24},
    {"name": "Telegram HQ reporting", "kind": "pulls", "number": 30,
     "owner": "Foundry-Agent implementation", "next": "Verify, review and deploy digest expansion",
     "threshold_hours": 24},
)


def parse_utc(timestamp):
    value = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise ValueError("unqualified timestamp")
    return value.astimezone(UTC)


def assess(now, snapshots, registry=WORKSTREAMS):
    """Return grounded statuses. Missing data never becomes an all-clear."""
    if now.tzinfo is None:
        raise ValueError("timezone required")
    now = now.astimezone(UTC)
    results = []
    for item in registry:
        key = f"{item['kind']}/{item['number']}"
        record = snapshots.get(key)
        base = {k: item[k] for k in ("name", "owner", "next")}
        base["key"] = key
        if not record or "updated_at" not in record:
            base.update(status="UNKNOWN", age_hours=None, reason="Source unavailable")
        else:
            seen = parse_utc(record["updated_at"])
            age = (now - seen).total_seconds() / 3600
            if age < -0.1:
                base.update(status="UNKNOWN", age_hours=None, reason="Future source timestamp")
            elif record.get("merged") is True or record.get("state") == "closed":
                base.update(status="CLOSED", age_hours=round(max(0, age), 1),
                            reason="GitHub record closed; outcome needs confirmation")
            elif age >= item["threshold_hours"]:
                base.update(status="STALE", age_hours=round(age, 1),
                            reason="No GitHub update within threshold; execution progress not proven")
            else:
                base.update(status="OPEN", age_hours=round(max(0, age), 1),
                            reason="Recently updated in GitHub; execution progress not proven")
        results.append(base)
    return results


def digest_lines(statuses):
    lines = ["Workstream accountability (GitHub-backed):"]
    for item in statuses:
        age = "unknown" if item["age_hours"] is None else f"{item['age_hours']:.1f}h"
        lines.append(f"- {item['name']}: {item['status']} | Last update: {age} ago")
        if item["status"] in ("STALE", "UNKNOWN"):
            lines.append(f"  Owner: {item['owner']} | Next: {item['next']}")
    if any(item["status"] in ("STALE", "UNKNOWN") for item in statuses):
        lines.append("ATTENTION: Missing/stale evidence requires coordination; this monitor cannot self-dispatch.")
    else:
        lines.append("No monitored GitHub record is stale; this does NOT certify absence of blockers.")
    return "\n".join(lines)
