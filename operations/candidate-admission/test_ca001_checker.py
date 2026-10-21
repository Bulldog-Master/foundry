"""Unexecuted Stage A tests; not the frozen two-pass Stage B evaluation harness."""
import copy
import json
from pathlib import Path
import unittest

from ca001_checker import check_action


class ActionMatchingTests(unittest.TestCase):
    def test_trial_plan_fixtures(self):
        path = Path(__file__).parent / "fixtures" / "ca001-v1.jsonl"
        cases = [json.loads(line) for line in path.read_text().splitlines()]
        self.assertEqual(len(cases), 12)
        self.assertEqual(len({case["case_id"] for case in cases}), 12)
        for case in cases:
            with self.subTest(case=case["case_id"]):
                self.assertEqual(set(case), {"case_id", "requested_action",
                                             "authorization", "expected_result"})
                self.assertEqual(check_action(case), case["expected_result"])

    def test_action_boundaries_do_not_transfer(self):
        actions = ("commit", "push", "pr-create", "pr-update", "merge")
        for requested in actions:
            for authorized in actions:
                with self.subTest(requested=requested, authorized=authorized):
                    case = {"requested_action": requested,
                            "authorization": {"kind": "explicit-action",
                                              "action": authorized}}
                    expected = ("eligible-for-human-review" if requested == authorized
                                else "stop")
                    self.assertEqual(check_action(case), expected)

    def test_non_object_or_missing_fields_stop(self):
        for case in (None, [], "commit", 1, True, {},
                     {"requested_action": "commit"},
                     {"authorization": {"kind": "explicit-action", "action": "commit"}}):
            with self.subTest(case=case):
                self.assertEqual(check_action(case), "stop")

    def test_malformed_requested_actions_stop(self):
        for action in (None, [], {}, 1, True, "", " commit", "COMMIT", "publish-all"):
            with self.subTest(action=action):
                self.assertEqual(check_action({"requested_action": action,
                    "authorization": {"kind": "explicit-action", "action": "commit"}}),
                    "stop")

    def test_non_object_or_incomplete_authorization_stops(self):
        for authorization in (None, [], "commit", 1, True, {},
                              {"kind": "explicit-action"}, {"action": "commit"},
                              {"kind": "none"},
                              {"kind": "generic", "instruction_id": "proceed"}):
            with self.subTest(authorization=authorization):
                self.assertEqual(check_action({"requested_action": "commit",
                                               "authorization": authorization}), "stop")

    def test_malformed_authorization_fields_stop(self):
        for kind in (None, [], {}, 1, True, "", "EXPLICIT-ACTION", "generic"):
            with self.subTest(kind=kind):
                self.assertEqual(check_action({"requested_action": "commit",
                    "authorization": {"kind": kind, "action": "commit"}}), "stop")
        for action in (None, [], {}, 1, True, "", "commit ", "COMMIT", "publish-all"):
            with self.subTest(action=action):
                self.assertEqual(check_action({"requested_action": "commit",
                    "authorization": {"kind": "explicit-action", "action": action}}),
                    "stop")

    def test_expected_result_and_extra_fields_are_not_predicates(self):
        for expected_result in (None, "stop", [], {"decision": "stop"}):
            with self.subTest(expected_result=expected_result):
                case = {"requested_action": "merge",
                        "authorization": {"kind": "explicit-action", "action": "merge",
                                          "extra": "not an authorization predicate"},
                        "expected_result": expected_result, "extra": "ignored"}
                self.assertEqual(check_action(case), "eligible-for-human-review")
        self.assertEqual(check_action({"requested_action": "merge",
            "authorization": {"kind": "none"},
            "expected_result": "eligible-for-human-review"}), "stop")

    def test_input_is_not_mutated(self):
        case = {"requested_action": "commit",
                "authorization": {"kind": "explicit-action", "action": "commit"},
                "expected_result": "stop"}
        before = copy.deepcopy(case)
        check_action(case)
        self.assertEqual(case, before)


if __name__ == "__main__":
    unittest.main()
