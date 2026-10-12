#!/usr/bin/env python3
"""Offline validation for a bounded Telegram approval front-end candidate.

This module does not poll Telegram, launch Foundry-Agent, write GitHub, or perform
reserved acts. It validates a callback against a frozen task envelope and emits a
controller handoff record only when exact bindings match.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json

ALLOWED_ACTIONS = {"commit", "push", "pr-create", "pr-update"}
RESERVED_ACTIONS = {
    "merge", "sign", "production-promotion", "doctrine-change",
    "founder-override", "sealed-truth-change", "provider-authorization",
}


def canonical_bytes(envelope):
    if not isinstance(envelope, dict):
        raise ValueError("envelope must be object")
    return (json.dumps(envelope, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def envelope_sha256(envelope):
    return hashlib.sha256(canonical_bytes(envelope)).hexdigest()


def parse_utc(value):
    parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.astimezone(dt.timezone.utc)


def validate_envelope(envelope, now):
    required = {
        "task_id", "nonce", "expires_at", "task_sha256", "workdir",
        "sandbox", "actions", "summary",
    }
    if not isinstance(envelope, dict) or set(envelope) != required:
        raise ValueError("unexpected envelope schema")
    if not isinstance(envelope["task_id"], str) or not envelope["task_id"]:
        raise ValueError("invalid task id")
    if not isinstance(envelope["nonce"], str) or len(envelope["nonce"]) < 16:
        raise ValueError("invalid nonce")
    if envelope["sandbox"] not in ("read-only", "workspace-write"):
        raise ValueError("invalid sandbox")
    if not isinstance(envelope["workdir"], str) or not envelope["workdir"].startswith("/home/foundry-agent/work/"):
        raise ValueError("invalid workdir")
    if not isinstance(envelope["summary"], str) or not envelope["summary"].strip():
        raise ValueError("invalid summary")
    if not isinstance(envelope["task_sha256"], str) or len(envelope["task_sha256"]) != 64:
        raise ValueError("invalid task hash")
    actions = envelope["actions"]
    if not isinstance(actions, list) or len(actions) != len(set(actions)):
        raise ValueError("invalid actions")
    if any(a in RESERVED_ACTIONS for a in actions):
        raise ValueError("reserved action")
    if any(a not in ALLOWED_ACTIONS for a in actions):
        raise ValueError("unknown action")
    expires = parse_utc(envelope["expires_at"])
    now = now.astimezone(dt.timezone.utc)
    if expires <= now:
        raise ValueError("expired")
    return True


def check_callback(callback, pending, envelope, now):
    """Return APPROVE/REJECT only for an exact, unexpired binding."""
    if not all(isinstance(x, dict) for x in (callback, pending, envelope)):
        return None
    try:
        validate_envelope(envelope, now)
    except (ValueError, TypeError):
        return None
    if pending.get("task_id") != envelope["task_id"]:
        return None
    if pending.get("envelope_sha256") != envelope_sha256(envelope):
        return None
    if pending.get("nonce") != envelope["nonce"]:
        return None

    message = callback.get("message") or {}
    chat = message.get("chat") or {}
    sender = callback.get("from") or {}
    if str(chat.get("id")) != str(pending.get("chat_id")):
        return None
    if str(sender.get("id")) != str(pending.get("founder_user_id")):
        return None
    if message.get("message_id") != pending.get("message_id"):
        return None

    data = callback.get("data")
    if data == "approve:" + envelope["task_id"] + ":" + envelope["nonce"]:
        return "APPROVE"
    if data == "reject:" + envelope["task_id"] + ":" + envelope["nonce"]:
        return "REJECT"
    return None


def make_decision(callback, pending, envelope, prior, now):
    """Create one immutable-intent decision record; replay returns prior unchanged."""
    if prior:
        return prior
    action = check_callback(callback, pending, envelope, now)
    if action is None:
        return None
    return {
        "decision": action,
        "task_id": envelope["task_id"],
        "envelope_sha256": envelope_sha256(envelope),
        "task_sha256": envelope["task_sha256"],
        "actions": list(envelope["actions"]),
        "decided_at": now.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "telegram_update_id": callback.get("_update_id"),
        "chat_id": str((callback.get("message") or {}).get("chat", {}).get("id")),
        "founder_user_id": str((callback.get("from") or {}).get("id")),
        "message_id": (callback.get("message") or {}).get("message_id"),
    }


def controller_handoff(decision, envelope):
    """Return a bounded handoff only for an exact APPROVE record."""
    if not isinstance(decision, dict) or decision.get("decision") != "APPROVE":
        raise ValueError("approval required")
    if decision.get("envelope_sha256") != envelope_sha256(envelope):
        raise ValueError("stale approval")
    if decision.get("task_sha256") != envelope.get("task_sha256"):
        raise ValueError("task hash mismatch")
    if decision.get("actions") != envelope.get("actions"):
        raise ValueError("action mismatch")
    return {
        "task_id": envelope["task_id"],
        "task_sha256": envelope["task_sha256"],
        "envelope_sha256": decision["envelope_sha256"],
        "workdir": envelope["workdir"],
        "sandbox": envelope["sandbox"],
        "actions": list(envelope["actions"]),
        "approval_record": decision,
        "standing_authority": False,
    }
