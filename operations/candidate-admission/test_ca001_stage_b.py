"""Harness mechanics only. Never import the CA-001 candidate or Stage A tests."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import ca001_harness as harness


def stand_in_cases():
    return [{"case_id": "stand-in-" + str(i), "requested_action": "inert",
             "authorization": {"kind": "none"}, "expected_result": "stop"}
            for i in range(12)]


def stand_in_suite(failure=False):
    class InertTest(unittest.TestCase):
        def runTest(self):
            self.assertFalse(failure)
    return unittest.TestSuite(InertTest() for _ in range(8))


class HarnessMechanicsTests(unittest.TestCase):
    def test_stable_bytes_without_candidate_or_timing(self):
        one, code = harness.run_checks(lambda _: "stop", stand_in_suite(), stand_in_cases())
        two, _ = harness.run_checks(lambda _: "stop", stand_in_suite(), stand_in_cases())
        self.assertEqual(code, 0)
        self.assertEqual(one, two)
        self.assertTrue(one.endswith(b"\n"))
        self.assertEqual(json.loads(one)["tests_run"], 8)

    def test_stand_in_mismatch_is_not_success(self):
        output, code = harness.run_checks(lambda _: "eligible-for-human-review",
                                          stand_in_suite(), stand_in_cases())
        self.assertEqual(code, 1)
        self.assertFalse(json.loads(output)["all_expected_results"])

    def test_unit_test_failure_is_not_success(self):
        output, code = harness.run_checks(lambda _: "stop", stand_in_suite(True),
                                          stand_in_cases())
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output)["failures"], 8)

    def test_invalid_result_aborts(self):
        with self.assertRaises(harness.IntegrityError):
            harness.run_checks(lambda _: [], stand_in_suite(), stand_in_cases())

    def test_expected_result_is_not_forwarded(self):
        seen = []
        def stand_in(value):
            seen.append(set(value))
            return "stop"
        harness.run_checks(stand_in, stand_in_suite(), stand_in_cases())
        self.assertEqual(seen, [{"requested_action", "authorization"}] * 12)

    def test_strict_json_parse(self):
        for value in ('{"x":1,"x":2}', 'NaN', '{', b'\xff'):
            with self.subTest(value=value), self.assertRaises(harness.IntegrityError):
                harness.decode(value)

    def test_fixture_format_errors_are_integrity_errors(self):
        data = b"\n".join(harness.canonical(c).rstrip(b"\n") for c in stand_in_cases())
        self.assertEqual(len(harness.load_cases(data)), 12)
        for bad in (data + b"\n\n", b"\n" + data, data.replace(b'"stand-in-1"', b'"stand-in-0"'),
                    data.replace(b'"expected_result":"stop"', b'"extra":1,"expected_result":"stop"', 1)):
            with self.subTest(bad=bad[:30]), self.assertRaises(harness.IntegrityError):
                harness.load_cases(bad)

    def test_unexpected_output_is_not_silently_discarded(self):
        with self.assertRaises(harness.IntegrityError):
            with contextlib.redirect_stdout(harness.RejectOutput()):
                print("unexpected")

    def test_source_hash_and_symlink_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            expected = {}
            for name in harness.FILES:
                path = root / name
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(b"inert stand-in bytes")
                expected[name] = harness.digest(path.read_bytes())
            self.assertEqual(len(harness.source_snapshot(root, expected)), 7)
            (root / "ca001_checker.py").write_bytes(b"changed stand-in bytes")
            with self.assertRaises(harness.IntegrityError):
                harness.source_snapshot(root, expected)
            (root / "ca001_checker.py").unlink()
            (root / "ca001_checker.py").symlink_to(root / "PROTOCOL-v0.1.md")
            with self.assertRaises(harness.IntegrityError):
                harness.source_snapshot(root, expected)

    def test_no_stage_a_imported(self):
        import sys
        self.assertNotIn("ca001_checker", sys.modules)
        self.assertNotIn("test_ca001_checker", sys.modules)

    def test_large_source_is_rejected_before_reading(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            first = root / harness.FILES[0]
            first.write_bytes(b"x" * 65537)
            with self.assertRaises(harness.IntegrityError):
                harness.source_snapshot(root, dict.fromkeys(harness.FILES, "0" * 64))

    def test_default_entrypoint_refuses_execution(self):
        with patch("sys.argv", ["ca001_harness.py"]), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as stopped:
                harness.main()
        self.assertEqual(stopped.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
