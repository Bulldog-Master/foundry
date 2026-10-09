# CA-001: Deterministic-rule promotion trial

- Revision: 0 (draft intake/test plan)
- Protocol: [v0.1](PROTOCOL-v0.1.md), DRAFT
- Status: PROPOSED — no implementation, execution, review or admission approval
- Proposer: Foundry Agent under Bulldog's local drafting instruction

## Existing evidence and novelty

Reviewed `main` at `ed8f205995fde4f1dff9f48e9baa1c2224e73fab`, all
repository files, all 19 PR summaries, the PR #15 review, the branch listing
(only main), and issue search (no issues returned).

[Program state](../operations/FOUNDRY-PROGRAM-STATE.md) already calls for v0.1,
deterministic-rule promotion first, approval bound to tested versions, and
reconciliation before larger admissions. No separate admission protocol/case
was found in these records. PR #15 is merged with four recorded PASS reviews.
Its body names `operations/FOUNDRY-PROGRAM-STATE.md`; the committed file is
actually under `operations/operations/`. This draft links the actual path and
does not relocate it or revise the historical PR.

[Lesson 0001](../../lessons/0001-authorization-boundary-clarity.md) is already
Verified and founder-promoted; the PR template already requires separate explicit
authorization at repository action boundaries. This trial proposes a mechanical
check of explicit action packets against that existing rule. It does not promote
the lesson again or claim to infer human authorization from natural language.

Run-009 remains INVALID. Existing Sandbox verification is frozen reference work,
not a new admission candidate. Baseline v2, memory, orchestration, alternate
runtimes and broader Caller dispatch remain outside this case.

## Proposed candidate and bounded use

A pure offline checker of inert structured fixtures: given a requested repository
action and an explicit authorization packet, return `eligible-for-human-review`
only for an exact action, repository, declared paths and artifact revision match;
otherwise return `stop`. Broad text such as "proceed" cannot supply missing fields.
Unknown or malformed input returns `stop`. Eligibility never executes or grants
authorization. No GitHub writes, command execution, networking or persistence.

Baseline: manual application of the existing authorization-boundary requirement.
Expected improvement: reproducible detection of missing/mismatched packet fields;
no claim of better human judgment or of coverage of all authorization decisions.
Potential harm: a misleading eligibility result could be mistaken for approval.
Intended later target: advisory local preflight only, with explicit human decisions
retained. Disable by removing the advisory invocation; no production rollback.

## Proposed finite test plan

Before execution, select the exact schema, implementation, source/artifact hashes,
configuration, dependency/runtime versions, environment, commands and result
location; name the operator, custodian and independent reviewer. These are OPEN,
so this intake is not ready for evaluation approval.

Use 16 public synthetic fixtures, with expected outcomes independently checked
before freeze: 4 exact matches (commit, push, PR creation, PR update); 12 stop
cases (missing authorization; generic proceed; wrong action; wrong repository;
path outside scope; wrong artifact hash; malformed packet; unknown action;
merge requested with PR-only authorization; expired authorization; stale packet
revision; attempted expansion to signing/provider/production authority).
The schema must represent these distinctions without interpreting free text.
No real credentials, sealed truth, pilot corpus or production data are used.

Run the same frozen corpus twice in a local disposable directory, single process,
no network, maximum 60 seconds per pass and 1 MiB total output. Retain both full
outputs, hashes, runtime/configuration and exit status; no automatic retries.
Stop on any protocol integrity failure or limit breach. Expected fixture outcomes
must come from the existing rule, not from candidate output or model agreement.

Proposed acceptance: 16/16 expected results on each pass, identical outputs on
both passes, zero false eligibility results, no fixture mutation or unauthorized
side effects, and independently verified four-gate review with conditions closed.
Passing this finite corpus establishes behavior only within the tested schema and
cases. It cannot establish authenticity of real approval packets or exhaustiveness.

## Review, disposition and handoff

Independent review and all four gates: PENDING, not self-certified by this draft.
Decision: NONE. Approval bindings: NONE. Result/evidence hashes: NOT YET AVAILABLE.
All attempts and rejection/defer reasons must be preserved under protocol v0.1.

Open decisions for Bulldog: whether this checker is the intended first rule;
exact schema and handling of expiry/revision; bounded implementation/evaluation
scope; independent reviewer and evidence custody arrangement. This choice is a
proposal, not an existing repository decision.

Next approval checkpoint: Bulldog reviews the exact two-file draft and confirms
the first test-case interpretation and bounded next packet. No standing workflow
integration is authorized. Before actual evaluation, complete and approve the
frozen tuple/plan and establish independent custody. After a valid trial and
independent review, admission stops at the recorded disposition; an exact advisory
integration diff still requires separate Bulldog approval. Commit, push, PR and
merge boundaries are not crossed by this draft.
