# Foundry 2 Review Packet and Evaluator Result Contract v0.1

- **Status:** DRAFT — DESIGN ONLY — NOT AUTHORIZED FOR IMPLEMENTATION
- **Scope:** Product-neutral contract for the frozen review packet, the evaluator result, and the controller-authored invocation record
- **Authority:** Subordinate to ADR-0001, ADR-0002, `VERSION.md`, `operations/FOUNDRY-2-CONTROLLER-DESIGN-v0.1.md`, and `operations/FOUNDRY-2-COMMISSIONING-v0.1.md`; also subordinate to ADR-0003 only if ADR-0003 is ratified
- **Machine-readable schemas:** `operations/foundry-2/schemas/review-packet.schema.json`, `review-result.schema.json`, `invocation-record.schema.json`
- **Implementation:** No packet-builder code, evaluator adapter, publisher, or routing engine is authorized by this document. Implementation begins only after **both** ADR-0003 is ratified and a separate commissioning scope is approved.

## 1. Purpose

Every substantive PR is evaluated against a sealed, hash-bound packet that no party being governed or evaluating can alter or select. This contract fixes what goes into the packet, what the evaluator may return, and what the controller records about the evaluation, so the evaluator, the GitHub publisher, and the remediation loop can each be built against something exact.

## 2. Roles and separation

| Component | Does | Must not |
| --- | --- | --- |
| Packet builder (deterministic, controller trust root) | Fetches inputs by exact SHA, writes the manifest, hashes, seals | Judge the PR; accept inputs from the producer; be run by the evaluator, Hermes, or Codex |
| Evaluator (isolated Claude invocation) | Reads only the sealed packet; returns one schema-valid result | Hold GitHub or provider credentials; publish; author its own independence claims; select or extend its evidence |
| Controller | Validates the result, checks bindings, derives routing, authors the invocation record | Infer authority from prose |
| Publisher (`foundry-evaluator` GitHub App identity) | Verifies hashes and current head, then posts the check and review | Hold the App key anywhere the evaluator or Hermes can reach; post a PASS for a stale head |
| Controller release custodian | Freezes the builder, task, schemas, governance profile, publisher, and their hashes after founder approval | Produce the subject change; evaluate it; alter a frozen release unilaterally |

The packet builder reads GitHub with a read-only identity. It never uses `Bulldog-Master` or `Bulldog-z` credentials.

The controller release custodian is a separately commissioned administrative role outside all producer workspaces and identities, including Codex, Hermes, and repository operators. Every release or profile change requires a founder-approved commissioning record naming the exact hashes; the custodian may install that approved release but has no policy discretion. The founder ratifies the initial trust anchor and every change to the evaluator task, governance profile, or trusted publisher identity.

## 3. Packet contents

A packet is a directory sealed by `manifest.json` plus members (files). The manifest conforms to `review-packet.schema.json`.

**Included**

1. The exact diff between `merge_base_sha` and `head_sha`, generated with pinned git version and recorded flags (`--binary --no-ext-diff --no-textconv --full-index` at minimum).
2. The full head contents of every changed file. A diff alone is not sufficient for evaluation.
3. Governing references, read at **`base_sha`**, from the independently commissioned controller release profile (the allowlist of Constitution, ADR, `VERSION.md`, and operations paths that govern review). The profile and packet builder are frozen outside the subject repository before use. `governance_profile_sha256` binds the exact profile in the manifest; `producer_identity.build_sha256` binds the builder. A PR therefore cannot alter the rules or evidence-selection code by which it is judged.
4. Profile-declared related context needed by a gate, read at an exact base or head SHA. Each `related_context_refs[]` entry names the packet member, repository path, source SHA, applicable gates, and a non-empty necessity justification. The frozen profile—not the producer or evaluator—selects these paths. Missing context produces `EVIDENCE_MISSING`; it never permits live repository access.
5. If the PR itself changes a governing file, the head version is also included with role `subject_head_version`, and the evaluator task states that the base version governs.
6. The evaluator task (identity, version, hash). The instructions live in the versioned task, not in the packet.
7. For re-review only: the prior packet hash and current round number. Prior findings, titles, verdicts, and other prior judgments are not disclosed to the evaluator.

**Excluded (prohibited context)**

