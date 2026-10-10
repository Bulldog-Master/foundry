# Foundry 2 Review Packet and Evaluator Result Contract v0.1

- **Status:** DRAFT — DESIGN ONLY — NOT AUTHORIZED FOR IMPLEMENTATION
- **Scope:** Product-neutral contract for the frozen review packet, the evaluator result, and the controller-authored invocation record
- **Authority:** Subordinate to ADR-0003, ADR-0001, ADR-0002, `operations/FOUNDRY-2-CONTROLLER-DESIGN-v0.1.md`, and `operations/FOUNDRY-2-COMMISSIONING-v0.1.md`
- **Machine-readable schemas:** `operations/foundry-2/schemas/review-packet.schema.json`, `review-result.schema.json`, `invocation-record.schema.json`
- **Implementation:** No packet-builder code, evaluator adapter, publisher, or routing engine is authorized by this document. Implementation begins only after the commissioning scope is approved.

## 1. Purpose

Every substantive PR is evaluated against a sealed, hash-bound packet that no party being governed or evaluating can alter or select. This contract fixes what goes into the packet, what the evaluator may return, and what the controller records about the evaluation, so the evaluator, the GitHub publisher, and the remediation loop can each be built against something exact.

## 2. Roles and separation

| Component | Does | Must not |
| --- | --- | --- |
| Packet builder (deterministic, controller trust root) | Fetches inputs by exact SHA, writes the manifest, hashes, seals | Judge the PR; accept inputs from the producer; be run by the evaluator, Hermes, or Codex |
| Evaluator (isolated Claude invocation) | Reads only the sealed packet; returns one schema-valid result | Hold GitHub or provider credentials; publish; author its own independence claims; select or extend its evidence |
| Controller | Validates the result, checks bindings, derives routing, authors the invocation record | Infer authority from prose |
| Publisher (`foundry-evaluator` GitHub App identity) | Verifies hashes and current head, then posts the check and review | Hold the App key anywhere the evaluator or Hermes can reach; post a PASS for a stale head |

The packet builder reads GitHub with a read-only identity. It never uses `Bulldog-Master` or `Bulldog-z` credentials.

## 3. Packet contents

A packet is a directory sealed by `manifest.json` plus members (files). The manifest conforms to `review-packet.schema.json`.

**Included**

1. The exact diff between `merge_base_sha` and `head_sha`, generated with pinned git version and recorded flags (`--binary --no-ext-diff --no-textconv --full-index` at minimum).
2. The full head contents of every changed file. A diff alone is not sufficient for evaluation.
3. Governing references, read at **`base_sha`**, from the independently commissioned controller release profile (the allowlist of Constitution, ADR, `VERSION.md`, and operations paths that govern review). The profile and packet builder are frozen outside the subject repository before use, and their hashes are recorded in commissioning evidence. A PR therefore cannot alter the rules or evidence-selection code by which it is judged.
4. If the PR itself changes a governing file, the head version is also included with role `subject_head_version`, and the evaluator task states that the base version governs.
5. The evaluator task (identity, version, hash). The instructions live in the versioned task, not in the packet.
6. For re-review only: structured prior findings (ID, gate, severity, title, claimed remediation commit). No prior verdict prose.

**Excluded (prohibited context)**

- Producer self-assessment of gate outcomes, and the PR body or comments as instructions. (If PR prose is ever needed, it is included only as a clearly delimited untrusted statement; v0.1 excludes it.)
- Other evaluators' verdicts, and any verdict prose from earlier rounds.
- Founder approval, adoption, override, or activation fields' state as an input to judgment.
- Sealed truth, secrets, credentials.
- Network access and repository access beyond the packet.

**Completeness.** If any input exceeds the size limit, the builder fails. There is no silent truncation. `completeness.complete` must be `true` and `truncated` must be `false`.

**Fork PRs.** `head_repository` is recorded. Content comes from the head repository by SHA.

## 4. Sealing

- Every member is listed in `members[]` with SHA-256 and size.
- `packet_sha256` = SHA-256 of the manifest serialized with the Foundry v0.1 canonical JSON profile, with the `packet_sha256` field omitted. That profile is UTF-8 JSON with no insignificant whitespace, object member names sorted lexicographically by Unicode code point, non-ASCII characters emitted directly, and integers serialized in ordinary base-10 form. The v0.1 schemas permit no non-integer JSON numbers. This deliberately describes the implemented profile and makes no RFC 8785 interoperability claim.
- The sealed packet is stored append-only, outside the write authority of the producer, Hermes, Codex, and the evaluator.
- The packet hash is also written into the GitHub check output when the verdict is published, giving an external witness.
- Inputs are fetched by commit SHA, never by branch name. If the PR head moves while the packet is being built, the build restarts.

## 5. Evaluator invocation

