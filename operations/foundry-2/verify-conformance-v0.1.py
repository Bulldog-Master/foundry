#!/usr/bin/env python3
import copy, hashlib, json, pathlib, subprocess, sys
from jsonschema import Draft202012Validator, ValidationError

ROOT = pathlib.Path(__file__).resolve().parent
V = json.loads((ROOT / "CONFORMANCE-VECTORS-v0.1.json").read_text())

def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def patch(value, operations):
    out = copy.deepcopy(value)
    for op in operations:
        parts = [p.replace("~1", "/").replace("~0", "~") for p in op["path"].split("/")[1:]]
        parent = out
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        key = int(parts[-1]) if isinstance(parent, list) else parts[-1]
        if op["op"] in ("add", "replace"):
            parent[key] = op["value"]
        else:
            raise AssertionError("unsupported patch op")
    return out

def overall(verdicts):
    if "FAIL" in verdicts: return "FAIL"
    if "PASS_WITH_CONDITIONS" in verdicts: return "PASS_WITH_CONDITIONS"
    return "PASS"

def routing(x):
    cats, sevs = set(x["categories"]), set(x["severities"])
    if "RESERVED_ACT_REQUIRED" in cats: return ["ESCALATE_FOUNDER", True]
    if x["security"] == "FAIL": return ["HARD_STOP", True]
    if cats & {"TRUST_BOUNDARY_DEFECT", "INTEGRITY_ANOMALY", "SPEC_AMBIGUITY", "OTHER"} or "CRITICAL" in sevs:
        return ["HARD_STOP", True]
    if x["other_gates"]: return ["RETURN_TO_OPERATIONS", False]
    return ["CONTINUE", False]

def controller(case):
    x, cid = case["input"], case["id"]
    if cid == "derived-overall-mismatch": return "INVALID_DERIVED_OVERALL" if overall(x["gate_verdicts"]) != x["reported_overall"] else "VALID"
    if cid == "binding-mismatch": return "INVALID_BINDING_MISMATCH" if x["packet_head"] != x["result_head"] else "VALID"
    if cid == "member-hash-mismatch": return "INVALID_MEMBER_CROSS_REFERENCE" if x["declared"] != x["observed"] else "VALID"
    if cid == "evidence-member-missing": return "INVALID_EVIDENCE_REF" if x["evidence_member"] not in x["members"] else "VALID"
    if cid == "context-mismatch": return "INVALID_CONTEXT" if x["allowed"] != x["observed"] else "VALID"
    if cid == "routing-mismatch": return "INVALID_ROUTING" if x["derived"] != x["reported"] else "VALID"
    if cid == "other-invalidity": return "INVALID_OTHER"
    if cid == "stale-head": return "RESEAL_NO_PUBLICATION" if x["packet_head"] != x["current_head"] else "VALID"
    if x["attempt"] == 2 or x["parseable_adverse_signals"]: return "HARD_STOP"
    return "RETRY_IDENTICAL"

def main():
    by_id = {c["id"]: c for c in V["schema_cases"]}
    for vector in V["canonical_json_vectors"]:
        data = canon(vector["input"])
        assert data.decode() == vector["canonical_utf8"]
        assert hashlib.sha256(data).hexdigest() == vector["sha256"]
    first = V["canonical_json_vectors"][0]["canonical_utf8"].encode()
    coreutils = subprocess.check_output(["sha256sum"], input=first).decode().split()[0]
    assert coreutils == V["hash_provenance"][1]["expected"] == hashlib.sha256(first).hexdigest()
    if len(sys.argv) > 1 and sys.argv[1] == "--hash-only":
        print(hashlib.sha256(first).hexdigest()); return
    for case in V["schema_cases"]:
        instance = case.get("instance")
        if instance is None:
            instance = patch(by_id[case["mutation_of"]]["instance"], case["patch"])
        schema = json.loads((ROOT / "schemas" / case["schema"]).read_text())
        try:
            Draft202012Validator(schema).validate(instance); schema_valid = True
        except ValidationError:
            schema_valid = False
        if case["expected"] == "VALID": assert schema_valid, case["id"]
        elif case["expected"] == "INVALID_MALFORMED": assert not schema_valid, case["id"]
        elif case["id"] == "result-invalid-pass-with-finding":
            assert schema_valid and overall([g["verdict"] for g in instance["gates"].values()]) != instance["overall"]
        elif case["id"] == "invocation-records-widening":
            assert schema_valid and (instance["network_policy"] != "none" or instance["tools_available"] or instance["credentials_present"])
    for case in V["controller_cases"]: assert controller(case) == case["expected"], case["id"]
    for case in V["routing_cases"]: assert routing(case["input"]) == case["expected"]
    print("PASS conformance-v0.1")

if __name__ == "__main__": main()