- Producer self-assessment of gate outcomes, and the PR body or comments as instructions. (If PR prose is ever needed, it is included only as a clearly delimited untrusted statement; v0.1 excludes it.)
- Other evaluators' verdicts and all earlier findings, titles, judgments, and verdict prose.
- Founder approval, adoption, override, or activation fields' state as an input to judgment.
- Sealed truth, secrets, credentials.
- Network access and repository access beyond the packet.

**Completeness.** If any input exceeds the size limit, the builder fails. There is no silent truncation. `completeness.complete` must be `true` and `truncated` must be `false`.

**Fork PRs.** `head_repository` is recorded. Content comes from the head repository by SHA.

## 4. Sealing

- Every member is listed in `members[]` with SHA-256 and size.
- `packet_sha256` = SHA-256 of the manifest serialized with the Foundry v0.1 canonical JSON profile, with the `packet_sha256` field omitted. That profile is UTF-8 JSON with no insignificant whitespace, object member names sorted lexicographically by Unicode code point, non-ASCII characters emitted directly, and integers serialized in ordinary base-10 form. Strings encode quotation mark as `\"`, reverse solidus as `\\`, U+0008 as `\b`, U+0009 as `\t`, U+000A as `\n`, U+000C as `\f`, U+000D as `\r`, and every other U+0000–U+001F code point as lowercase `\u00xx`. Solidus is not escaped. Alternative escape spellings and lone UTF-16 surrogates are invalid. All other characters are emitted directly. The v0.1 schemas permit no non-integer JSON numbers. This defines the prospective contract profile and makes no RFC 8785 interoperability claim.
- The sealed packet is stored append-only, outside the write authority of the producer, Hermes, Codex, and the evaluator.
- The packet hash is also written into the GitHub check output when the verdict is published, giving an external witness.
- Inputs are fetched by commit SHA, never by branch name. If the PR head moves while the packet is being built, the build restarts.

## 5. Evaluator invocation

- The evaluator receives the sealed packet and the evaluator task. Nothing else.
- Packet content is untrusted data. Instructions found inside packet files carry no authority.
- No tools beyond reading the packet. No network. No credentials. The invocation record states exactly what was available.
- The evaluator returns a single JSON document conforming to `review-result.schema.json`. Anything else is malformed.

## 6. Evaluator result

Bound to the packet by `packet_sha256`, `pr_number`, `head_sha`, `evaluator_task_sha256`, and the exact `routing_profile` value `foundry-routing-v0.1-security-na-hard-stop`, which must also appear in `manifest.evaluator_task`. Contains four gate verdicts (`PASS`, `FAIL`, `PASS_WITH_CONDITIONS`, `N/A`), findings, an overall verdict, a routing value, and `requires_human`. A task or result omitting or changing that profile is invalid; therefore Security `N/A` cannot inherit a different task-local route.

Schema-enforced where expressible, and otherwise controller-enforced as invalidity rules:

- `N/A` requires a specific `na_reason`.
- `PASS_WITH_CONDITIONS` requires at least one recorded condition.
- `FAIL` requires at least one finding.
- Every finding carries `category`, `severity`, and at least one `evidence_ref` (exact packet-member name and line range). `diff.patch` is addressable like every other member. Repository paths are display-only metadata and never identify evidence.
- Each finding ID resolves exactly once, uses the gate prefix (`ARCH`, `SEC`, `PRIV`, or `QUAL`), matches its finding's gate, and is listed by that gate; every finding is listed.
- `PASS` and `N/A` carry no findings; `conditions` occurs only on `PASS_WITH_CONDITIONS`; `na_reason` occurs only on `N/A`.
- Every `evidence_ref.member` resolves exactly once in `members[]`, and `1 <= line_start <= line_end <= member line count`.
- The controller derives `overall` from gate verdicts (`FAIL` if any gate fails, else `PASS_WITH_CONDITIONS` if any gate is conditional, else `PASS`) and invalidates a mismatch.

The result contains no model identity, session, configuration, or independence claims. Those are not the evaluator's to author.

The controller-design document currently requires `reviewer_identity` and `independence_record` in the structured Security/Evaluation result. This draft proposes relocating them into the controller-authored invocation record because the evaluator must not attest to its own identity or independence. That change is not authoritative unless the founder ratifies it in a separate founder-controlled act outside this subject PR. The controller must hard-stop with `ESCALATE_FOUNDER` until that act is present in the governing base. This draft does not quote, manufacture, or pre-complete that act.

