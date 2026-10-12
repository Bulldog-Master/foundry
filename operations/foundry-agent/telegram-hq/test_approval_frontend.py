import datetime as dt
import unittest

from approval_frontend import (
    check_callback, controller_handoff, envelope_sha256, make_decision,
)

NOW = dt.datetime(2026, 10, 12, 2, 30, tzinfo=dt.timezone.utc)
ENV = {
    "task_id": "task-abc123",
    "nonce": "0123456789abcdef",
    "expires_at": "2026-10-12T02:35:00Z",
    "task_sha256": "a" * 64,
    "workdir": "/home/foundry-agent/work/repos/foundry",
    "sandbox": "workspace-write",
    "actions": ["commit", "push", "pr-update"],
    "summary": "Update existing bounded PR",
}
PENDING = {
    "task_id": ENV["task_id"],
    "envelope_sha256": envelope_sha256(ENV),
    "nonce": ENV["nonce"],
    "chat_id": "-100123",
    "founder_user_id": "777",
    "message_id": 42,
}


def cb(data=None, *, chat="-100123", user="777", message=42, uid=9):
    return {
        "_update_id": uid,
        "id": f"cb-{uid}",
        "from": {"id": user},
        "message": {"message_id": message, "chat": {"id": chat}},
        "data": data or f"approve:{ENV['task_id']}:{ENV['nonce']}",
    }


class ApprovalFrontendTests(unittest.TestCase):
    def test_exact_approval_binding_and_handoff(self):
        self.assertEqual(check_callback(cb(), PENDING, ENV, NOW), "APPROVE")
        decision = make_decision(cb(), PENDING, ENV, None, NOW)
        handoff = controller_handoff(decision, ENV)
        self.assertEqual(handoff["actions"], ENV["actions"])
        self.assertFalse(handoff["standing_authority"])

    def test_reject_binding(self):
        event = cb(f"reject:{ENV['task_id']}:{ENV['nonce']}")
        self.assertEqual(check_callback(event, PENDING, ENV, NOW), "REJECT")
        with self.assertRaises(ValueError):
            controller_handoff(make_decision(event, PENDING, ENV, None, NOW), ENV)

    def test_wrong_user_chat_message_nonce_or_hash_rejected(self):
        self.assertIsNone(check_callback(cb(user="778"), PENDING, ENV, NOW))
        self.assertIsNone(check_callback(cb(chat="-100124"), PENDING, ENV, NOW))
        self.assertIsNone(check_callback(cb(message=43), PENDING, ENV, NOW))
        bad_pending = dict(PENDING, nonce="ffffffffffffffff")
        self.assertIsNone(check_callback(cb(), bad_pending, ENV, NOW))
        bad_pending = dict(PENDING, envelope_sha256="0" * 64)
        self.assertIsNone(check_callback(cb(), bad_pending, ENV, NOW))

    def test_expired_rejected(self):
        later = NOW + dt.timedelta(minutes=10)
        self.assertIsNone(check_callback(cb(), PENDING, ENV, later))

    def test_reserved_or_unknown_action_rejected(self):
        for action in ("merge", "sign", "production-promotion", "unknown"):
            env = dict(ENV, actions=[action])
            pending = dict(PENDING, envelope_sha256=envelope_sha256(env))
            self.assertIsNone(check_callback(cb(), pending, env, NOW))

    def test_cross_action_or_stale_envelope_rejected(self):
        decision = make_decision(cb(), PENDING, ENV, None, NOW)
        changed = dict(ENV, actions=["commit"])
        with self.assertRaises(ValueError):
            controller_handoff(decision, changed)
        changed = dict(ENV, task_sha256="b" * 64)
        with self.assertRaises(ValueError):
            controller_handoff(decision, changed)

    def test_replay_does_not_replace_first_decision(self):
        first = make_decision(cb(), PENDING, ENV, None, NOW)
        reject = cb(f"reject:{ENV['task_id']}:{ENV['nonce']}", uid=10)
        self.assertIs(make_decision(reject, PENDING, ENV, first, NOW), first)


if __name__ == "__main__":
    unittest.main()
