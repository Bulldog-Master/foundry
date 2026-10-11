#!/usr/bin/env python3
"""foundry-evaluator-invoke -- BOOTSTRAP-0 v0.1

One-shot evaluator invoker for the Foundry 2 review-packet contract
(operations/foundry-2/REVIEW-PACKET-SPEC-v0.1.md).  Installed root-owned (0755) and invoked as root for BOOTSTRAP-0 only, launched by the founder from the Windows side (`wsl -d Foundry-Agent -u root -- ...`).
No sudoers rule is involved. The agent user (foundry-agent) can neither read the
API credential, invoke the provider through this bootstrap path, nor write the evidence this script produces.

BOOTSTRAP-0 limits: uncommissioned code, stdlib validation only, not Foundry 2
commissioning evidence. Foundry-Agent autonomous invocation is not authorized by this bootstrap artifact. Usage: foundry-evaluator-invoke <packet_dir>
Takes exactly one argument.  No environment variables are read.  No tools and no
network are offered to the model.
"""
import datetime, hashlib, json, os, re, socket, stat, sys, urllib.error, urllib.request, uuid

ETC = "/etc/foundry-evaluator"
KEY_FILE = ETC + "/api-key"
CONFIG_FILE = ETC + "/config.json"
TASK_FILE = ETC + "/evaluator-task.md"
TERMS_FILE = ETC + "/provider-terms.json"
RUNS = "/var/lib/foundry-evaluator/runs"
API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
MAX_PACKET_BYTES = 4_000_000
TIMEOUT_S = 900

H64 = re.compile(r"^[0-9a-f]{64}$")
G40 = re.compile(r"^[0-9a-f]{40}$")
FID = re.compile(r"^FND-[A-Z]{3,4}-[0-9]{3,}$")
GATES = ("architecture", "security", "privacy", "quality")
VERDICTS = {"PASS", "FAIL", "PASS_WITH_CONDITIONS", "N/A"}
CATS = {"IMPLEMENTATION_DEFECT", "TRUST_BOUNDARY_DEFECT", "INTEGRITY_ANOMALY", "SPEC_AMBIGUITY",
        "RESERVED_ACT_REQUIRED", "EVIDENCE_MISSING", "OTHER"}
SEVS = {"CRITICAL", "MAJOR", "MINOR"}
ROUTES = {"CONTINUE", "RETURN_TO_OPERATIONS", "HARD_STOP", "ESCALATE_FOUNDER"}
ROUTING_PROFILE = "foundry-routing-v0.1-security-na-hard-stop"
MANIFEST_KEYS = {"packet_schema_version", "packet_id", "repository", "pr_number", "base_ref", "base_sha",
                 "merge_base_sha", "head_repository", "head_sha", "changed_files", "diff", "governance_profile_sha256", "governance_refs", "related_context_refs",
                 "evaluator_task", "allowed_context", "prohibited_context", "review_round",
                 "producer_identity", "completeness", "members", "packet_created_at", "packet_sha256"}


