"""Pure advisory action matching; not real approval, admission or merge readiness."""

RECOGNIZED_ACTIONS = frozenset({"commit", "push", "pr-create", "pr-update", "merge"})


def check_action(case):
    """Read only requested_action and authorization; never infer authority."""
    if not isinstance(case, dict):
        return "stop"
    requested = case.get("requested_action")
    authorization = case.get("authorization")
    if not isinstance(requested, str) or requested not in RECOGNIZED_ACTIONS:
        return "stop"
    if not isinstance(authorization, dict):
        return "stop"
    authorized = authorization.get("action")
    if (authorization.get("kind") == "explicit-action"
            and isinstance(authorized, str)
            and authorized in RECOGNIZED_ACTIONS
            and authorized == requested):
        return "eligible-for-human-review"
    return "stop"
