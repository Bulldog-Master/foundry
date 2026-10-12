import pathlib
import tempfile
import unittest
from preflight import inspect


class PreflightTests(unittest.TestCase):
    def test_commissioned_actor(self):
        with tempfile.TemporaryDirectory() as temp:
            work=pathlib.Path(temp)
            contract=work/"AGENTS.md"
            contract.write_text("test fixture")
            result=inspect(1000,work,contract,lambda name:"/fixture/codex",None)
            self.assertEqual(result["read_only_preflight"],"PASS")
            self.assertEqual(result["task_execution"],"NOT_ACTIVATED")

    def test_reject_root(self):
        with tempfile.TemporaryDirectory() as temp:
            path=pathlib.Path(temp); (path/"AGENTS.md").write_text("fixture")
            with self.assertRaises(RuntimeError):
                inspect(0,path,path/"AGENTS.md",lambda name:"/fixture/codex",None)

    def test_reject_missing_contract(self):
        with tempfile.TemporaryDirectory() as temp:
            path=pathlib.Path(temp)
            with self.assertRaises(RuntimeError):
                inspect(1000,path,path/"AGENTS.md",lambda name:"/fixture/codex",None)

    def test_reject_missing_agent_binary(self):
        with tempfile.TemporaryDirectory() as temp:
            path=pathlib.Path(temp); (path/"AGENTS.md").write_text("fixture")
            with self.assertRaises(RuntimeError):
                inspect(1000,path,path/"AGENTS.md",lambda name:None,None)


if __name__=="__main__":
    unittest.main()
