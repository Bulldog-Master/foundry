#!/usr/bin/env python3
import copy
import datetime
import hashlib
import json
import pathlib
import re
import sys

from jsonschema import Draft202012Validator, FormatChecker

ROOT = pathlib.Path(__file__).resolve().parent
V = json.loads((ROOT / "CONFORMANCE-VECTORS-v0.1.json").read_text())
ALLOWED_CONTEXT = ["packet_manifest", "packet_members", "evaluator_task"]
GATE_PREFIX = {"architecture": "ARCH", "security": "SEC", "privacy": "PRIV", "quality": "QUAL"}
HARD_CATEGORIES = {"TRUST_BOUNDARY_DEFECT", "INTEGRITY_ANOMALY", "SPEC_AMBIGUITY", "OTHER"}
FORMAT_CHECKER = FormatChecker()
RFC3339 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")


@FORMAT_CHECKER.checks("date-time", raises=(TypeError, ValueError))
def valid_datetime(value):
    if not isinstance(value, str) or not RFC3339.fullmatch(value):
        return False
    parsed = datetime.datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    return parsed.tzinfo is not None


def canon(value):
    def reject_surrogates(item):
        if isinstance(item, str):
            assert not any(0xD800 <= ord(ch) <= 0xDFFF for ch in item), "lone surrogate"
        elif isinstance(item, list):
            for child in item:
                reject_surrogates(child)
        elif isinstance(item, dict):
            for key, child in item.items():
                reject_surrogates(key)
                reject_surrogates(child)
        elif isinstance(item, int):
            assert -(2**53) + 1 <= item <= (2**53) - 1, "integer outside safe range"
        else:
            assert item is None or isinstance(item, bool), "unsupported JSON number"
    reject_surrogates(value)
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
    if cats & HARD_CATEGORIES or "CRITICAL" in sevs:
        return ["HARD_STOP", True]
    if cats or sevs or x["other_gates"]:
        return ["RETURN_TO_OPERATIONS", False]
    return ["CONTINUE", False]


def semantic_result(instance):
    verdicts = [gate["verdict"] for gate in instance["gates"].values()]
    if overall(verdicts) != instance["overall"]:
        return "INVALID_DERIVED_OVERALL"
    indexed = [fid for gate in instance["gates"].values() for fid in gate["finding_ids"]]
    actual = [finding["finding_id"] for finding in instance["findings"]]
    if len(actual) != len(set(actual)) or len(indexed) != len(set(indexed)) or sorted(indexed) != sorted(actual):
        return "INVALID_FINDING_INDEX"
    findings = {finding["finding_id"]: finding for finding in instance["findings"]}
    for gate_name, gate in instance["gates"].items():
        for finding_id in gate["finding_ids"]:
            finding = findings[finding_id]
            if finding["gate"] != gate_name or not finding_id.startswith("FND-" + GATE_PREFIX[gate_name] + "-"):
                return "INVALID_FINDING_INDEX"
        if gate["verdict"] == "FAIL" and not gate["finding_ids"]:
            return "INVALID_FINDING_INDEX"
        if gate["verdict"] in ("PASS", "N/A") and gate["finding_ids"]:
            return "INVALID_FINDING_INDEX"
    for finding in instance["findings"]:
        for ref in finding["evidence_refs"]:
            if ref["line_end"] < ref["line_start"]:
                return "INVALID_EVIDENCE_REF"
    route_input = {
        "categories": [finding["category"] for finding in instance["findings"]],
        "severities": [finding["severity"] for finding in instance["findings"]],
        "security": instance["gates"]["security"]["verdict"],
        "other_gates": [gate["verdict"] for gate in instance["gates"].values()
                        if gate["verdict"] == "PASS_WITH_CONDITIONS"]
                       + [gate["verdict"] for name, gate in instance["gates"].items()
                          if name != "security" and gate["verdict"] == "FAIL"],
    }
    expected_route, expected_human = routing(route_input)
    if [instance["routing"], instance["requires_human"]] != [expected_route, expected_human]:
        return "INVALID_ROUTING"
    return "VALID"


