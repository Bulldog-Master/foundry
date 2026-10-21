"""One deterministic Stage B pass; inert unless explicitly invoked after freeze."""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import pwd
import signal
import sys
import time
import unittest


FILES = ("PROTOCOL-v0.1.md", "CA-001-deterministic-rule-promotion.md",
         "CA-001-EVALUATION-PACKET-v1.md", "ca001_checker.py",
         "fixtures/ca001-v1.jsonl", "test_ca001_checker.py", "ca001_harness.py")
WORKDIR = "/home/foundry-agent/work/candidate-admission/ca001-v1"


class IntegrityError(ValueError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise IntegrityError("duplicate JSON key")
        result[key] = value
    return result


def decode(data):
    def invalid_constant(value):
        raise IntegrityError("non-JSON constant")
    try:
        return json.loads(data, object_pairs_hook=unique_object,
                          parse_constant=invalid_constant)
    except (ValueError, UnicodeError, RecursionError) as error:
        raise IntegrityError("invalid JSON") from error


def load_cases(data):
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeError as error:
        raise IntegrityError("fixture is not UTF-8") from error
    if len(lines) != 12 or any(not line.strip() for line in lines):
        raise IntegrityError("expected twelve nonblank fixture lines")
    cases = [decode(line) for line in lines]
    ids = set()
    for case in cases:
        if (not isinstance(case, dict) or set(case) != {
                "case_id", "requested_action", "authorization", "expected_result"}
                or not isinstance(case["case_id"], str) or not case["case_id"]
                or case["case_id"] in ids
                or case["expected_result"] not in ("eligible-for-human-review", "stop")):
            raise IntegrityError("invalid frozen fixture structure")
        ids.add(case["case_id"])
    return cases


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def run_checks(check, test_suite, cases):
    """No clocks or traceback paths in the comparison stream."""
    result = unittest.TestResult()
    test_suite.run(result)
    tests_ok = (result.testsRun == 8 and result.wasSuccessful()
                and not result.skipped and not result.expectedFailures
                and not result.unexpectedSuccesses)
    rows = []
    for case in cases:
        # Expected values belong to this harness, never to the candidate input.
        value = check({"requested_action": case["requested_action"],
                       "authorization": case["authorization"]})
        if not isinstance(value, str) or value not in ("stop", "eligible-for-human-review"):
            raise IntegrityError("candidate returned an invalid result")
        rows.append({"case_id": case["case_id"], "result": value,
                     "matches_expected": value == case["expected_result"]})
    success = tests_ok and all(row["matches_expected"] for row in rows)
    report = {"cases": rows, "tests_run": result.testsRun, "tests_ok": tests_ok,
              "failures": len(result.failures), "errors": len(result.errors),
              "failed_test_ids": sorted(test.id() for test, _ in result.failures + result.errors),
              "skipped": len(result.skipped), "all_expected_results": success}
    return canonical(report), 0 if success else 1


class RejectOutput(io.TextIOBase):
    def write(self, value):
        if value:
            raise IntegrityError("unexpected candidate or test output")
        return 0


def source_snapshot(root, expected):
    if not isinstance(expected, dict) or set(expected) != set(FILES):
        raise IntegrityError("unexpected source inventory")
    result = {}
    for name in FILES:
        path = root / name
        if (path.is_symlink() or not path.is_file()
                or root not in path.resolve().parents or path.stat().st_size > 65536):
            raise IntegrityError("source path is not a contained regular file")
        value = path.read_bytes()
        if digest(value) != expected[name]:
            raise IntegrityError("source hash mismatch")
        result[name] = value
    return result


def execute_pass(manifest, deadline):
    root = Path(__file__).resolve().parent
    if (root != Path(WORKDIR) or Path.cwd().resolve() != root
            or os.geteuid() != 1000 or pwd.getpwuid(os.geteuid()).pw_name != "foundry-agent"
            or not sys.dont_write_bytecode
            or not sys.flags.isolated):
        raise IntegrityError("wrong execution boundary")
    remaining = deadline - time.time()
    if not 0 < remaining <= 60:
        raise IntegrityError("expired or oversized pass deadline")
    # A lost Windows client cannot leave this no-subprocess worker running forever.
    signal.signal(signal.SIGALRM, lambda *_: os._exit(124))
    signal.setitimer(signal.ITIMER_REAL, remaining)
    runtime = manifest["runtime"]
    executable = Path(sys.executable).resolve()
    if (set(runtime) != {"path", "sha256", "version"}
            or str(executable) != runtime["path"]
            or digest(executable.read_bytes()) != runtime["sha256"]
            or sys.version != runtime["version"]):
        raise IntegrityError("runtime mismatch")
    sources = source_snapshot(root, manifest["sources"])
    cases = load_cases(sources["fixtures/ca001-v1.jsonl"])
    with contextlib.redirect_stdout(RejectOutput()), contextlib.redirect_stderr(RejectOutput()):
        modules = []
        for name in ("ca001_checker", "test_ca001_checker"):
            spec = importlib.util.spec_from_file_location(name, root / (name + ".py"))
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            exec(compile(sources[name + ".py"], str(root / (name + ".py")), "exec"),
                 module.__dict__)
            modules.append(module)
        suite = unittest.defaultTestLoader.loadTestsFromModule(modules[1])
        output, code = run_checks(modules[0].check_action, suite, cases)
    source_snapshot(root, manifest["sources"])
    return output, code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--manifest-sha256")
    parser.add_argument("--deadline-utc", type=float)
    args = parser.parse_args()
    if not args.execute:
        parser.error("execution disabled; separate frozen Stage B authorization required")
    try:
        raw = sys.stdin.buffer.read(65537)
        if len(raw) > 65536 or digest(raw) != args.manifest_sha256:
            raise IntegrityError("manifest hash/size mismatch")
        manifest = decode(raw)
        if (not isinstance(manifest, dict) or manifest.get("schema") != "ca001-stage-b-v1"
                or args.deadline_utc is None):
            raise IntegrityError("missing frozen manifest or deadline")
        output, code = execute_pass(manifest, args.deadline_utc)
    except Exception:
        output, code = canonical({"error": "integrity-or-harness-failure"}), 2
    sys.stdout.buffer.write(output)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
