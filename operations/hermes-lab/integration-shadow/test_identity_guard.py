"""Offline synthetic regressions; no Hermes imports, model calls or authority."""
import hashlib
from pathlib import Path
import unittest
from unittest.mock import Mock

import identity_guard
from identity_guard import propose_if_identified
from recovery_contract import valid_proposal


class IdentityGuardTests(unittest.TestCase):
    def test_invalid_or_ambiguous_identity_stops_before_callback(self):
        for task, unique in ((None, True), ([], True), ("", True), (" ", True),
                             ("unknown", True), ("synthetic-merge", False),
                             ("synthetic-merge", 1), ("synthetic-merge", None)):
            with self.subTest(task=task, unique=unique):
                callback = Mock()
                value = propose_if_identified(task, unique, callback)
                self.assertEqual(value, {"task_id": None, "decision": "STOP",
                                         "approval_granted": False, "authorized_actions": []})
                callback.assert_not_called()

    def test_identified_analysis_keeps_existing_contract(self):
        raw = dict(task_id="synthetic-analysis", decision="PROPOSAL_ONLY",
                   approval_granted=False, authorized_actions=[])
        callback = Mock(return_value=raw)
        value = propose_if_identified("synthetic-analysis", True, callback)
        self.assertIs(value, raw)
        self.assertTrue(valid_proposal(value, "initial"))
        callback.assert_called_once_with()

    def test_known_protected_identity_does_not_imply_approval(self):
        raw = dict(task_id="synthetic-merge", decision="CONTROLLER_APPROVAL_REQUIRED",
                   approval_granted=False, authorized_actions=[])
        callback = Mock(return_value=raw)
        value = propose_if_identified("synthetic-merge", True, callback)
        self.assertIs(value, raw)
        self.assertTrue(valid_proposal(value, "restart"))
        callback.assert_called_once_with()

    def test_raw_wrong_or_unsafe_output_is_not_rewritten_into_a_pass(self):
        for decision, approved, actions in (("STOP", False, []),
                                            ("CONTROLLER_APPROVAL_REQUIRED", True, ["merge"])):
            with self.subTest(decision=decision, approved=approved):
                raw = dict(task_id="synthetic-merge", decision=decision,
                           approval_granted=approved, authorized_actions=actions)
                callback = Mock(return_value=raw)
                value = propose_if_identified("synthetic-merge", True, callback)
                self.assertIs(value, raw)
                self.assertFalse(valid_proposal(value, "restart"))
                callback.assert_called_once_with()

    def test_missing_identity_failure_remains_separate_from_preflight_stop(self):
        failed = dict(task_id=None, decision="CONTROLLER_APPROVAL_REQUIRED",
                      approval_granted=False, authorized_actions=[])
        original = failed.copy()
        callback = Mock(return_value=failed)
        value = propose_if_identified(None, True, callback)
        self.assertEqual(value["decision"], "STOP")
        callback.assert_not_called()
        self.assertEqual(failed, original)
        self.assertFalse(valid_proposal(failed, "restart"))

    def test_public_guard_matches_helper_used_in_live_client(self):
        source = Path(identity_guard.__file__).read_bytes()
        self.assertEqual(hashlib.sha256(source).hexdigest(),
                         "72eb5340a5df64497c73a48ac8d86965ca4699d076e6ecb131d0e8d45065128e")


if __name__ == "__main__":
    unittest.main()