- The evaluator receives the sealed packet and the evaluator task. Nothing else.
- Packet content is untrusted data. Instructions found inside packet files carry no authority.
- No tools beyond reading the packet. No network. No credentials. The invocation record states exactly what was available.
- The evaluator returns a single JSON document conforming to `review-result.schema.json`. Anything else is malformed.

## 6. Evaluator result

Bound to the packet by `packet_sha256`, `pr_number`, `head_sha`, and `evaluator_task_sha256`. Contains four gate verdicts (`PASS`, `FAIL`, `PASS_WITH_CONDITIONS`, `N/A`), findings, an overall verdict, a routing value, and `requires_human`.

Schema-enforced rules:

- `N/A` requires a specific `na_reason`.
- `PASS_WITH_CONDITIONS` requires at least one recorded condition.
- `FAIL` requires at least one finding.
- Every finding carries `category`, `severity`, and at least one `evidence_ref` (path and line range).

The result contains no model identity, session, configuration, or independence claims. Those are not the evaluator's to author.

## 7. Invocation record (controller-authored)

Built from observed facts: provider and model ID, effective configuration hash, system-prompt hash, session ID, runtime image hash, host, accessible context, tools available, network policy, credentials present (must be empty), known prior exposure and its stated limits, attempt number, timestamps, schema-validation outcome, routing-check outcome, and `review_record_sha256`.

`review_record_sha256` = SHA-256 of the canonicalized `{packet_sha256, result_sha256, invocation_record_without_hash}`.

## 8. Deterministic routing

The controller derives routing from the structured result using this frozen table, evaluated top to bottom. The evaluator's own `routing` and `requires_human` values must equal the derived values. A mismatch makes the result invalid (§9); the controller never silently takes either value.

| Condition | Routing | Human |
| --- | --- | --- |
| Any finding with category `RESERVED_ACT_REQUIRED` | `ESCALATE_FOUNDER` | yes |
| Any finding with category `TRUST_BOUNDARY_DEFECT` or `INTEGRITY_ANOMALY`; any `CRITICAL` finding; any `SPEC_AMBIGUITY` finding | `HARD_STOP` | yes |
| Any gate `FAIL`, or any gate `PASS_WITH_CONDITIONS` (all findings `IMPLEMENTATION_DEFECT` or `EVIDENCE_MISSING`, none `CRITICAL`) | `RETURN_TO_OPERATIONS` | no |
| All four gates `PASS` or `N/A` (with reason), no open findings | `CONTINUE` | no |

A Security `FAIL` blocks regardless of other gates and can be bypassed only by a recorded founder override (reserved act 5). Disagreement between multiple evaluators is out of scope for v0.1 and routes `ESCALATE_FOUNDER`.

A finding in category `OTHER` routes `HARD_STOP` with `requires_human = true`.
A `PASS` or `N/A` gate must carry no findings; otherwise the result is invalid.

## 9. Malformed, mismatched, or stale results

- Schema-invalid, binding mismatch, or routing mismatch: the result is **invalid**, never reinterpreted or repaired.
- The controller may issue exactly **one** fresh invocation on the identical packet and configuration (attempt 2). Both attempts are retained and visible.
- A second invalid result is a `HARD_STOP`.
- A valid `FAIL` or `PASS_WITH_CONDITIONS` is never re-run. The retry applies only to invalid output, so it cannot be used to shop for a better verdict.
- Stale: if `head_sha` differs from the PR's current head at acceptance, publication, or immediately before `FOUNDER_ACTION_REQUIRED`, the result is stale. The publisher refuses to post a PASS for a stale head, and the controller starts a new packet.

## 10. Publication

The publisher validates: result schema, `packet_sha256` against the stored sealed packet, `review_record_sha256`, routing check, and current head. Then it posts as `foundry-evaluator`:

- a check run, `foundry/four-gate`: `success` only when overall is `PASS` and the head is current; otherwise `failure` or `action_required`;
- a review rendered by a fixed template from the structured result. Evaluator prose appears only as quoted data and is never interpreted.

Which of the two branch protection trusts is established by the commissioning test PR, not assumed.

## 11. Founder notification

`FOUNDER_ACTION_REQUIRED` is emitted only when: overall is `PASS`, the published check is `success`, the head is re-verified current, and no hard stop is open. It names the exact head SHA and the requested reserved act (protected-branch merge).

## 12. Decisions taken as defaults in this draft

These are defaults chosen to keep the founder out of the loop. Each goes to independent review with this document and can be changed:

1. `PASS_WITH_CONDITIONS` returns to Operations in v0.1 (conservative). A later version may allow recorded post-merge conditions.
2. The PR body is excluded from the packet.
3. Re-review packets carry structured prior findings, and the invocation record notes that exposure.
4. One re-invocation is permitted for malformed output only.

## 13. Not covered by this contract

The remediation-loop work order format, the Codex worker adapter, the Hermes adapter, the GitHub App creation, and the Anthropic provider credential for the evaluator. The last two are founder-reserved acts (3 and 8).