def semantic_invocation(instance):
    if (instance["accessible_context"] != ALLOWED_CONTEXT or instance["tools_available"]
            or instance["credentials_present"] or instance["network_policy"] != "none"):
        return "INVALID_CONTEXT"
    if instance["pre_transmission_disclosure"]["packet_sha256"] != instance["packet_sha256"]:
        return "INVALID_BINDING_MISMATCH"
    disclosure = instance["pre_transmission_disclosure"]
    private = disclosure["repository_visibility"] != "PUBLIC" or disclosure["fork_visibility"] == "PRIVATE"
    if not disclosure["provider_terms_accepted"]:
        return "INVALID_OTHER"
    if disclosure["scan_outcome"] == "CLEAN" and private and disclosure["founder_decision_sha256"] is None:
        return "INVALID_OTHER"
    if disclosure["scan_outcome"] == "BLOCKED":
        return "INVALID_OTHER"
    if instance["raw_output_bytes"] == 0 and instance["raw_output_sha256"] is not None:
        return "INVALID_OTHER"
    if instance["raw_output_bytes"] > 0 and instance["raw_output_sha256"] is None:
        return "INVALID_OTHER"
    if (instance["schema_validation"] == "VALID") != (instance["result_sha256"] is not None):
        return "INVALID_OTHER"
    return "VALID"


def semantic_case(schema_name, instance):
    if schema_name == "review-result.schema.json":
        return semantic_result(instance)
    if schema_name == "invocation-record.schema.json":
        return semantic_invocation(instance)
    return "VALID"


def adverse_signals(raw):
    duplicates = False

    def unique_pairs(pairs):
        nonlocal duplicates
        out = {}
        for key, value in pairs:
            if key in out:
                duplicates = True
            out[key] = value
        return out

    try:
        text = raw.decode("utf-8", errors="strict")
        value = json.loads(text, object_pairs_hook=unique_pairs,
                           parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return "INDETERMINATE", []
    if duplicates or not isinstance(value, dict):
        return "INDETERMINATE", []
    found = set()

    def walk(item):
        if isinstance(item, dict):
            if item.get("verdict") == "FAIL":
                found.add("verdict:FAIL")
            if item.get("severity") == "CRITICAL":
                found.add("severity:CRITICAL")
            category = item.get("category")
            if category in HARD_CATEGORIES | {"RESERVED_ACT_REQUIRED"}:
                found.add("category:" + category)
            for child in item.values():
                walk(child)
        elif isinstance(item, list):
            for child in item:
                walk(child)

    walk(value)
    return ("ADVERSE" if found else "NONE"), sorted(found)


def controller(case):
    x = case["input"]
    if "raw_output" in x:
        outcome, signals = adverse_signals(x["raw_output"].encode("utf-8"))
        if x["attempt"] == 2 or outcome != "NONE" or signals:
            return "HARD_STOP"
        return "RETRY_IDENTICAL"
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
    if "indexed_findings" in x:
        return "INVALID_FINDING_INDEX" if sorted(x["indexed_findings"]) != sorted(x["actual_findings"]) else "VALID"
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

    def instance_for(case):
        if "instance" in case:
            return copy.deepcopy(case["instance"])
        return patch(instance_for(by_id[case["mutation_of"]]), case["patch"])

    for vector in V["canonical_json_vectors"]:
        data = canon(vector["input"])
        assert data.decode("utf-8") == vector["canonical_utf8"], vector
        assert hashlib.sha256(data).hexdigest() == vector["sha256"], vector

    literal = V["canonical_json_vectors"][0]["canonical_utf8"].encode("utf-8")
    assert V["hash_provenance"][0]["expected"] == hashlib.sha256(literal).hexdigest()
    if len(sys.argv) > 1 and sys.argv[1] == "--hash-only":
        print(hashlib.sha256(literal).hexdigest())
        return

    for case in V["schema_cases"]:
        instance = instance_for(case)
        schema = json.loads((ROOT / "schemas" / case["schema"]).read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema, format_checker=FORMAT_CHECKER).iter_errors(instance))
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
