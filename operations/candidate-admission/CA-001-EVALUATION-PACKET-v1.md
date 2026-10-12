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

Input is one decoded JSON object. The checker returns exactly one of:

- `eligible-for-human-review`
- `stop`

Recognized requested actions are exactly:

- `commit`
- `push`
- `pr-create`
- `pr-update`
- `merge`

Eligibility is returned only when all of the following are true:

1. `requested_action` is a scalar string in the recognized set;
2. `authorization.kind == "explicit-action"`;
3. `authorization.action` is a scalar string in the recognized set;
4. `authorization.action == requested_action`;
5. no extra requested action is present.

Everything else returns `stop`.

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

Malformed-action coverage uses a non-scalar or absent `requested_action`.
The scope-expansion fixture uses a non-scalar composite request and must return
`stop`.

## 3. Proposed implementation artifacts

Candidate artifacts to be created only after exact packet authorization:

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

The Bulldog-Surface Windows controller is the proposed evidence custodian.

Proposed evidence root:

`C:\Users\John\Foundry-Control\candidate-admission\CA-001\v1\`

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

After freeze, the controller invokes the unprivileged WSL identity directly;
Codex/model execution is not part of the deterministic evaluation.

For each pass:

`timeout 60s python3 ca001_checker.py fixtures/ca001-v1.jsonl`

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
- byte-identical normalized outputs across both passes;
- zero false `eligible-for-human-review` outcomes;
- no fixture/source drift;
- no unauthorized side effects;
- all required evidence retained under controller custody;
- no integrity failure or limit breach.

Any integrity failure makes that attempt INVALID and blocks an admission
disposition until a separately authorized valid attempt exists.

## 8. Roles and independence

Proposed producer: Foundry-Agent implementation workstream.

Proposed evaluation operator: Bulldog-Surface deterministic controller invoking
the frozen candidate as unprivileged `foundry-agent`.

Proposed evidence custodian: Bulldog-Surface controller-side evidence root.

Independent reviewer: **OPEN — must be named and independence-recorded before
freeze/execution**. The reviewer cannot be the candidate producer and must be
assessed under ADR-0002 for accessible state, authority, relevant prior
exposure, bounded context, and evidence limitations.

A second account controlled by Bulldog is not an independent evaluator.

## 9. Current open freeze items

This packet is not executable until all are resolved and Bulldog authorizes the
exact tuple:

1. exact candidate/fixture/test source bytes and hashes after implementation;
2. exact Python runtime version;
3. named independent reviewer and independence record;
4. exact controller evidence-capture script/hash;
5. final packet/manifest hash.

## 10. Stop point

Authorization of this packet may permit bounded implementation and/or
evaluation only if Bulldog explicitly says so for the exact frozen tuple.

Even a valid PASS does not authorize integration.

STOP after preserved evaluation evidence and independent four-gate review.
Admission disposition remains a separate Bulldog decision. Advisory integration
remains separately gated. Merge and reserved acts remain separate founder
boundaries.
