#!/usr/bin/env python3
import copy
import hashlib
import json
import pathlib
import subprocess
import sys

from jsonschema import Draft202012Validator, FormatChecker

ROOT = pathlib.Path(__file__).resolve().parent
V = json.loads((ROOT / "CONFORMANCE-VECTORS-v0.1.json").read_text())
ALLOWED_CONTEXT = ["packet_manifest", "packet_members", "evaluator_task"]


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def patch(value, operations):
    out = copy.deepcopy(value)
    for op in operations:
        parts = [p.replace("~1", "/").replace("~0", "~") for p in op["path"].split("/")[1:]]
        parent = out
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        key = int(parts[-1]) if isinstance(parent, list) else parts[-1]
        if op["op"] == "add" and isinstance(parent, list):
            parent.insert(key, op["value"])
        elif op["op"] in ("add", "replace"):
            parent[key] = op["value"]
        else:
            raise AssertionError("unsupported patch op")
    return out


def overall(verdicts):
    if "FAIL" in verdicts:
        return "FAIL"
    if "PASS_WITH_CONDITIONS" in verdicts:
        return "PASS_WITH_CONDITIONS"
    return "PASS"


def routing(x):
    cats, sevs = set(x["categories"]), set(x["severities"])
    if "RESERVED_ACT_REQUIRED" in cats:
        return ["ESCALATE_FOUNDER", True]
    if x["security"] in ("FAIL", "N/A"):
        return ["HARD_STOP", True]
    if cats & {"TRUST_BOUNDARY_DEFECT", "INTEGRITY_ANOMALY", "SPEC_AMBIGUITY", "OTHER"} or "CRITICAL" in sevs:
        return ["HARD_STOP", True]
    if x["other_gates"]:
        return ["RETURN_TO_OPERATIONS", False]
    return ["CONTINUE", False]


def semantic_result(instance):
    verdicts = [gate["verdict"] for gate in instance["gates"].values()]
    if overall(verdicts) != instance["overall"]:
        return "INVALID_DERIVED_OVERALL"
    indexed = [fid for gate in instance["gates"].values() for fid in gate["finding_ids"]]
    actual = [finding["finding_id"] for finding in instance["findings"]]
    if len(indexed) != len(set(indexed)) or sorted(indexed) != sorted(actual):
        return "INVALID_FINDING_INDEX"
    return "VALID"


def semantic_invocation(instance):
    if (instance["accessible_context"] != ALLOWED_CONTEXT or instance["tools_available"]
            or instance["credentials_present"] or instance["network_policy"] != "none"):
        return "INVALID_CONTEXT"
    if instance["schema_validation"] != "VALID" and not instance["raw_output_sha256"]:
        return "INVALID_OTHER"
    return "VALID"


def semantic_case(schema_name, instance):
    if schema_name == "review-result.schema.json":
        return semantic_result(instance)
    if schema_name == "invocation-record.schema.json":
        return semantic_invocation(instance)
    return "VALID"


def controller(case):
    x = case["input"]
    if "gate_verdicts" in x:
        return "INVALID_DERIVED_OVERALL" if overall(x["gate_verdicts"]) != x["reported_overall"] else "VALID"
    if "packet_head" in x and "result_head" in x:
        return "INVALID_BINDING_MISMATCH" if x["packet_head"] != x["result_head"] else "VALID"
    if "declared" in x and "observed" in x:
        return "INVALID_MEMBER_CROSS_REFERENCE" if x["declared"] != x["observed"] else "VALID"
    if "evidence_member" in x:
        return "INVALID_EVIDENCE_REF" if x["evidence_member"] not in x["members"] else "VALID"
    if "allowed" in x:
        return "INVALID_CONTEXT" if x["allowed"] != x["observed"] else "VALID"
    if "derived" in x:
        return "INVALID_ROUTING" if x["derived"] != x["reported"] else "VALID"
    if "named_rule" in x:
        return "INVALID_OTHER"
    if "schema_validation" in x:
        assert x["schema_validation"] != "VALID" and x["raw_output_sha256"] and x["result_sha256"] is None
        return "INVALID_OUTPUT_RETAINED"
    if "current_head" in x:
        return "RESEAL_NO_PUBLICATION" if x["packet_head"] != x["current_head"] else "VALID"
    if x["attempt"] == 2 or x["parseable_adverse_signals"]:
        return "HARD_STOP"
    return "RETRY_IDENTICAL"


def main():
    by_id = {case["id"]: case for case in V["schema_cases"]}
    for vector in V["canonical_json_vectors"]:
        data = canon(vector["input"])
        assert data.decode("utf-8") == vector["canonical_utf8"], vector
        assert hashlib.sha256(data).hexdigest() == vector["sha256"], vector

    literal = V["canonical_json_vectors"][0]["canonical_utf8"].encode("utf-8")
    external_digest = subprocess.check_output(["sha256sum"], input=literal).decode().split()[0]
    assert external_digest == V["hash_provenance"][1]["expected"] == hashlib.sha256(literal).hexdigest()
    if len(sys.argv) > 1 and sys.argv[1] == "--hash-only":
        print(hashlib.sha256(literal).hexdigest())
        return

    for case in V["schema_cases"]:
        instance = case.get("instance")
        if instance is None:
            instance = patch(by_id[case["mutation_of"]]["instance"], case["patch"])
        schema = json.loads((ROOT / "schemas" / case["schema"]).read_text())
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance))
        if case["expected"] == "VALID":
            assert not errors and semantic_case(case["schema"], instance) == "VALID", case["id"]
        elif case["expected"] == "INVALID_MALFORMED":
            assert errors, case["id"]
        else:
            # A semantic invariant may also be encoded directly in the schema.
            # The named controller classification must still be derived from the instance.
            assert semantic_case(case["schema"], instance) == case["expected"], case["id"]

    for case in V["controller_cases"]:
        assert controller(case) == case["expected"], case["id"]
    for case in V["routing_cases"]:
        assert routing(case["input"]) == case["expected"], case
    print("PASS conformance-v0.1")


if __name__ == "__main__":
    main()
