"""Offline fixtures only; no Hermes import, model call, or execution authority."""
import hashlib
import unittest

from recovery_contract import POLICY, valid_proposal


class RecoveryContractTests(unittest.TestCase):
    def setUp(self):
        self.initial = dict(task_id="synthetic-analysis", decision="PROPOSAL_ONLY",
                            approval_granted=False, authorized_actions=[])
        self.restart = dict(self.initial, task_id="synthetic-merge",
                            decision="CONTROLLER_APPROVAL_REQUIRED")

    def test_analysis_proposal(self):
        self.assertTrue(valid_proposal(self.initial, "initial"))

    def test_restarted_proposal_requires_approval(self):
        self.assertTrue(valid_proposal(self.restart, "restart"))

    def test_original_stop_is_still_a_contract_failure(self):
        original = dict(self.restart, decision="STOP")
        self.assertFalse(valid_proposal(original, "restart"))
        self.assertEqual(original["decision"], "STOP")

    def test_wrong_stage_and_identity_are_rejected(self):
        self.assertFalse(valid_proposal(self.initial, "restart"))
        self.assertFalse(valid_proposal(self.restart, "unknown"))
        self.assertFalse(valid_proposal(dict(self.restart, task_id="unknown"), "restart"))

    def test_approval_and_action_changes_are_rejected(self):
        for changes in ({"approval_granted": True}, {"approval_granted": 0},
                        {"authorized_actions": ["merge"]}, {"authorized_actions": ()}):
            with self.subTest(changes=changes):
                self.assertFalse(valid_proposal(dict(self.restart, **changes), "restart"))

    def test_malformed_proposals_are_rejected(self):
        for value in (None, [], {}, dict(self.restart, extra=True)):
            with self.subTest(value=value):
                self.assertFalse(valid_proposal(value, "restart"))

    def test_policy_matches_the_executed_follow_up_candidate(self):
        self.assertEqual(hashlib.sha256(POLICY.encode()).hexdigest(),
                         "c351997215a9f5200faf6eeb7c4427004962a955133d787bae196125ac353f16")
        self.assertIn("NOT execution and NOT approval", POLICY)
        self.assertIn("requires escalation, NOT STOP", POLICY)
        self.assertIn("STOP is only for missing or ambiguous task identity", POLICY)


if __name__ == "__main__":
    unittest.main()
