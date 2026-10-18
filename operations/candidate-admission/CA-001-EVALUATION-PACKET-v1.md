# CA-001 Evaluation Packet v1 — deterministic-rule promotion

- Type: bounded operational evaluation packet
- Protocol: Candidate Admission Protocol v0.1
- Candidate: CA-001 deterministic-rule promotion
- Status: DRAFT — not frozen, not authorized for implementation or execution
- Production impact: none
- Integration authority: none
- Merge/signing/provider/sealed-truth authority: none

## 1. Exact candidate behavior

Implement one pure Python checker with no networking, subprocess execution,
persistence, GitHub access, credentials, model calls, or external dependencies.

Proposed repository path:

`operations/candidate-admission/ca001_checker.py`

The checker exposes a pure function over one decoded object and reads only
`requested_action` and `authorization`. A separate harness reads the JSONL
file, passes each object, and compares the result with `expected_result`.
The checker never reads `expected_result`. It returns exactly one of:

- `eligible-for-human-review`
- `stop`

Recognized requested actions are exactly:

- `commit`
- `push`
- `pr-create`
- `pr-update`
- `merge`

Eligibility is returned only when all of the following are true:

1. `requested_action` is a string (not a list, object, number, boolean or null)
   in the recognized set;
2. `authorization.kind == "explicit-action"`;
3. `authorization.action` is a string (not a list, object, number, boolean or
   null) in the recognized set;
4. `authorization.action == requested_action`.

Everything else returns `stop`. A non-object case or authorization returns
`stop`; the checker must not raise. Scope expansion represented by a composite
`requested_action` is rejected by rule 1, not an additional policy predicate.

The checker does not infer intent from prose and does not authenticate whether a
real founder authorization occurred. Its output is advisory eligibility only.

## 2. Frozen fixture encoding

Proposed fixture file:

`operations/candidate-admission/fixtures/ca001-v1.jsonl`

Each line is one JSON object with exactly:

- `case_id`
- `requested_action`
- `authorization`
- `expected_result`

`authorization` uses one of these schemas:

- explicit: `{"kind":"explicit-action","action":"commit"}`
- none: `{"kind":"none"}`
- generic: `{"kind":"generic","instruction_id":"proceed"}`

The generic form deliberately carries an identifier rather than free prose.
The checker does not interpret `instruction_id`.

The 12 cases and expected outcomes remain exactly those in
`CA-001-deterministic-rule-promotion.md`.

Malformed-action coverage uses a non-string `requested_action`, so every
fixture retains exactly the four fields above.
The scope-expansion fixture uses a non-scalar composite request and must return
`stop`.

## 3. Proposed implementation artifacts

Candidate artifacts to be created only after the separate Stage A implementation
authorization described in §10:

- `operations/candidate-admission/ca001_checker.py`
- `operations/candidate-admission/fixtures/ca001-v1.jsonl`
- `operations/candidate-admission/test_ca001_checker.py`

No service, hook, workflow, GitHub App, bot, daemon, or standing invocation is
part of CA-001.

## 4. Evaluation environment

Proposed execution environment:

- host role: dedicated `Foundry-Agent` WSL execution environment;
- disposable working directory:
  `/home/foundry-agent/work/candidate-admission/ca001-v1`;
- execution identity: unprivileged `foundry-agent`;
- runtime: system `python3`, exact version captured and frozen before execution;
- dependencies: Python standard library only;
- network use: prohibited by the packet and absent from candidate code;
- provider/model calls: prohibited;
- credentials/signing/sealed truth: prohibited;
- production hosts: prohibited.

The evaluation does not use Caller-1 or Sandbox-1 Production Baseline v1.

## 5. Controller and evidence custody

The Foundry controller environment is the proposed evidence custodian.

The proposed evidence location is an evidence root outside the agent's writable
domain, designated by Bulldog at freeze. Its concrete path is OPEN.

This packet designates no trust root and does not relocate the controller or
Caller signing trust root.

This packet does not establish custody. Hashes detect change and do not
establish custody or isolation. Capture mechanism, location and host-level
verification are OPEN (`EVIDENCE_MISSING`). The `Foundry-Agent` environment is
not a trust root.

Before execution the controller must retain, hash, and freeze:

- protocol source and SHA-256;
- CA-001 trial-plan source and SHA-256;
- candidate source and SHA-256;
- fixture source and SHA-256;
- test source and SHA-256;
- exact Python version;
- exact commands;
- environment facts relevant to the trial;
- this evaluation packet and SHA-256.

The governed execution account must not be able to alter the controller-side
frozen manifest or captured authoritative transcript/evidence.

