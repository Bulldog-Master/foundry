"""Uninstalled synthetic input guard; never infer approval or rewrite model output."""
KNOWN_TASKS = frozenset({"synthetic-analysis", "synthetic-merge"})


def propose_if_identified(task_id, unique_identity, propose):
    if (not isinstance(task_id, str) or task_id not in KNOWN_TASKS
            or unique_identity is not True):
        return {"task_id": None, "decision": "STOP",
                "approval_granted": False, "authorized_actions": []}
    return propose()
