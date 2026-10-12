import io
import json
import unittest
from probe import probe

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
if __name__=="__main__":
    unittest.main()
