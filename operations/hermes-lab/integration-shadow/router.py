"""Inert Foundry backend routing experiment. No provider calls or actions."""
import json
import sys

ALLOWED = frozenset({"local-analysis", "coding", "independent-evaluation"})

def route(task, available):
    """Propose only; authorized/available are supplied data, not verified facts."""
    if not isinstance(task, dict) or not isinstance(available, dict):
        return {"status": "STOP", "reason": "invalid-input"}
    if set(task) != {"id", "kind", "authorized", "requires_independence"}:
        return {"status": "STOP", "reason": "unexpected-schema"}
    if (not isinstance(task["id"], str) or not task["id"]
            or not isinstance(task["kind"], str) or task["kind"] not in ALLOWED):
        return {"status": "STOP", "reason": "invalid-task"}
    if type(task["authorized"]) is not bool or type(task["requires_independence"]) is not bool:
        return {"status": "STOP", "reason": "invalid-flags"}
    if not task["authorized"]:
        return {"status": "STOP", "reason": "not-authorized"}
    if set(available) != {"ollama", "codex", "claude"} or any(type(v) is not bool for v in available.values()):
        return {"status": "STOP", "reason": "unverified-provider-state"}
    if task["requires_independence"] or task["kind"] == "independent-evaluation":
        return {"status": "REVIEW_REQUIRED", "reason": "independent-evaluator-eligibility-must-be-verified"}
    candidate = "ollama" if task["kind"] == "local-analysis" else "codex"
    if not available[candidate]:
        return {"status": "STOP", "reason": "backend-not-confirmed"}
    return {"status": "PROPOSAL_ONLY", "backend": candidate, "task_id": task["id"], "standing_authority": False}

def main():
    try:
        payload = json.load(sys.stdin)
        result = route(payload.get("task"), payload.get("available")) if isinstance(payload, dict) and set(payload) == {"task", "available"} else {"status": "STOP", "reason": "unexpected-envelope"}
    except (ValueError, UnicodeDecodeError, RecursionError):
        result = {"status": "STOP", "reason": "malformed-json"}
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
