# Foundry Constitution

- **Version:** 2
- **Originally ratified:** 2026-07-12 (record: PR #1)
- **Last amended:** 2026-07-13 (record: PR #3)

This document is the founder's pre-commitment about how work is done under Foundry. It binds the founder, the Foundry itself, every product built under it, and any intelligence — human or artificial — operating inside it.

It is authoritative from the moment it is ratified. It is amended only by explicit, recorded founder decision.

## Principles

### 1. Reality validates

Nothing in Foundry is true because it is written here. Claims about how the world works are validated by real engineering work, real product usage, and real outcomes. Documents describe reality; they do not create it.

### 2. Evidence

Two kinds of content live here and are treated differently.

**Ratifiable pre-commitments** — the principles in this document, the shape of the templates, the initial operating model, and any explicit founder ratification of a policy or charter — are authoritative because the founder ratifies them in advance. They do not require prior evidence. What they commit to is *how work will be done*, not *what has already been shown to be true about the world*.

**Operational claims** — ADRs asserting a technical outcome, lessons drawn from work, standards, measurements, and claimed improvements — must earn continued authority through evidence from real work. A ratifiable pre-commitment can be adopted on the founder's authority alone; an operational claim cannot. A claim that a gate catches a class of defect, that a mechanism preserves a privacy property, or that a change improves an outcome is operational and requires evidence, regardless of who authored it.

### 3. Products drive

Foundry exists to serve product work, not the other way around. Process, tooling, and doctrine are justified by the value they add to real products. When Foundry begins to consume more attention than the products it supports, that is a signal to simplify Foundry, not to expand it.

### 4. Every project improvement

Every project should, on completion or at meaningful milestones, contribute at least one verified improvement — a lesson, an ADR, a standard, or a change to Foundry itself — so that the next project starts from a stronger baseline than the last.

### 5. Doctrine vs policy

**Doctrine** is a durable commitment about how work is done. It changes rarely and only by explicit founder decision.

**Policy** is an operational choice about how doctrine is currently applied. It may change as reality changes.

ADRs and lessons must declare which they are. Confusing the two — treating a policy as doctrine or a doctrine as policy — is itself a governance failure.

### 6. Intelligence as replaceable

Any intelligence operating inside Foundry — human contractor, AI agent, tool, model, or platform — is treated as replaceable infrastructure. Foundry does not depend on the continued existence of any particular vendor, model, or assistant. Artifacts are authored so that a different intelligence, brought in later, can continue the work.

**Replaceable does not mean behaviourally equivalent, and does not mean zero retuning.** Swapping an intelligence is a supported operation, not a no-op. Prompts, adapters, calibration data, evaluation baselines, and thresholds are model-specific artifacts and are expected to change when the intelligence changes. Foundry's doctrine is model-neutral; Foundry's operation is model-specific. The cost of a swap is the cost of reproducing the model-specific artifacts to the same standard, not a claim that the new intelligence will behave identically.

### 7. Human judgment

Automated and AI-assisted work is welcome, but human judgment is the final authority. No doctrine change, lesson promotion, security exception, merge into a protected branch, **or override of a failed evaluation gate** occurs without explicit founder approval.

**The producer of a change cannot be its sole evaluator.** Independent evaluation may be satisfied by a different human reviewer, a separate AI model or intelligence operating in an evaluator role, a separate evaluation session that did not produce the change and is given the change packet and applicable rubric, deterministic verification where the criterion can be evaluated mechanically, or an explicit combination of these. Naming the same person under two role labels on the same change does not satisfy this requirement. The founder remains the final approval authority, but founder approval does not by itself substitute for independent gate evaluation when the founder produced the change.

### 8. Simplicity

Prefer the smallest thing that works. Add structure only when its absence has caused a real problem. Remove structure that has stopped earning its keep.

## Governance

During the current generation the founder is the sole ratifying authority. There is no artificial separation of powers. Human approval before merge is the primary safeguard, augmented by mandatory evaluation gates whose definitions live in ADRs. As Foundry matures, additional governance may be introduced through ADRs, but only in response to real operating needs.

## Responsible use

Foundry and any product built under it must not be used to:

- design, build, or operate weapons or systems intended to cause physical harm to people;
- target, surveil, deceive, manipulate, or discriminate against individuals or groups;
- produce products primarily intended to create, distribute, or commercialize explicit sexual content;
- circumvent laws or platform terms of service in the jurisdictions where the product operates.

Protective research, accessibility, and safety work — including work touching sensitive subject matter — are allowed when their purpose is protective, educational, or therapeutic rather than exploitative.

Any exception to this section requires an explicit, recorded founder decision.