class Reject(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


def jcs(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_regular(path, require_root=False):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise Reject("not a regular file: " + path)
        if require_root and (st.st_uid != 0 or st.st_mode & 0o022):
            raise Reject("unsafe owner/mode: " + path)
        with os.fdopen(fd, "rb") as f:
            fd = -1
            return f.read(MAX_PACKET_BYTES + 1)
    finally:
        if fd != -1:
            os.close(fd)


# ---------------------------------------------------------------- packet
def load_packet(pdir):
    pdir = os.path.realpath(pdir)
    if not os.path.isdir(pdir):
        raise Reject("packet_dir is not a directory")
    pst = os.stat(pdir)
    if pst.st_uid != 0 or pst.st_mode & 0o022:
        raise Reject("packet directory is not root-controlled")
    manifest = json.loads(read_regular(os.path.join(pdir, "manifest.json"), True).decode("utf-8"))
    if not isinstance(manifest, dict) or set(manifest) != MANIFEST_KEYS:
        raise Reject("manifest keys differ from the v0.1 schema")
    if manifest["packet_schema_version"] != "0.1":
        raise Reject("unsupported packet_schema_version")
    c = manifest["completeness"]
    if c.get("complete") is not True or c.get("truncated") is not False:
        raise Reject("packet is not complete")
    body = dict(manifest)
    declared = body.pop("packet_sha256")
    if not H64.match(str(declared)) or sha(jcs(body)) != declared:
        raise Reject("packet_sha256 does not match the canonical manifest")
    if not G40.match(str(manifest["head_sha"])):
        raise Reject("bad head_sha")
    members, total = {}, 0
    listed = set()
    for m in manifest["members"]:
        name = m["name"]
        if name.startswith("/") or ".." in name.split("/") or name == "manifest.json" or name in listed:
            raise Reject("bad member name: " + name)
        listed.add(name)
        data = read_regular(os.path.join(pdir, name), True)
        total += len(data)
        if total > MAX_PACKET_BYTES:
            raise Reject("packet exceeds size limit")
        if sha(data) != m["sha256"] or len(data) != m["size"]:
            raise Reject("member hash/size mismatch: " + name)
        members[name] = data.decode("utf-8")  # strict; binary members unsupported in BOOTSTRAP-0
    on_disk = set()
    for root, dirs, files in os.walk(pdir, followlinks=False):
        for n in dirs + files:
            full = os.path.join(root, n)
            if os.path.islink(full):
                raise Reject("symlink in packet: " + full)
        for n in files:
            on_disk.add(os.path.relpath(os.path.join(root, n), pdir))
    if on_disk - listed - {"manifest.json"}:
        raise Reject("unlisted files in packet dir")
    paths = {name: (len(content.splitlines()) or 1) for name, content in members.items()}
    for cf in manifest["changed_files"]:
        if cf["status"] == "deleted":
            if "member" in cf or "head_content_sha256" in cf or "head_blob_sha" in cf:
                raise Reject("deleted file carries head content: " + cf["path"])
            continue
        if cf["member"] not in members or sha(members[cf["member"]].encode()) != cf["head_content_sha256"]:
            raise Reject("changed_file member mismatch: " + cf["path"])
    d = manifest["diff"]
    if d["member"] not in members or sha(members[d["member"]].encode()) != d["sha256"]:
        raise Reject("diff member mismatch")
    for g in manifest["governance_refs"]:
        if g["member"] not in members or sha(members[g["member"]].encode()) != g["sha256"]:
            raise Reject("governance member mismatch: " + g["path"])
    for row in manifest["related_context_refs"]:
        if row["member"] not in members or sha(members[row["member"]].encode()) != row["sha256"]:
            raise Reject("related-context member mismatch: " + row["path"])
        expected = manifest["base_sha"] if row["source"] == "base" else manifest["head_sha"]
        if row["source_sha"] != expected:
            raise Reject("related-context source mismatch: " + row["path"])
    return manifest, members, paths


# ---------------------------------------------------------------- result
def derive_routing(r):
    """Frozen routing table from spec section 8, fail-closed for uncovered cases."""
    fnd = r["findings"]
    cats = {f["category"] for f in fnd}
    if "RESERVED_ACT_REQUIRED" in cats:
        return "ESCALATE_FOUNDER", True
    if r["gates"]["security"]["verdict"] == "N/A":
        return "HARD_STOP", True
    if r["gates"]["security"]["verdict"] == "FAIL":
        return "HARD_STOP", True
    if cats & {"TRUST_BOUNDARY_DEFECT", "INTEGRITY_ANOMALY", "SPEC_AMBIGUITY", "OTHER"} or any(f["severity"] == "CRITICAL" for f in fnd):
        return "HARD_STOP", True
    if any(g["verdict"] in ("FAIL", "PASS_WITH_CONDITIONS") for g in r["gates"].values()):
        if cats <= {"IMPLEMENTATION_DEFECT", "EVIDENCE_MISSING"}:
            return "RETURN_TO_OPERATIONS", False
        return "HARD_STOP", True
    return "CONTINUE", False


def adverse_signals(r):
    if not isinstance(r, dict):
        return []
    found = set()
    hard = {"TRUST_BOUNDARY_DEFECT", "INTEGRITY_ANOMALY", "SPEC_AMBIGUITY", "RESERVED_ACT_REQUIRED", "OTHER"}
    def walk(value):
        if isinstance(value, dict):
            if value.get("verdict") == "FAIL": found.add("verdict:FAIL")
            if value.get("severity") == "CRITICAL": found.add("severity:CRITICAL")
            if value.get("category") in hard: found.add("category:" + value["category"])
            for child in value.values(): walk(child)
        elif isinstance(value, list):
            for child in value: walk(child)
    walk(r)
    return sorted(found)


def check_result(r, manifest, paths):
    """Returns (schema_validation, errors).  Empty errors => VALID."""
    errs = []
    top = {"result_schema_version", "packet_sha256", "pr_number", "head_sha", "evaluator_task_sha256", "routing_profile",
           "gates", "findings", "overall", "routing", "requires_human"}
    if not isinstance(r, dict) or set(r) != top:
        return "INVALID_MALFORMED", ["top-level keys differ from schema"]
    if r["result_schema_version"] != "0.1":
        errs.append("result_schema_version")
    if not isinstance(r["gates"], dict) or set(r["gates"]) != set(GATES):
        return "INVALID_MALFORMED", ["gates must be exactly the four gates"]
    if not isinstance(r["findings"], list):
        return "INVALID_MALFORMED", ["findings must be a list"]
    if not isinstance(r["requires_human"], bool) or r["routing"] not in ROUTES or r["overall"] not in {"PASS", "FAIL", "PASS_WITH_CONDITIONS"}:
        errs.append("overall/routing/requires_human invalid")
    listed_by = {}
    for gname, g in r["gates"].items():
        if not isinstance(g, dict) or not set(g) <= {"verdict", "finding_ids", "conditions", "na_reason"} \
                or not {"verdict", "finding_ids"} <= set(g) or g["verdict"] not in VERDICTS \
                or not isinstance(g["finding_ids"], list) or len(set(map(str, g["finding_ids"]))) != len(g["finding_ids"]) \
                or not all(isinstance(i, str) and FID.match(i) for i in g["finding_ids"]):
            errs.append("gate malformed: " + gname)
            continue
        v = g["verdict"]
        if v == "N/A" and not (isinstance(g.get("na_reason"), str) and g["na_reason"].strip()):
            errs.append("N/A needs na_reason: " + gname)
        if v == "PASS_WITH_CONDITIONS" and not (isinstance(g.get("conditions"), list) and g["conditions"] and all(isinstance(c, str) for c in g["conditions"])):
            errs.append("PASS_WITH_CONDITIONS needs conditions: " + gname)
        if v == "FAIL" and not g["finding_ids"]:
            errs.append("FAIL needs findings: " + gname)
        if v in ("PASS", "N/A") and g["finding_ids"]:
            errs.append("PASS/N-A gate must not carry findings: " + gname)
        for i in g["finding_ids"]:
            listed_by[i] = gname
    seen = set()
    for f in r["findings"]:
        need = {"finding_id", "gate", "category", "severity", "title", "evidence_refs"}
        if not isinstance(f, dict) or not need <= set(f) or not set(f) <= need | {"detail"}:
            errs.append("finding malformed")
            continue
        ok = (isinstance(f["finding_id"], str) and FID.match(f["finding_id"]) and f["gate"] in GATES
              and f["category"] in CATS and f["severity"] in SEVS and isinstance(f["title"], str)
              and 1 <= len(f["title"]) <= 200 and isinstance(f.get("detail", ""), str) and len(f.get("detail", "")) <= 4000
              and isinstance(f["evidence_refs"], list) and f["evidence_refs"])
        if not ok:
            errs.append("finding fields invalid: " + str(f.get("finding_id")))
            continue
        for e in f["evidence_refs"]:
            if not (isinstance(e, dict) and {"member", "line_start", "line_end"} <= set(e)
                    and set(e) <= {"member", "repository_path", "line_start", "line_end"} and isinstance(e["member"], str)
                    and ("repository_path" not in e or isinstance(e["repository_path"], str))
                    and all(isinstance(e[k], int) and not isinstance(e[k], bool) and e[k] >= 1 for k in ("line_start", "line_end"))):
                errs.append("evidence_ref malformed: " + f["finding_id"])
            elif e["member"] not in paths:
                errs.append("evidence member not in packet: " + e["member"])
            elif e["line_end"] < e["line_start"] or e["line_end"] > paths[e["member"]]:
                errs.append("evidence line range invalid: " + f["finding_id"])
        if f["finding_id"] in seen:
            errs.append("duplicate finding id")
        seen.add(f["finding_id"])
        if listed_by.get(f["finding_id"]) != f["gate"]:
            errs.append("finding/gate listing mismatch: " + f["finding_id"])
    if seen != set(listed_by):
        errs.append("gate finding_ids and findings differ")
    if errs:
        return "INVALID_MALFORMED", errs
    vs = [g["verdict"] for g in r["gates"].values()]
    overall = "FAIL" if "FAIL" in vs else ("PASS_WITH_CONDITIONS" if "PASS_WITH_CONDITIONS" in vs else "PASS")
    if r["overall"] != overall:
        return "INVALID_MALFORMED", ["overall inconsistent with gate verdicts"]
    bind = (r["packet_sha256"] == manifest["packet_sha256"] and r["pr_number"] == manifest["pr_number"]
            and r["head_sha"] == manifest["head_sha"] and r["evaluator_task_sha256"] == manifest["evaluator_task"]["sha256"]
            and r["routing_profile"] == ROUTING_PROFILE == manifest["evaluator_task"]["routing_profile"])
    if not bind:
        return "INVALID_BINDING_MISMATCH", ["result is not bound to this packet"]
    return "VALID", []


# ---------------------------------------------------------------- main
def main(argv):
    if len(argv) != 2:
        print("usage: foundry-evaluator-invoke <packet_dir>", file=sys.stderr)
        return 2
    try:
        manifest, members, paths = load_packet(argv[1])
        task = read_regular(TASK_FILE, True)
        if sha(task) != manifest["evaluator_task"]["sha256"]:
            raise Reject("installed evaluator task hash differs from the packet's evaluator_task.sha256")
        cfg = json.loads(read_regular(CONFIG_FILE, True).decode())
        terms = read_regular(TERMS_FILE, True)
        if (set(cfg) != {"model", "max_tokens", "effort"} or not isinstance(cfg["model"], str)
                or not isinstance(cfg["max_tokens"], int) or cfg["effort"] not in {"low", "medium", "high", "xhigh", "max"}):
            raise Reject("config.json must contain exactly model, max_tokens, and a valid effort")
        key = read_regular(KEY_FILE, True).decode().strip()
    except (Reject, ValueError, KeyError, TypeError, OSError, UnicodeDecodeError) as e:
        print("REJECTED: %s" % e, file=sys.stderr)
        return 2

    psha = manifest["packet_sha256"]
    scan_rules = {
        "PRIVATE_KEY": re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
        "ANTHROPIC_KEY": re.compile(r"sk-ant-[A-Za-z0-9_-]{16,}"),
        "GITHUB_TOKEN": re.compile(r"gh[opsu]_[A-Za-z0-9]{20,}"),
        "AWS_ACCESS_KEY": re.compile(r"AKIA[0-9A-Z]{16}"),
    }
    disclosure_matches = sorted({rule for content in members.values() for rule, pattern in scan_rules.items() if pattern.search(content)})
    if disclosure_matches:
        print("REJECTED: pre-transmission disclosure scan blocked: %s" % ",".join(disclosure_matches), file=sys.stderr)
        return 2
    disclosure = {
        "scanner_sha256": sha(b"foundry-bootstrap0-disclosure-scanner-v0.1" + read_regular(os.path.realpath(sys.argv[0]), True)),
        "packet_sha256": psha,
        "repository_visibility": "PUBLIC",
        "fork_visibility": "NOT_A_FORK",
        "members_scanned": len(members) + 1,
        "bytes_scanned": sum(len(v.encode("utf-8")) for v in members.values()) + len(jcs(manifest)),
        "scan_outcome": "CLEAN",
        "matched_rule_ids": [],
        "provider_terms_sha256": sha(terms),
        "founder_decision_sha256": None,
    }
    run_dir = os.path.join(RUNS, psha)
    os.makedirs(run_dir, mode=0o700, exist_ok=True)
    os.chmod(run_dir, 0o700)
    attempts, prior_invocation_id = {}, None
    for n in (1, 2):
        rec = os.path.join(run_dir, "attempt-%d" % n, "invocation-record.json")
        if os.path.exists(rec):
            j = json.loads(open(rec, "rb").read())
            attempts[n] = (j["schema_validation"] == "VALID" and j["routing_check"] == "MATCHES_TABLE")
            if n == 1: prior_invocation_id = j["invocation_id"]
        elif os.path.isdir(os.path.dirname(rec)):
            attempts[n] = False
    if os.path.exists(os.path.join(run_dir, "attempt-1", "adverse-signal.json")):
        print("REFUSED: invalid attempt 1 contained an adverse signal; this packet is a HARD_STOP", file=sys.stderr)
        return 4
    if 1 not in attempts:
        attempt = 1
    elif attempts[1]:
        print("REFUSED: a valid evaluation already exists for this packet; valid results are never re-run", file=sys.stderr)
        return 4
    elif 2 not in attempts:
        attempt = 2
    else:
        print("REFUSED: both attempts used; this packet is a HARD_STOP", file=sys.stderr)
        return 4
    adir = os.path.join(run_dir, "attempt-%d" % attempt)
    os.mkdir(adir, 0o700)

    user_content = json.dumps({"manifest": manifest, "members": members}, ensure_ascii=False)
    body = {"model": cfg["model"], "max_tokens": cfg["max_tokens"], "system": task.decode("utf-8"),
            "messages": [{"role": "user", "content": user_content}],
            "output_config": {"effort": cfg["effort"]}}
    started = now()
    req = urllib.request.Request(API_URL, data=json.dumps(body).encode("utf-8"), method="POST", headers={
        "x-api-key": key, "anthropic-version": API_VERSION, "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            raw = resp.read()
            request_id = resp.headers.get("request-id", "")
    except urllib.error.HTTPError as e:
        os.rmdir(adir)  # transport failure does not consume an attempt
        print("TRANSPORT ERROR: HTTP %s" % e.code, file=sys.stderr)
        return 3
    except Exception as e:
        os.rmdir(adir)
        print("TRANSPORT ERROR: %s" % type(e).__name__, file=sys.stderr)
        return 3
    completed = now()

    def put(name, data):
        with open(os.path.join(adir, name), "xb", opener=lambda p, flags: os.open(p, flags, 0o600)) as f:
            f.write(data)

    put("raw-response.json", raw)
    put("request-meta.json", jcs({"model": cfg["model"], "max_tokens": cfg["max_tokens"],
                                  "effort": cfg["effort"], "system_prompt_sha256": sha(task),
                                  "user_content_sha256": sha(user_content.encode())}))
    observed_model, validation, errors, result, routing_check = cfg["model"], "INVALID_MALFORMED", [], None, "NOT_APPLICABLE"
    try:
        api = json.loads(raw.decode("utf-8"))
        observed_model = api.get("model", observed_model)
        text = "".join(b.get("text", "") for b in api["content"] if b.get("type") == "text")
        if api.get("stop_reason") != "end_turn":
            errors.append("stop_reason is %r, output may be truncated" % api.get("stop_reason"))
        else:
            result = json.loads(text.strip())
            validation, errors = check_result(result, manifest, paths)
    except Exception as e:
        errors.append("unparseable response: %s" % type(e).__name__)
    if validation == "VALID":
        route, human = derive_routing(result)
        routing_check = "MATCHES_TABLE" if (result["routing"] == route and result["requires_human"] == human) else "MISMATCH"
    signals = adverse_signals(result)
    adverse = not (validation == "VALID" and routing_check == "MATCHES_TABLE") and bool(signals)
    if adverse:
        put("adverse-signal.json", jcs({"hard_stop":True,"signals":signals,"raw_output_sha256":sha(raw)}))
    result_sha = None
    if validation == "VALID":
        result_sha = sha(jcs(result))
        put("result.json", jcs(result))
    rec = {
        "record_schema_version": "0.1", "invocation_id": str(uuid.uuid4()),
        "packet_sha256": psha, "raw_output_sha256": sha(raw), "raw_output_bytes": len(raw),
        "transport_outcome": "COMPLETED",
        "result_sha256": result_sha,
        "evaluator": {"provider": "anthropic", "model_id": observed_model, "config_sha256": sha(jcs(cfg)),
                      "system_prompt_sha256": sha(task)},
        "environment": {"session_id": request_id or "none", "runtime_image_sha256": sha(read_regular(os.path.realpath(sys.argv[0]), True) + sys.version.encode()),
                        "host_id": socket.gethostname()},
        "accessible_context": ["packet_manifest", "packet_members", "evaluator_task"], "tools_available": [], "network_policy": "none",
        "credentials_present": [],
        "prior_exposure": {"known_prior_sessions_on_this_pr": [],
                           "knowable_limits": "Stateless API call with no conversation history supplied; "
                                              "prior training exposure to repository content is not knowable."},
        "attempt": attempt, "started_at": started, "completed_at": completed,
        "schema_validation": validation, "routing_check": routing_check,
        "adverse_signal_scan": {"algorithm_version": "0.1", "outcome": "ADVERSE" if adverse else "NONE",
                                "matched_signals": signals if adverse else []},
        "pre_transmission_disclosure": disclosure,
    }
    rec["review_record_sha256"] = sha(jcs({"packet_sha256": psha, "result_sha256": result_sha,
                                           "invocation_record_without_hash": rec}))
    put("validation-errors.json", jcs(errors))
    put("invocation-record.json", jcs(rec))
    ok = validation == "VALID" and routing_check == "MATCHES_TABLE"
    print(json.dumps({"packet_sha256": psha, "attempt": attempt, "schema_validation": validation,
                      "routing_check": routing_check, "overall": result["overall"] if ok else None,
                      "routing": result["routing"] if ok else None, "errors": errors[:5],
                      "review_record_sha256": rec["review_record_sha256"], "run_dir": adir}, indent=2))
    return 4 if adverse else (0 if ok else 5)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
