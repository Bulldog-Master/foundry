import importlib.util
import io
import json
import pathlib
import unittest

P = pathlib.Path(__file__).with_name("notify.py")
spec = importlib.util.spec_from_file_location("notify", P)
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)


class FakeResponse:
    def __init__(self, raw=b'{"ok":true}'):
        self.raw = raw
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self, limit):
        return self.raw


class NotificationTests(unittest.TestCase):
    def test_render_link(self):
        t = n.render("ACTION_REQUIRED", "Approve?", "Evidence ready",
                     "https://github.com/Bulldog-Master/foundry/issues/29")
        self.assertIn("issues/29", t)

    def test_reject_non_foundry_links(self):
        for link in ("http://github.com/Bulldog-Master/foundry/issues/29",
                     "https://evil.example/p/1",
                     "https://github.com/Bulldog-Master/foundry/issues/29?x=1",
                     "https://github.com/Bulldog-Master/foundry/issues/29#token",
                     "https://github.com/Bulldog-Master/foundry/pull/0"):
            with self.subTest(link=link), self.assertRaises(ValueError):
                n.validate_link(link)

    def test_reject_unbounded_or_empty(self):
        with self.assertRaises(ValueError):
            n.render("INFO", "title", "x" * 4000, None)
        with self.assertRaises(ValueError):
            n.render("INFO", " ", "body", None)

    def test_send_payload_without_external_network(self):
        calls = []
        def opener(request, timeout):
            calls.append((request, timeout))
            return FakeResponse()
        n.notify("hello", token="123:example-token", chat_id="-123", opener=opener)
        self.assertEqual(len(calls), 1)
        payload = json.loads(calls[0][0].data)
        self.assertEqual(payload["chat_id"], "-123")
        self.assertEqual(payload["text"], "hello")
        self.assertTrue(payload["disable_web_page_preview"])

    def test_fail_closed_bad_credentials(self):
        with self.assertRaises(ValueError):
            n.notify("hello", token="", chat_id="123")
        with self.assertRaises(ValueError):
            n.notify("hello", token="123:foo", chat_id="not-an-id")

    def test_fail_closed_provider_response(self):
        with self.assertRaises(ValueError):
            n.notify("hi", token="123:foo", chat_id="123",
                     opener=lambda *args, **kw: FakeResponse(b'{"ok":false}'))

    def test_dry_run_has_no_send(self):
        self.assertEqual(n.main(["--kind", "INFO", "--title", "Test",
                                 "--summary", "Dry run"]), 0)


if __name__ == "__main__":
    unittest.main()
