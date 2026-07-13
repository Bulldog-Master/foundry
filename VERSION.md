# Foundry Version

This file describes the current maturity state of Foundry. It is not software semantic versioning.

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
- **Builder / evaluator separation.** The producer of a change cannot be its sole evaluator. Roles must be named in each record.
- **Manual gate evidence and measurement.** Gate records are authored by hand and reviewed by hand. Gates themselves generate evidence about their own value: what they caught, what they missed, what they cost.
- **Model-neutral doctrine, model-specific operation.** Constitution, ADRs, charters, and gate definitions do not name a specific model. Prompts, adapters, calibration data, baselines, and thresholds are model-specific and are expected to change when the intelligence changes.
- **First proving ground.** The first bounded Daang Remote change under Foundry 1 is also the first product-level test of the four-gate model.

### Explicitly out of scope for Foundry 1

- No automation of gates.
- No CI enforcement of gates or of Foundry structure.
- No orchestration layer.
- No agent framework.
- No automated gate runner.
- No accumulated gate statistics or dashboards.

These may be proposed later, on evidence, via new ADRs. They are not permitted to be introduced silently.

### When a new generation begins

A new Foundry generation is declared only when operating reality has materially changed — for example, when Foundry supports more than one authorized product, when the founder is no longer the sole operator, when automation of any part of the gate contract becomes appropriate on evidence, or when the current operating model has demonstrably stopped fitting the work.

Growth of content inside Foundry — more ADRs, more lessons, more product milestones — does not by itself constitute a generational change.