## 7. Invocation record (controller-authored)

Built from observed facts: provider and model ID, effective configuration hash, system-prompt hash, session ID, runtime image hash, host, accessible context, tools available, network policy, credentials present (must be empty), known prior exposure and its stated limits, attempt number, timestamps, transport outcome, exact raw-output byte count and hash, adverse-signal scan record, pre-transmission disclosure record, schema-validation outcome, routing-check outcome, and `review_record_sha256`. `raw_output_sha256` is computed over the exact response bytes before parsing. It is null only when `raw_output_bytes` is zero; otherwise it is mandatory, including partial output before a timeout and every malformed or schema-invalid response. Raw bytes are retained under the same custody and retention rules. `result_sha256` is present exactly when `schema_validation` is `VALID`; otherwise it is null.

For a valid result, `result_sha256` is SHA-256 of the parsed result reserialized with the Foundry v0.1 canonical JSON profile. It is `null` whenever no schema-valid result exists; `raw_output_sha256` still binds the exact received bytes. `invocation_record_without_hash` is the complete invocation-record object with only `review_record_sha256` omitted. `review_record_sha256` is SHA-256 of the canonical JSON object with exactly the keys `packet_sha256`, `result_sha256`, and `invocation_record_without_hash`.

The record schema deliberately permits any non-empty observed context label and therefore preserves observed violations: extra context, tool names, credentials, widened or unknown network state, and every invalidity class remain representable. For a valid run, both `manifest.allowed_context` and `invocation_record.accessible_context` must equal exactly `["packet_manifest", "packet_members", "evaluator_task"]`; `tools_available` and `credentials_present` must be empty; and `network_policy` must be `none`. Any deviation invalidates the evaluation. The provider credential belongs only to the controller transport boundary and is never evaluator-visible.

## 7.1 ADR-0002 Decisions 1–5

1. **Non-interactive independence.** The evaluator receives one sealed packet and returns one JSON document. It has no repository, GitHub, controller, publisher, or remediation-loop channel.
2. **No self-asserted independence.** The controller release custodian freezes the task and profile outside the subject repository; their hashes are bound into the packet and invocation record. The evaluator supplies neither identity nor independence claims.
3. **Verified isolation.** Commissioning captures effective provider request configuration, tool count, network policy, credential visibility, accessible-context enumeration, runtime hash, filesystem ownership/modes, and negative probes. A missing or widened observation invalidates the run.
4. **Prior-exposure eligibility.** A later round names the prior packet but supplies no prior findings or judgments. The invocation record lists known prior sessions and knowability limits. Known prior-judgment exposure or materially unresolved exposure makes the run ineligible and hard-stops before publication.
5. **Minimum bounded context.** The packet contains only the manifest, exact diff, changed-file contents, frozen governing references, profile-declared justified related context, and task binding. Completeness is fail-closed, and no live network, live repository expansion, producer-selected context, or prior judgment is permitted.

## 8. Deterministic routing

The controller derives routing from the structured result using this frozen table, evaluated top to bottom. The evaluator's own `routing` and `requires_human` values must equal the derived values. A mismatch makes the result invalid (§9); the controller never silently takes either value.

| Condition | Routing | Human |
| --- | --- | --- |
| Any finding category is `RESERVED_ACT_REQUIRED` | `ESCALATE_FOUNDER` | yes |
| The Security gate is `FAIL` or `N/A` | `HARD_STOP` | yes |
| Any finding category is `TRUST_BOUNDARY_DEFECT`, `INTEGRITY_ANOMALY`, `SPEC_AMBIGUITY`, or `OTHER`; or any finding severity is `CRITICAL` | `HARD_STOP` | yes |
| Any non-Security gate is `FAIL`, or any gate is `PASS_WITH_CONDITIONS`; and every finding category is `IMPLEMENTATION_DEFECT` or `EVIDENCE_MISSING` | `RETURN_TO_OPERATIONS` | no |
| Every gate is `PASS` or `N/A`, and there are no findings | `CONTINUE` | no |

