# PR #26 Founder Override Record

- **Status:** APPROVED
- **Pull request:** #26
- **Evaluated head:** `dcb0c9afa29815045007248a69492a392b5f63fe`
- **Approved content head:** `4fa54f37c8720c51a04fde3b0f3df95cc0270999`
- **Evaluator result at evaluated head:** `FAIL`
- **Routing:** `HARD_STOP`
- **Founder identity:** `github:Bulldog-Master`
- **Decision:** `APPROVE_FOUNDER_OVERRIDE`
- **Recorded at:** `2026-10-11T13:59:45Z`
- **Evidence:** [Founder-authenticated PR comment](https://github.com/Bulldog-Master/foundry/pull/26#issuecomment-6109799158)

## Founder statement

> I, Bulldog, approve the PR #26 founder override record as drafted, covering the content at head `4fa54f37c8720c51a04fde3b0f3df95cc0270999`. I accept findings FND-SEC-001, FND-SEC-002, FND-PRIV-001 and FND-QUAL-003 as design debt in a design-only v0.1 draft. This approval closes the HARD_STOP recorded for head `dcb0c9afa29815045007248a69492a392b5f63fe` for PR #26 only. It closes no other stop and grants no implementation, commissioning, or activation authority. The only change permitted after this approval is the addition of the override record file itself.

## Accepted findings and risk

1. **FND-SEC-001 — Security — MAJOR.** The adverse-signal retry rule uses a denylist. An unusual or noncanonical adverse evaluator response could be classified as retry-eligible, allowing a bad evaluator run to be quietly retried. This is accepted only as design debt in a design-only draft and must be corrected before implementation.
2. **FND-SEC-002 — Security — MINOR.** Normative conformance dependencies are version-pinned without cryptographic artifact hashes.
3. **FND-PRIV-001 — Privacy — MINOR.** A provider-terms transmission block cannot be represented consistently by the current record schema.
4. **FND-QUAL-003 — Quality — MINOR.** Zero-byte timeout handling is inconsistent across the specification, vectors, and harness.

The draft must not be treated as validated implementation, commissioning evidence, activation authority, or authority to operate an evaluator.

## Rationale

PR #26 is a design-only v0.1 draft. It grants no implementation, commissioning, activation, production, credential, publishing, or autonomous-operation authority.

Implementation remains separately gated by correction or formal disposition of the accepted findings, ADR-0003 ratification, a founder-approved commissioning scope, fresh conformance evidence from the exact implementation artifacts, and independent evaluation of the implementation and operational controls.

## Required follow-up

- **FND-SEC-001:** Replace the adverse-output denylist with a fail-closed retry rule. The recommended v0.1.1 design is to allow a retry only after an empty provider response.
- **FND-SEC-002:** Add verified dependency artifact hashes with hash-enforced installation, or use a reproducible dependency-free harness.
- **FND-PRIV-001:** Define and test a conforming non-transmission record for unavailable or unacceptable provider terms.
- **FND-QUAL-003:** Define zero-byte transport failure explicitly and align the specification, schema, vectors, and harness.

Each follow-up item retains its evaluator finding ID for traceability.

## Remediated after evaluation, not re-evaluated

These corrections are present at approved content head `4fa54f37c8720c51a04fde3b0f3df95cc0270999`. They have not been independently re-evaluated, and this record does not claim that either gate now passes.

### FND-QUAL-001

A `MATCH_AUTHORIZED` disclosure without `founder_decision_sha256` now returns `INVALID_OTHER`. The replacement harness has SHA-256 `50cff93445fbe2db97b3361fab7daf2715be7485a7854db84ba7009f0ca185c9`. The pinned environment produced:

```text
PASS conformance-v0.1
```

### FND-QUAL-002

`CONFORMANCE-RUN-v0.1.json` was regenerated after the harness correction. All six recorded artifact hashes match the final files, and the record identifies the pinned `jsonschema 4.19.2` environment. This is deterministic producer evidence, not an independent evaluator verdict.

## Reassessment conditions

The four accepted findings must be reassessed before any implementation work based on this contract begins and during ADR-0003 ratification.

The two post-evaluation corrections must also be verified before commissioning or activation. No implementation, commissioning, or activation may rely on this override as proof that an evaluator gate passed.

## Effect and boundary

This override closes only the `HARD_STOP` recorded for evaluated head `dcb0c9afa29815045007248a69492a392b5f63fe` on PR #26, for the design-only content approved at head `4fa54f37c8720c51a04fde3b0f3df95cc0270999`. It does not turn the failed gate into a pass, close any other stop, ratify ADR-0003, authorize implementation or commissioning, activate Foundry 2, or itself merge PR #26.
