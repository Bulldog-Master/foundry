# ADR 0001: Model-neutral Foundry, model-specific operation, and the four-gate operating contract

- **Status:** Accepted
- **Type:** Doctrinal
- **Expires:** Does not expire
- **Date:** 2026-07-13
- **Author(s):** Bulldog-Master (founder)
- **Related ADRs:** None

## Context

Foundry 0 established a minimum permanent foundation: a Constitution, blank templates, one authorized product (Daang Remote), and human approval before merge. That baseline was sufficient to ratify pre-commitments and to receive the first product charter, but it did not yet describe how work is actually evaluated once it begins to produce artifacts.

Two forces pushed a next-generation decision:

- **Replaceable intelligence in practice.** The Constitution treats any intelligence — human or AI — as replaceable infrastructure. In real use, models differ. Prompts, adapters, calibration data, evaluation baselines, and pass/fail thresholds are model-specific. Treating "replaceable" as if it meant "behaviourally equivalent, zero retuning" would silently make Foundry depend on whichever model happened to be in use.
- **Builder as sole evaluator.** In Foundry 0 the founder was both the producer of work and the only reviewer of it. That was acceptable for ratifying pre-commitments; it is not acceptable for evaluating substantive engineering claims. A change cannot be its own witness.

This ADR ratifies the operating contract that resolves both, and names it Foundry 1.

## Decision

Foundry adopts a **model-neutral doctrine, model-specific operation** posture and a **four-gate operating contract** enforced on every substantive change.

### Model neutrality vs model specificity

- **Doctrine is model-neutral.** The Constitution, ADRs, charters, templates, and gate definitions do not name a specific model, vendor, or agent framework.
- **Operation is model-specific.** Prompts, adapters, calibration data, evaluation baselines, thresholds, and any retuning required to make a particular intelligence perform to gate standard are model-specific artifacts and are expected to change when the intelligence changes.
- **Replaceable does not mean equivalent.** Swapping the intelligence is a supported operation; it is not a no-op. The cost of a swap is the cost of reproducing the model-specific artifacts against the new model, not a claim that the new model will behave identically.

### The four mandatory gates

Every substantive change to a product or to Foundry itself is evaluated against four gates:

1. **Architecture Gate** — Is the change coherent with the current architectural commitments? Does it preserve replaceability, simplicity, and the boundaries declared in the relevant charter and ADRs?
2. **Security and Cryptography Gate** — Does the change preserve or improve the security posture, including cryptographic agility and, where declared, present-day post-quantum posture? Does it introduce new attack surface, downgrade primitives, or create key-management debt?
3. **Privacy and Metadata Gate** — Does the change respect metadata minimization, metadata resistance, avoidance of avoidable correlation, and unlinkability where the workflow permits and the product remains usable? Are any unavoidable linkabilities documented and justified? **This gate owns the seam between engineering identity and product identity** and must explicitly check that engineering-side identifiers (author, tooling, environment, model, build) do not leak into product-side artifacts, telemetry, or user-visible surfaces.
4. **Quality and Verification Gate** — Is there evidence the change does what it claims? Are tests, measurements, or reasoned arguments present and appropriate to the change's blast radius?

### Builder / evaluator separation

The producer of a change **cannot be its sole evaluator**. During Foundry 1, separation may be satisfied by:

- a different human reviewer;
- a separate AI model or intelligence operating in an evaluator role;
- a separate evaluation session that did not produce the change and is given the change packet, evidence, and applicable rubric;
- deterministic verification where the gate criterion can be evaluated mechanically;
- or an explicit combination of these.

The founder remains the final approval authority, but founder approval does not by itself substitute for independent gate evaluation when the founder produced the change. Naming the same person under two role labels on the same change does not satisfy this requirement.

### Failed gates block by default

