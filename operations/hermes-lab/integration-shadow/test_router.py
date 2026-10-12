import unittest
from router import route

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

if __name__ == "__main__":
    unittest.main()
