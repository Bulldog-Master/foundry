# Amendment 0001 — Controller-Observed Reviewer Identity

- **Status:** PROPOSED — NOT RATIFIED, COMMISSIONED, OR ACTIVATED
- **Amends:** `operations/FOUNDRY-2-CONTROLLER-DESIGN-v0.1.md`, section “Structured review result”
- **Ratification:** Requires a separate founder-controlled act outside this subject PR
- **Scope:** Resolves only the authorship and placement of `reviewer_identity` and `independence_record`; it does not ratify ADR-0003, approve a commissioning scope, activate Foundry 2, authorize implementation, or merge this PR

## Proposed interpretation

Replace `reviewer_identity` and `independence_record` in the evaluator-authored structured payload with a controller-authored invocation record bound to that payload by `result_sha256` and `review_record_sha256`.

The controller must record reviewer/provider identity from observed transport facts, and independence/isolation facts from the commissioned runtime and effective request. The evaluator must not self-attest to its identity, isolation, credentials, accessible context, tools, network, or prior exposure.

The combined authoritative review record remains machine-readable and contains every field required by the governing controller design:

- evaluator payload: `category`, `severity`, `verdict`, `routing`, `requires_human`, and member-addressed `evidence_refs`;
- controller invocation record: observed `reviewer_identity` facts and the complete `independence_record` facts;
- cryptographic bindings between packet, payload, invocation record, task, configuration, and exact PR head.

## Ratification boundary and commissioning

This subject PR does not evidence, quote, author, or pre-complete the founder's reserved act. Until a separate founder-controlled record ratifies this amendment in the governing base, the controller must treat the proposal as non-authoritative and route `ESCALATE_FOUNDER`. Ratification would resolve only the controller-design field-authorship ambiguity; it would not commission or activate the design. ADR-0003 ratification, a separate founder-approved commissioning scope, frozen release hashes, trust-anchor evidence, and all other governing preconditions remain mandatory before implementation or activation.
