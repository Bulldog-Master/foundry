import contextlib
import io
import json
import sys
import unittest
from unittest import mock
from router import route, main

AVAIL = {"ollama": True, "codex": True, "claude": True}
def task(kind="coding", authorized=True, independent=False):
    return {"id": "demo-001", "kind": kind, "authorized": authorized, "requires_independence": independent}

class ShadowRoutingTests(unittest.TestCase):
    def test_coding_uses_existing_codex(self):
        self.assertEqual(route(task(), AVAIL)["backend"], "codex")
    def test_local_routes_ollama(self):
        self.assertEqual(route(task("local-analysis"), AVAIL)["backend"], "ollama")
    def test_no_fallback_to_unapproved_provider(self):
        self.assertEqual(route(task("local-analysis"), {**AVAIL, "ollama": False})["status"], "STOP")
    def test_no_auth(self):
        self.assertEqual(route(task(authorized=False), AVAIL)["status"], "STOP")
    def test_independence(self):
        self.assertEqual(route(task(independent=True), AVAIL)["status"], "REVIEW_REQUIRED")
    def test_independent_kind(self):
        self.assertEqual(route(task("independent-evaluation"), AVAIL)["status"], "REVIEW_REQUIRED")
    def test_unverified_states(self):
        self.assertEqual(route(task(), {"ollama": 1, "codex": True, "claude": True})["status"], "STOP")
    def test_unknown_kind(self):
        self.assertEqual(route(task("merge"), AVAIL)["status"], "STOP")
    def test_extra_fields(self):
        self.assertEqual(route({**task(), "tools": ["shell"]}, AVAIL)["status"], "STOP")
    def test_no_actor_authority(self):
        self.assertFalse(route(task(), AVAIL)["standing_authority"])

    def test_non_string_kind_returns_stop(self):
        for kind in ([], {}):
            with self.subTest(kind=kind):
                self.assertEqual(route(task(kind), AVAIL)["status"], "STOP")

    def test_deeply_nested_stdin_returns_json_stop(self):
        depth = sys.getrecursionlimit() + 100
        payload = "[" * depth + "]" * depth
        output = io.StringIO()
        with mock.patch("sys.stdin", io.StringIO(payload)):
            with contextlib.redirect_stdout(output):
                main()
        result = json.loads(output.getvalue())
        self.assertEqual(result["status"], "STOP")
        self.assertIn(result["reason"], {"malformed-json", "unexpected-envelope"})

    def test_json_decoder_recursion_error_returns_stop(self):
        # Decoder recursion limits differ across Python versions.
        output = io.StringIO()
        with mock.patch("router.json.load", side_effect=RecursionError):
            with contextlib.redirect_stdout(output):
                main()
        self.assertEqual(json.loads(output.getvalue()),
                         {"status": "STOP", "reason": "malformed-json"})

if __name__ == "__main__":
    unittest.main()
