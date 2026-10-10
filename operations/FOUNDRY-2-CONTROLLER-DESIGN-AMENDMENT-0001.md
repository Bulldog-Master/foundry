# Proposed Amendment 0001 — Controller-Observed Reviewer Identity

- **Status:** PROPOSED — NOT RATIFIED — NO AUTHORITY
- **Amends:** `operations/FOUNDRY-2-CONTROLLER-DESIGN-v0.1.md`, section “Structured review result”
- **Effective only if:** explicitly ratified by the founder together with ADR-0003 and the commissioning scope

## Proposal

Replace `reviewer_identity` and `independence_record` in the evaluator-authored structured payload with a controller-authored invocation record bound to that payload by `result_sha256` and `review_record_sha256`.

The controller must record reviewer/provider identity from observed transport facts, and independence/isolation facts from the commissioned runtime and effective request. The evaluator must not self-attest to its identity, isolation, credentials, accessible context, tools, network, or prior exposure.

The combined authoritative review record remains machine-readable and contains every field required by the governing controller design:

- evaluator payload: `category`, `severity`, `verdict`, `routing`, `requires_human`, and member-addressed `evidence_refs`;
- controller invocation record: observed `reviewer_identity` facts and the complete `independence_record` facts;
- cryptographic bindings between packet, payload, invocation record, task, configuration, and exact PR head.

## Compatibility and migration

Until this amendment is ratified, the existing controller-design requirement governs and the v0.1 review-packet contract cannot be commissioned. Ratification changes only authorship and placement of the two fields; it does not weaken or remove them.
