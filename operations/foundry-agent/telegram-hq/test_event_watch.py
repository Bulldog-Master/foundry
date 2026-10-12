import importlib.util
import io
import json
import pathlib
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("event_watch", pathlib.Path(__file__).with_name("event_watch.py"))
import sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class Response:
    def __init__(self, obj):
        self.body = io.BytesIO(json.dumps(obj).encode())
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self, *args): return self.body.read(*args)


def fake_fetch(req, timeout):
    url = req.full_url
    if "/pulls/" in url:
        return Response({"state": "open", "draft": False, "merged": False,
                         "head": {"sha": "a" * 40}, "updated_at": "2026-10-11T00:00:00Z"})
    return Response({"state": "open", "updated_at": "2026-10-11T00:00:00Z", "comments": 0})


class WatchTests(unittest.TestCase):
    def test_first_run_baseline_no_notification(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "state.json"
            calls = []
            self.assertEqual(m.watch(path, fetch=fake_fetch, send=lambda *a, **kw: calls.append(a)), 0)
            self.assertTrue(path.exists())
            self.assertFalse(calls)

    def test_unchanged_deduplicated(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "state.json"
            calls = []
            send = lambda *a, **kw: calls.append(a)
            m.watch(path, fetch=fake_fetch, send=send)
            m.watch(path, fetch=fake_fetch, send=send)
            self.assertFalse(calls)

    def test_transition_notifies_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "state.json"
            m.watch(path, fetch=fake_fetch, send=lambda *a, **kw: None)
            first = json.loads(path.read_text())
            first["pulls/30"]["draft"] = True
            path.write_text(json.dumps(first))
            calls = []
            self.assertEqual(m.watch(path, fetch=fake_fetch, send=lambda *a, **kw: calls.append(a)), 1)
            self.assertEqual(len(calls), 1)
            self.assertEqual(m.watch(path, fetch=fake_fetch, send=lambda *a, **kw: calls.append(a)), 0)

    def test_failed_delivery_does_not_advance(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "state.json"
            m.watch(path, fetch=fake_fetch, send=lambda *a, **kw: None)
            first = json.loads(path.read_text())
            first["issues/29"]["comments"] = 1
            path.write_text(json.dumps(first))
            before = path.read_bytes()
            def fail(*a, **kw): raise RuntimeError("failure")
            with self.assertRaises(RuntimeError):
                m.watch(path, fetch=fake_fetch, send=fail)
            self.assertEqual(path.read_bytes(), before)

    def test_reject_symlink_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "state.json"
            target = pathlib.Path(tmp) / "real.json"
            target.write_text("{}")
            path.symlink_to(target)
            with self.assertRaises(ValueError):
                m.watch(path, fetch=fake_fetch)


if __name__ == "__main__":
    unittest.main()
