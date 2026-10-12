"""Strictly advisory Jev output validator for synthetic Foundry evaluation. No provider or tool calls."""
from datetime import datetime, timezone
KINDS = {"task-triage", "evidence-sufficiency", "review-needed"}
def assess(packet, decision, now=None):
    now = now or datetime.now(timezone.utc)
    if not isinstance(packet, dict) or not isinstance(decision, dict):
        return {"status": "STOP", "reason": "invalid-input"}
    if set(packet) != {"task_id", "kind", "sources", "generated_at"}:
        return {"status": "STOP", "reason": "invalid-evidence-schema"}
    if not isinstance(packet["task_id"], str) or not packet["task_id"] or packet["kind"] not in KINDS:
        return {"status": "STOP", "reason": "invalid-task"}
    if not isinstance(packet["sources"], list) or not (1 <= len(packet["sources"]) <= 32):
        return {"status": "STOP", "reason": "missing-evidence"}
    def timeparse(value):
        result = datetime.fromisoformat(value.replace("Z","+00:00"))
        if result.tzinfo is None: raise ValueError("timezone missing")
        return result
    try:
        captured=timeparse(packet["generated_at"])
        if captured>now or (now-captured).total_seconds()>86400: raise ValueError("stale")
    except (ValueError,TypeError,AttributeError):
        return {"status": "STOP", "reason": "invalid-or-stale-time"}
    for item in packet["sources"]:
        if not isinstance(item,dict) or set(item)!={"id","observed_at"} or not isinstance(item["id"],str) or not item["id"].strip():
            return {"status":"STOP","reason":"invalid-source"}
        try:
            observed=timeparse(item["observed_at"])
            if observed>now: raise ValueError("future source")
        except (ValueError,TypeError,AttributeError):
            return {"status":"STOP","reason":"invalid-source-time"}
    if set(decision)!={"choice","probability","model"} or decision["model"]!="typesafe-ai/jev":
        return {"status":"STOP","reason":"invalid-decision-schema"}
    if decision["choice"] not in {"routine","investigate","escalate"}:
        return {"status":"STOP","reason":"unknown-choice"}
    probability=decision["probability"]
    if type(probability) not in (int,float) or not (0<=probability<=1):
        return {"status":"STOP","reason":"invalid-probability"}
    return {"status":"ADVISORY_ONLY","task_id":packet["task_id"],"signal":decision["choice"],"probability":probability,"source_count":len(packet["sources"]),"standing_authority":False}
