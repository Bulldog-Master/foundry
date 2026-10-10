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

This subject PR does not evidence, quote, author, or pre-complete the founder's reserved act. The sole recognized ratification artifact is `operations/foundry-2/ratifications/AMENDMENT-0001.json` read from the base commit and included as a `governing` member. It must name amendment `0001`, bind the SHA-256 of this amendment, identify the founder, record `RATIFY`, carry an RFC 3339 timestamp, and provide a non-empty founder-controlled signature or evidence reference. Absence or mismatch produces the controller-side outcome `ESCALATE_FOUNDER` with `requires_human=true`; it is not an evaluator routing-table result and is not called `HARD_STOP`. Ratification resolves only the controller-design field-authorship ambiguity; it does not commission or activate the design. ADR-0003 ratification, a separate founder-approved commissioning scope, frozen release hashes, trust-anchor evidence, and all other governing preconditions remain mandatory before implementation or activation.
