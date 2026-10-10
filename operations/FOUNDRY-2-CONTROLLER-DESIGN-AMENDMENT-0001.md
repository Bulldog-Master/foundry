# Amendment 0001 — Controller-Observed Reviewer Identity

- **Status:** RATIFIED AS THE FOUNDER'S AUTHORITATIVE INTERPRETATION — NOT COMMISSIONED OR ACTIVATED
- **Amends:** `operations/FOUNDRY-2-CONTROLLER-DESIGN-v0.1.md`, section “Structured review result”
- **Ratified:** 2026-10-10 by the founder's explicit determination recorded below
- **Scope:** Resolves only the authorship and placement of `reviewer_identity` and `independence_record`; it does not ratify ADR-0003, approve a commissioning scope, activate Foundry 2, authorize implementation, or merge this PR

## Founder determination

> I determine that the structured Security/Evaluation result means the combined authoritative review record, and I authorize remediation of the current PR #26 findings on that basis.

This determination is recorded verbatim. It establishes that the governing “structured Security/Evaluation result” is the combined authoritative review record described below.

## Ratified interpretation

Replace `reviewer_identity` and `independence_record` in the evaluator-authored structured payload with a controller-authored invocation record bound to that payload by `result_sha256` and `review_record_sha256`.

The controller must record reviewer/provider identity from observed transport facts, and independence/isolation facts from the commissioned runtime and effective request. The evaluator must not self-attest to its identity, isolation, credentials, accessible context, tools, network, or prior exposure.

The combined authoritative review record remains machine-readable and contains every field required by the governing controller design:

- evaluator payload: `category`, `severity`, `verdict`, `routing`, `requires_human`, and member-addressed `evidence_refs`;
- controller invocation record: observed `reviewer_identity` facts and the complete `independence_record` facts;
- cryptographic bindings between packet, payload, invocation record, task, configuration, and exact PR head.

## Compatibility and commissioning

This ratification resolves the controller-design field-authorship ambiguity for review of this contract. It does not itself commission or activate the design. ADR-0003 ratification, a separate founder-approved commissioning scope, frozen release hashes, trust-anchor evidence, and all other governing preconditions remain mandatory before implementation or activation.