- A gate result of **Fail** blocks merge by default.
- A gate result of **Pass with conditions** requires the conditions to be recorded and either satisfied before merge or explicitly deferred with a follow-up.
- A gate result of **N/A** is allowed only with a specific, recorded reason; it is not a shortcut around the gate.
- **Only an explicit, recorded founder override** may allow a change with a failed gate to proceed. An override does **not** turn a failure into a pass. The gate result remains Fail; the override records the accepted risk, the rationale, the follow-up, and the condition under which the decision will be reassessed.

### Engineering identity vs product identity

Engineering identity (who built it, with what tools, under what account, against which model) and product identity (what the product exposes to its users and to the world) are separate domains. Their conflation is a category of privacy failure. The Privacy and Metadata Gate owns detection of leakage across this seam.

### Gate authority and gate operation

The four-gate structure, the requirement that every applicable change receive all four outcomes, builder/evaluator separation, and failed-gate blocking are doctrinal commitments of Foundry 1.

The operation of each gate is evidence-dependent. Its rubric details, evaluator, prompts, tools, thresholds, calibration, cost, false-positive behaviour, false-negative behaviour, and continued mandatory status must be measured through real work.

A gate may be recalibrated, narrowed, or demoted when evidence shows that it is inaccurate, inconsistent, repeatedly bypassed, repeatedly overridden, missing defects within scope, or creating disproportionate cost.

A gate must not retain mandatory authority merely because it appeared in the original design.

### Proving ground

**Daang Remote is the first proving ground** for this contract. The first bounded Daang Remote change under Foundry 1 is also the first product-level test of the four-gate model.

### On moat

Execution — the ability to actually ship a metadata-minimizing, cryptographically agile product to personal-use excellence — is the present moat. Foundry is not itself the moat today. Foundry may compound that moat later if it demonstrably reduces the cost of subsequent products; that is a claim to be earned by evidence, not asserted here.

## Evidence

- Foundry 0 baseline: `CONSTITUTION.md`, `VERSION.md`, `README.md`, `foundry-templates/`, `product-charters/daang-remote.md`, merged via PR #1 and PR #2.
- Direct founder experience during Foundry 0 that (a) model swaps in practice required prompt and calibration changes to reach comparable output quality, and (b) sole-author review missed issues that a second reviewer would have caught.
- The Constitution's Principle 2 (Evidence), Principle 6 (Intelligence as replaceable), and Principle 7 (Human judgment), which this ADR amended in PR #3 to establish the Foundry 1 operating model.

Evidence for the specific calibration of each gate — thresholds, exemplars, false-positive/negative behaviour — will accumulate through use and is expected to drive later Operational ADRs.

## Consequences

**Easier:**

- Substantive changes have a uniform, recorded evaluation surface.
- Model swaps are legitimized as operational events with a known artifact cost, rather than as risks to doctrine.
- Privacy leakage between engineering and product identities has an explicit owner.

**Harder:**

- Every substantive PR carries four gate records and a builder/evaluator distinction. Trivial-looking changes must still show they are trivial.
- The founder can no longer act as sole author-and-evaluator by default; role separation must be named in each record.
- Overrides are visible and permanent in the record, which raises the cost of using them casually.

**Constraints on future work:**

- New ADRs that touch gate definitions must state whether they recalibrate, narrow, demote, or replace an existing gate, and must cite the evidence.
- Product charters and product-level ADRs are expected to reference the gates rather than invent parallel evaluation structures.

## Rollback

This ADR is Doctrinal and does not expire. It may be superseded by a later Doctrinal ADR that ratifies a different operating contract, but rollback is not routine: reverting to Foundry 0's implicit "founder is sole evaluator" model would require an explicit founder decision recorded as a superseding ADR, and would forfeit the evidence generated under Foundry 1.

Individual gates may be recalibrated, narrowed, or demoted via Operational ADRs without superseding this one, provided the four-gate structure and the builder/evaluator separation remain intact.

## Notes

- This ADR intentionally does not select transports, cryptographic primitives, agent frameworks, or automation. Those are downstream decisions.
- "Gates" here are a manual evaluation discipline. Foundry 1 explicitly does not introduce an automated gate runner, CI enforcement, or accumulated gate statistics; those may be proposed later on evidence.
