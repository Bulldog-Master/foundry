# Foundry Version

This file describes the current maturity state of Foundry. It is not software semantic versioning.

## Proposed next generation: Foundry 2

Foundry 2 is proposed in `adrs/ADR-0003-foundry-2-exception-driven-autonomous-operations.md`.

Until ADR-0003 is independently reviewed and explicitly ratified by Bulldog, **Foundry 1 remains the current authoritative generation** and no Foundry 2 automation is activated.

Foundry 2's target operating model is autonomous-by-default, human-by-exception. It preserves the Constitution, the four mandatory gates, failed-gate blocking, and ADR-0002 evaluator independence while allowing routine operational execution, gate invocation, evidence collection, deterministic routing, and remediation loops to be automated inside frozen authority envelopes.

Foundry 2 is product-neutral and intended to support multiple authorized products over time. ScoutProp is the intended first real proving ground after Foundry 2 commissioning and separate product authorization; it is not the sole product target.

### Founder-reserved acts

The proposed Foundry 2 reserved acts are defined normatively in ADR-0003. They remain unavailable to automated agents/controllers.

### Activation

Foundry 2 is not activated by this proposal or by design documents alone. Activation requires the commissioning evidence and direct founder activation described in `operations/FOUNDRY-2-COMMISSIONING-v0.1.md`.

The Foundry 1 section below is unchanged from `main` and remains the authoritative description of the current generation, including its explicit exclusions and the generation-change rule, until Foundry 2 is ratified and activated.

## Current generation: Foundry 1

Foundry 1 ratifies the four-gate operating contract on top of the Foundry 0 foundation. See [`adrs/ADR-0001-model-neutral-foundry-boundaries.md`](./adrs/ADR-0001-model-neutral-foundry-boundaries.md) for the doctrinal basis.

### Operating characteristics

- **One founder.** The founder is the sole ratifying authority.
- **One authorized product.** Daang Remote is the only product currently developed under Foundry.
- **Four mandatory manual gates on every substantive change:**
  1. Architecture
  2. Security and Cryptography
  3. Privacy and Metadata (owns the engineering-identity / product-identity seam)
  4. Quality and Verification
- **Failed gates block by default.** A gate result of Fail blocks merge; Pass with conditions requires recorded conditions; N/A requires a specific recorded reason.
- **Explicit founder override only.** A failed gate may only be bypassed by an explicit, recorded founder override that names the accepted risk, rationale, follow-up, and reassessment condition. An override does not convert a failure into a pass.
- **Builder / evaluator separation.** The producer of a change cannot be its sole evaluator. Roles and the independence basis must be recorded under ADR-0002; accessible state, prior exposure, control of frozen authoritative evidence, authorized context, and evidence limitations matter more than nominal session separation.
- **Manual gate evidence and measurement.** Gate records are authored by hand and reviewed by hand. Gates themselves generate evidence about their own value: what they caught, what they missed, what they cost.
- **Bounded Lane A operational delegation.** After the founder adopts the delegation record and its prerequisites are satisfied, a contained agent may execute pre-authorized, reversible operational work inside Lane A. This delegation is procedural execution only. It does not transfer judgment, approval, or governance authority, and it is subject to the structural firewall, independent verification, sampling, exposure tracking, stop-the-line, and record-retention controls in [`operations/FOUNDRY-DELEGATION-AND-ESCALATION-v0.1.md`](./operations/FOUNDRY-DELEGATION-AND-ESCALATION-v0.1.md).
- **Model-neutral doctrine, model-specific operation.** Constitution, ADRs, charters, and gate definitions do not name a specific model. Prompts, adapters, calibration data, baselines, and thresholds are model-specific and are expected to change when the intelligence changes.
- **First proving ground.** The first bounded Daang Remote change under Foundry 1 is also the first product-level test of the four-gate model.

### Explicitly out of scope for Foundry 1

- No automation of gates.
- No CI enforcement of gates or of Foundry structure.
- No Foundry orchestration layer.
- No adopted Foundry agent framework.
- No automated gate runner.
- No automated statistics pipeline or dashboard. Experimental run records, gate evidence, and statistics may accumulate manually through use.
- External experimental tooling, including Hermes, does not change the Foundry generation and is not an adopted Foundry agent framework.

The Lane A delegation above is not an exception to these exclusions. No agent,
controller, model, script, workflow, or other automated mechanism may exercise or
decide gate routing; evaluator assignment or sequencing; visibility-release
decisions; scoring; fusion; adjudication; founder overrides; production
promotion; or any other governance authority. Lane A may prepare information
and proposals for an authorized human decision-maker, but it may not make,
approve, imply, or execute the decision.

These may be proposed later, on evidence, via new ADRs. They are not permitted to be introduced silently.

### When a new generation begins

A new Foundry generation is declared only when operating reality has materially changed — for example, when Foundry supports more than one authorized product, when the founder is no longer the sole operator, when automation of any part of the gate contract becomes appropriate on evidence, or when the current operating model has demonstrably stopped fitting the work.

Growth of content inside Foundry — more ADRs, more lessons, more product milestones — does not by itself constitute a generational change.