A Security `FAIL` or `N/A` blocks regardless of other gates. Security may be `N/A` only as an explicit adverse result; it can never produce `CONTINUE`, a success check, or an approving review. If ADR-0003 is ratified, closing that hard stop is its reserved act 12; an override remains a separate reserved act. Automated remediation may prepare a new commit, but it does not itself close the Security hard stop. Multiple-evaluator disagreement is out of scope and has no derivation rule in v0.1.

Controller-side outcomes are also deterministic and are evaluated before the result table: an ineligible evaluator, unresolved material prior exposure, packet/profile/member failure, widened context, tools, network, credentials, or a second invalid response produces `HARD_STOP`, requires a human, and publishes `action_required`. A first invalid response is eligible for one identical retry **only if the deterministic adverse-signal scan reports `NONE`**. The scan operates on the exact raw bytes: decode strict UTF-8; parse exactly one complete JSON value while rejecting duplicate object keys; require an object root; then recursively visit every object and array. It reports `ADVERSE` if any member has the exact pair `"verdict":"FAIL"`, `"severity":"CRITICAL"`, or `"category"` equal to `TRUST_BOUNDARY_DEFECT`, `INTEGRITY_ANOMALY`, `SPEC_AMBIGUITY`, `RESERVED_ACT_REQUIRED`, or `OTHER`. Invalid UTF-8, parse failure, a non-object root, and other values report `NONE`, not an inferred judgment. The invocation record stores the algorithm version, outcome, and sorted unique matched signals. `ADVERSE` on attempt 1 immediately hard-stops; attempt 2 always hard-stops when invalid. A stale head produces no publication and a newly sealed packet. These are controller outcomes, never evaluator-authored routing values.

## 9. Malformed, mismatched, or stale results

- Schema-invalid; binding mismatch; derived-overall mismatch; finding/gate/ID mismatch; invalid evidence path or line range; widened context, tools, network, or credentials; packet member/profile cross-reference failure; or routing mismatch: the result is **invalid**, never reinterpreted or repaired.
- The controller may issue exactly **one** fresh invocation on the identical packet and configuration (attempt 2) only when attempt 1 is invalid and contains no safely parseable adverse signal defined in §8. Both attempts are retained and visible.
- A second invalid result is a `HARD_STOP`.
- A valid `FAIL` or `PASS_WITH_CONDITIONS` is never re-run. The retry applies only to invalid output, so it cannot be used to shop for a better verdict.
- Stale: if `head_sha` differs from the PR's current head at acceptance, publication, or immediately before `FOUNDER_ACTION_REQUIRED`, the result is stale. The publisher refuses to post a PASS for a stale head, and the controller starts a new packet.

## 10. Publication

The publisher validates: result schema, `packet_sha256` against the stored sealed packet, `review_record_sha256`, routing check, and current head. Then it posts as `foundry-evaluator`:

- a check run, `foundry/four-gate`: `success` only for a current-head valid `PASS / CONTINUE`; `failure` for any valid `FAIL`, `PASS_WITH_CONDITIONS`, `RETURN_TO_OPERATIONS`, or evaluator-derived `HARD_STOP`; and `action_required` for controller-side invalidity, independence hard stop, or `ESCALATE_FOUNDER`;
- a review rendered by a fixed template from the structured result. `PASS` maps to `APPROVE`; every other overall/routing state maps to `REQUEST_CHANGES`. Evaluator prose appears only as quoted data and is never interpreted.

The publisher also verifies that every non-deleted `changed_files[].member`, `diff.member`, `governance_refs[].member`, and `related_context_refs[].member` resolves exactly once in `members[]` with matching hashes and sizes; that `governance_refs` is non-empty; and that every changed governing path has both its base-governing and `subject_head_version` entries. Every `governing` ref must use `source_sha == base_sha`; every `subject_head_version` ref must use `source_sha == head_sha`; the governing paths must equal the frozen profile allowlist; and each related-context path, source choice, gate list, and justification must equal the frozen profile entry. Failure is invalid and no success or approval is posted.

Published GitHub output contains the gate verdicts, structured findings, routing, head SHA, packet hash, result hash, and review-record hash only. It excludes provider request/session identifiers, host identity, model configuration, and invocation-environment details.

