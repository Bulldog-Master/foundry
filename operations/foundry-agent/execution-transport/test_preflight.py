import pathlib
import tempfile
import unittest
from preflight import inspect, write_record


class PreflightTests(unittest.TestCase):
    def test_commissioned_actor(self):
        with tempfile.TemporaryDirectory() as temp:
            work=pathlib.Path(temp)
            contract=work/"AGENTS.md"
            contract.write_text("test fixture")
            result=inspect(1000,work,contract,lambda name:"/fixture/codex",None,expected_owner_uid=work.stat().st_uid)
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
                inspect(1000,path,path/"AGENTS.md",lambda name:None,None,expected_owner_uid=path.stat().st_uid)


class OutputTests(unittest.TestCase):
    def test_new_record_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            work = pathlib.Path(temp)
            output = work / "record.json"
            write_record(output, "fixture\n", work)
            self.assertEqual(output.read_text(), "fixture\n")
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)
            with self.assertRaises(OSError):
                write_record(output, "replacement", work)
            self.assertEqual(output.read_text(), "fixture\n")

    def test_reject_traversal_and_outside_path(self):
        with tempfile.TemporaryDirectory() as temp:
            work = pathlib.Path(temp)
            for output in (work / ".." / "escape.json", work.parent / "escape.json"):
                with self.assertRaises(RuntimeError):
                    write_record(output, "fixture", work)

    def test_reject_symlink_parent_and_leaf(self):
        with tempfile.TemporaryDirectory() as temp:
            work = pathlib.Path(temp)
            (work / "real").mkdir()
            (work / "link").symlink_to(work / "real", target_is_directory=True)
            (work / "leaf").symlink_to(work / "real" / "record.json")
            for output in (work / "link" / "record.json", work / "leaf"):
                with self.assertRaises(OSError):
                    write_record(output, "fixture", work)
            self.assertFalse((work / "real" / "record.json").exists())


if __name__=="__main__":
    unittest.main()