All attempts, including failed, timed-out, malformed, or aborted attempts, are
retained.

## 6. Exact commands and bounds

After freeze and Stage B authorization, the controller invokes the unprivileged
WSL identity directly; Codex/model execution is not part of the deterministic
evaluation. The exact commands, harness entry point, comparison mechanism and
invocation of `test_ca001_checker.py` are OPEN and must be declared before
freeze. A checker-only invocation does not establish the expected-result
comparisons. Each pass must retain the 60-second bound below.

Run exactly two passes against the same frozen artifacts.

Required capture per pass:

- stdout bytes;
- stderr bytes;
- exit code;
- start/end timestamps;
- source/fixture/test/runtime hashes;
- output SHA-256.

Hard bounds:

- 60 seconds maximum per pass;
- 1 MiB maximum combined retained stdout/stderr per pass;
- no automatic retries;
- no candidate or fixture mutation;
- no writes outside the disposable work directory;
- no network/provider/credential access.

## 7. Acceptance criteria

A valid evaluation requires all of:

- 12/12 expected results on pass 1;
- 12/12 expected results on pass 2;
- identical outputs across both passes;
- zero false `eligible-for-human-review` outcomes;
- no fixture/source drift;
- no unauthorized side effects;
- all required evidence retained under controller custody;
- no integrity failure or limit breach;
- independent four-gate review completed with all conditions resolved before
  an admission approval.

Any integrity failure makes that attempt INVALID and blocks an admission
disposition until a separately authorized valid attempt exists.

## 8. Roles and independence

Proposed producer: Foundry-Agent implementation workstream.

Proposed evaluation operator: the Foundry controller environment invoking
the frozen candidate as unprivileged `foundry-agent`.

Proposed evidence custodian: the Foundry controller environment, using the
evidence root designated at freeze.

Independent reviewer: **OPEN — must be named and independence-recorded before
freeze/execution**. The reviewer cannot be the candidate producer and must be
assessed under ADR-0002 for accessible state, authority, relevant prior
exposure, bounded context, and evidence limitations.

A second account controlled by Bulldog is not an independent evaluator.

## 9. Current open freeze items

Evaluation cannot begin until all pre-evaluation items are resolved and Bulldog
authorizes Stage B for the exact frozen tuple:

1. exact candidate/fixture/test source bytes and hashes after implementation;
2. exact Python runtime version and runtime identity/hash;
3. named independent reviewer and independence record;
4. exact controller evidence-capture script/hash, concrete evidence path and
   host-level custody/isolation verification;
5. final packet and manifest hashes, recorded outside the packet to avoid
   self-reference;
6. output format, ordering, any normalization (none presumed), exit-code
   contract including timeout outcomes, and comparison harness;
7. exact per-pass commands, harness responsibility for comparing results with
   `expected_result`, and invocation of `test_ca001_checker.py`;
8. independent confirmation of fixture expected outcomes from the trial-plan
   table, not from checker output, before freeze;
9. independent four-gate review arrangements and acceptance requiring all
   conditions closed before admission approval;
10. case-to-fixture encoding for all 12 cases, without adding cases or policy
    predicates;
11. harness handling of unparseable, blank or duplicate-key JSONL lines and
    unknown extra keys; no extra-key rejection predicate is presumed;
12. enforcement and observation of the 1 MiB combined output bound per pass
    and the prohibition on candidate writes outside the disposable work
    directory.

Items 1 and 5 are finalized after Stage A produces the draft artifacts. Items
2–4 and all other pre-evaluation items must be resolved before Stage B. The
post-evaluation review outcome in item 9 is not a prerequisite for Stage A or
for running the authorized trial; its arrangements must be fixed before freeze.

## 10. Stop point

Stage A: Bulldog separately authorizes bounded implementation, binding this
packet's hash and the §1–§3 specification and paths. This permits producing the
three proposed files; it does not permit evaluation.

Stage B: after those artifacts exist and the pre-evaluation freeze items are
resolved, Bulldog separately authorizes evaluation, binding the §9 tuple of
artifact hashes, runtime, reviewer, capture mechanism and manifest. The final
packet and manifest hashes are recorded outside the packet; no document must
contain its own hash.

Commit, push, PR creation/update and merge remain separate authorization
boundaries throughout both stages. Merging this DRAFT grants neither Stage A
nor Stage B authorization.

Even a valid PASS does not authorize integration.

STOP after preserved evaluation evidence and independent four-gate review.
Admission disposition remains a separate Bulldog decision. Advisory integration
remains separately gated. Merge and reserved acts remain separate founder
boundaries.