This draft does not claim that any GitHub App is trusted or installed. Commissioning must record the founder-approved App ID, installation ID, repository ID, key-custody boundary, and independently captured GitHub installation evidence. Until that record is ratified, no check or review identity is authoritative. Once ratified, the repository ruleset must require the `foundry/four-gate` check from that exact App integration, not merely a matching check name. A counted review must have GitHub's verified App-authored identity for the same App and exact head. A same-named workflow, user, token, or different App never satisfies either trust. These source bindings are mandatory commissioning acceptance tests.

## 10.1 Privacy, disclosure, and retention

Before provider transmission, the controller scans every byte that will cross the provider boundary—including the manifest, diff, all changed-file members, every governing and related-context member, and the evaluator task—for credential patterns, private keys, high-entropy tokens, and configured personal-data patterns. The invocation record binds the scanner release hash, packet hash, repository visibility observed from GitHub, byte and member counts, scan outcome, matched-rule IDs, provider-terms record hash, and any founder disclosure-decision hash. Any match blocks transmission unless an exact founder disclosure decision authorizes those matched rule IDs for that exact packet. v0.1 permits automatic transmission only when repository and fork visibility are public, the scan is clean, and provider terms are recorded and accepted. Private content requires a founder disclosure decision for the exact packet after the provider's current terms are recorded; unavailable or unacceptable terms block transmission. These are schema- and conformance-tested preconditions, not prose-only assertions.

Packets and invocation evidence are root-owned, mode `0500`/`0400` or stricter, append-preserving during their retention window, and inaccessible to producer and evaluator identities. Evidence for merged PRs expires one year after the later of merge or dependent activation; unmerged-PR evidence expires one year after closure; commissioning, preflight, and shadow evidence expires one year after the later of activation or abandonment. The retention job must delete expired evidence within 30 days, so ordinary maximum retention is 13 months after the applicable terminal event. `host_id`, provider session ID, and unhashed effective configuration are minimized or cryptographically redacted 30 days after final publication while their hashes and audit bindings remain. A legal hold, open incident, or documented audit dependency may suspend deletion only while recorded and must be reviewed every 90 days. No governed producer, evaluator, controller worker, or publisher can delete evidence. Deletion requires a separately commissioned founder-approved retention job, an audit record of exact deleted hashes, and confirmation that no hold remains. Changing this policy is a founder-reserved retention decision. GitHub publication is limited to the fields listed above.

## 11. Founder notification

`FOUNDER_ACTION_REQUIRED` is emitted only when: overall is `PASS`, the published check is `success`, the head is re-verified current, and no hard stop is open. It names the exact head SHA and the requested reserved act (protected-branch merge).

## 12. Decisions taken as defaults in this draft

These are defaults chosen to keep the founder out of the loop. Each goes to independent review with this document and can be changed:

1. `PASS_WITH_CONDITIONS` returns to Operations in v0.1 (conservative). A later version may allow recorded post-merge conditions.
2. The PR body is excluded from the packet.
3. Re-review packets carry only the prior packet hash and no prior judgments.
4. One re-invocation is permitted for malformed output only.

## 13. Not covered by this contract

The remediation-loop work order format, the Codex worker adapter, the Hermes adapter, the GitHub App creation, and the Anthropic provider credential for the evaluator. If ADR-0003 is ratified, its reserved-act catalogue governs those founder-controlled acts; until then, Foundry 1 remains authoritative.

## Appendix A. Conformance fixtures

`operations/foundry-2/CONFORMANCE-VECTORS-v0.1.json`, `operations/foundry-2/verify-conformance-v0.1.py`, and `operations/foundry-2/requirements-conformance-v0.1.txt` are normative together. The verifier executes the valid and invalid schema instances, canonical-JSON/hash vectors (including every control-character escape form), binding/member/evidence/context invalidities, zero-byte timeout representation, disclosure gating, adverse-invalid retry rule, stale-head behavior, and every routing row. Dependencies must be installed at the exact pinned versions. The vector file records the normative canonical byte literals plus two digest cross-check commands. The commands independently hash the same literal bytes; they are not represented as independent canonicalizers. The verifier must first reproduce each literal from its input, then compare both the literal and its digest, validate schemas with mandatory format checking, and execute controller rules from input fields rather than case identifiers. Commissioning requires a checked-in conformance-run evidence record containing the verifier hash, vector hash, schema hashes, dependency versions, command, timestamp, and `PASS` output; prose-only mutations are not conformance cases.
