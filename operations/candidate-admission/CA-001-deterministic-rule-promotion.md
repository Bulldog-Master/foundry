# CA-001: Deterministic-rule promotion trial

- Revision: 1 (narrowed draft intake/test plan)
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
check of explicit action authorization against that existing rule. It does not promote
the lesson again or claim to infer human authorization from natural language.

Run-009 remains INVALID. Existing Sandbox verification is frozen reference work,
not a new admission candidate. Baseline v2, memory, orchestration, alternate
runtimes and broader Caller dispatch remain outside this case.

## Proposed candidate and bounded use

A proposed pure offline checker of inert structured fixtures: given one requested
repository action and the action explicitly authorized for that boundary, return
`eligible-for-human-review` only when the requested action exactly matches the
explicitly authorized action; otherwise return `stop`. The five distinct actions
are `commit`, `push`, `pr-create`, `pr-update`, and `merge`. Authorization for one
never supplies authorization for another. A generic instruction such as "proceed"
does not widen the existing scope or authorize a new boundary. Unknown or malformed
actions return `stop` because they cannot establish an exact authorized action.

Eligibility reports only this action-match condition. It neither grants authority
nor establishes readiness to merge; substantive independent four-gate review and
explicit merge authorization remain required. No checker is implemented or executed
by this draft. The proposed checker has no GitHub writes, command execution,
networking or persistence and does not infer authorization from natural language.

Baseline: manual application of the existing authorization-boundary requirement.
Expected improvement: reproducible detection of absent or mismatched explicit
action authorization; no claim of better human judgment or coverage of all
authorization decisions. Potential harm: an eligibility result could be mistaken
for approval. Intended later target: advisory local preflight only, with explicit
human decisions retained. Disable by removing the advisory invocation.

## Proposed finite test plan

Before execution, select the exact fixture encoding, implementation, source/artifact
hashes, configuration, dependency/runtime versions, environment, commands and result
location; name the operator, custodian and independent reviewer. These are OPEN,
so this intake is not ready for evaluation approval. These protocol evidence and
custody requirements are not additional authorization predicates tested by CA-001.

Use these 12 public synthetic fixtures, with expected outcomes independently
checked before freeze. Each fixture represents a single boundary decision; an
explicit authorization in one fixture is not reusable authorization in another.
The encoding must distinguish explicit action authorization from generic text
without interpreting free text.

| Case | Requested action | Explicitly authorized action / instruction | Expected result |
| --- | --- | --- | --- |
| Exact commit | `commit` | `commit` | `eligible-for-human-review` |
| Exact push | `push` | `push` | `eligible-for-human-review` |
| Exact PR creation | `pr-create` | `pr-create` | `eligible-for-human-review` |
| Exact PR update | `pr-update` | `pr-update` | `eligible-for-human-review` |
| Exact merge | `merge` | `merge` | `eligible-for-human-review` |
| Missing authorization | `commit` | None | `stop` |
| Generic proceed | `push` | Generic "proceed" after authorization only for `commit`; no explicit `push` authorization | `stop` |
| Cross-action mismatch | `pr-update` | `pr-create` | `stop` |
| Merge with PR-only authorization | `merge` | `pr-update` | `stop` |
| Unknown action | `publish-all` | `push` | `stop` |
| Malformed action | Missing or non-scalar requested action | `commit` | `stop` |
| Attempted scope expansion | Composite `push` plus `pr-create` request | `push` only | `stop` |

The scope-expansion fixture tests only expansion across the established repository
action boundaries. No real credentials, sealed truth, pilot corpus or production
data are used. Exact merge eligibility tests action matching only, not gate completion.

Expiry, artifact-hash matching, stale authorization-packet revision, repository/path
matching, and broader packet-policy or signing/provider/production authority rules
are deferred future work, outside this corpus and its acceptance criteria. They are
not established by Lesson 0001 and require separate justification and approval.
Protocol v0.1's proposed evidence/version-binding requirements remain distinct from
this narrow test of the existing lesson.

Run the same frozen corpus twice in a local disposable directory, single process,
no network, maximum 60 seconds per pass and 1 MiB total output. Retain both full
outputs, hashes, runtime/configuration and exit status; no automatic retries.
Stop on any protocol integrity failure or limit breach. Expected fixture outcomes
must come from the existing rule, not from candidate output or model agreement.

Proposed acceptance: 12/12 expected results on each pass, identical outputs on
both passes, zero false eligibility results, no fixture mutation or unauthorized
side effects, and independently verified four-gate review with conditions closed.
Passing this finite corpus establishes behavior only within the tested schema and
cases. It cannot establish authenticity of real authorization or exhaustiveness.

## Review, disposition and handoff

Independent review and all four gates: PENDING, not self-certified by this draft.
Decision: NONE. Approval bindings: NONE. Result/evidence hashes: NOT YET AVAILABLE.
All attempts and rejection/defer reasons must be preserved under protocol v0.1.

Open decisions for Bulldog: bounded implementation/evaluation scope, exact fixture
encoding, independent reviewer and evidence custody arrangement. No implementation
or evaluation is authorized by this documentation revision.

Substantive independent review of this PR remains required before merge across
Architecture, Security and Cryptography, Privacy and Metadata, and Quality and
Verification. Repository-mechanics authorization does not make these gates N/A or
satisfy them. Outcomes and checkable independence evidence remain outstanding;
review conditions must be resolved, and a failed gate blocks merge by default under
the existing recorded-override rules. Explicit merge authorization is also separate.

Next approval checkpoint: Bulldog reviews this narrowed case and confirms a bounded
next implementation/evaluation packet. Before actual evaluation, complete and approve
the frozen tuple/plan and establish independent custody. After a valid trial and
independent review, admission stops at the recorded disposition; an exact advisory
integration diff still requires separate Bulldog approval. Commit, push, PR creation,
PR update, and merge remain separate explicit boundaries; authorization for this
PR revision does not authorize implementation, evaluation, integration or merge.
