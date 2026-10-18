import io
import http.client
import json
import os
import unittest
import urllib.request
import urllib.response
from email.message import Message
from unittest import mock
from probe import probe, open_loopback

class Response:
    def __init__(self, payload): self.value=io.BytesIO(json.dumps(payload).encode())
    def __enter__(self): return self
    def __exit__(self,*unused): return False
    def read(self, *args): return self.value.read(*args)

class ProbeTests(unittest.TestCase):
    def test_ollama_available(self):
        r=probe(opener=lambda url,timeout:Response({"models":[{"name":"local:latest"}]}),
                which=lambda name:"/usr/local/bin/hermes" if name=="hermes" else None)
        self.assertTrue(r["ollama"]["reachable"])
        self.assertEqual(r["ollama"]["model_count"],1)
        self.assertTrue(r["hermes"]["binary_found"])
        self.assertFalse(r["execution_enabled"])
    def test_ollama_unavailable(self):
        def bad(url,timeout): raise OSError("not reachable")
        r=probe(opener=bad,which=lambda name:None)
        self.assertFalse(r["ollama"]["reachable"])
        self.assertFalse(r["hermes"]["binary_found"])
    def test_malformed_response_fails_closed(self):
        r=probe(opener=lambda url,timeout:Response({"unexpected":1}),which=lambda n:None)
        self.assertFalse(r["ollama"]["reachable"])
        self.assertEqual(r["authority"],"NONE")

    def test_non_object_responses_fail_closed(self):
        for payload in ([], None, "s", [{"models": []}]):
            with self.subTest(payload=payload):
                result = probe(opener=lambda url, timeout: Response(payload),
                               which=lambda name: None)
                self.assertFalse(result["ollama"]["reachable"])

    def test_incomplete_http_response_fails_closed(self):
        def incomplete(url, timeout):
            raise http.client.IncompleteRead(b"partial", 10)
        result = probe(opener=incomplete, which=lambda name: None)
        self.assertFalse(result["ollama"]["reachable"])

    def run_fake_http(self, status, headers):
        requests = []

        class FakeHTTP(urllib.request.BaseHandler):
            handler_order = 100

            def http_open(self, request):
                requests.append((request.full_url, request.host, request.has_proxy()))
                response = urllib.response.addinfourl(
                    io.BytesIO(b'{"models": []}'), headers,
                    request.full_url, status)
                response.msg = "fixture response"
                return response

        original_builder = urllib.request.build_opener

        def build_fake(*handlers):
            client = original_builder(*handlers)
            client.add_handler(FakeHTTP())
            return client

        with mock.patch("probe.urllib.request.build_opener", side_effect=build_fake):
            result = probe(opener=open_loopback, which=lambda name: None)
        return result, requests

    def test_proxy_environment_is_ignored(self):
        environment = {"http_proxy": "http://proxy.invalid:8080",
                       "HTTP_PROXY": "http://proxy.invalid:8080",
                       "no_proxy": "", "NO_PROXY": ""}
        with mock.patch.dict(os.environ, environment, clear=True):
            result, requests = self.run_fake_http(200, Message())
        self.assertTrue(result["ollama"]["reachable"])
        self.assertEqual(requests, [
            ("http://127.0.0.1:11434/api/tags", "127.0.0.1:11434", False)])

    def test_redirect_is_refused_without_second_request(self):
        headers = Message()
        headers["Location"] = "http://redirect.invalid:8080/catalog"
        result, requests = self.run_fake_http(302, headers)
        self.assertFalse(result["ollama"]["reachable"])
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0][0], "http://127.0.0.1:11434/api/tags")

if __name__=="__main__":
    unittest.main()
