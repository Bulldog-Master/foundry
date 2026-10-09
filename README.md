# Foundry

Foundry is the operating system for how work gets built here.

It is not a documentation repository. Documentation is one of its outputs.

Foundry exists to make sure that every product built under it — starting with Daang Remote — is developed against a stable constitutional boundary, a disciplined decision record, verified learning, mandatory evaluation gates, and explicit human approval before change.

## Current generation: Foundry 1

Foundry 1 keeps the Foundry 0 foundation (Constitution, templates, one authorized product, human approval before merge) and adds a ratified four-gate operating contract for every substantive change. [`adrs/ADR-0001-model-neutral-foundry-boundaries.md`](./adrs/ADR-0001-model-neutral-foundry-boundaries.md) defines that contract, and [`adrs/ADR-0002-evaluator-independence-and-isolation.md`](./adrs/ADR-0002-evaluator-independence-and-isolation.md) extends its builder/evaluator separation with the durable independence standard. The current operating characteristics are described in [`VERSION.md`](./VERSION.md).

**Daang Remote is the first authorized product and the first proving ground** for the four-gate contract.

## The four manual gates

Every substantive change to a product or to Foundry itself is evaluated against four gates, recorded on the pull request:

1. **Architecture** — coherence with current architectural commitments and declared boundaries.
2. **Security and Cryptography** — security posture, cryptographic agility, and (where declared) post-quantum posture.
3. **Privacy and Metadata** — metadata minimization, metadata resistance, avoidance of avoidable correlation, unlinkability where the workflow permits, and explicit ownership of the seam between engineering identity and product identity.
4. **Quality and Verification** — evidence that the change does what it claims, appropriate to its blast radius.

Each gate result is one of **Pass**, **Fail**, **Pass with conditions**, or **N/A with a specific reason**. **A failed gate blocks merge by default.** Only an explicit, recorded **founder override** may allow a change with a failed gate to proceed, and an override does not convert a failure into a pass — it records accepted risk, rationale, follow-up, and reassessment.

The producer of a change cannot be its sole evaluator. Author and evaluator roles are named in the record, and independence is supported by recorded, checkable evidence appropriate to the evaluator arrangement under ADR-0002. A fresh conversation or separate role label is not sufficient by itself.

## Foundry 1 is manual and evidence-generating

Foundry 1 remains a manually governed discipline. It permits manual experimental run records, gate evidence, and statistics to accumulate and inform later decisions about automation, tooling, or additional structure. It has no CI enforcement, automated gate runner, automated statistics pipeline or dashboard, orchestration layer, or adopted agent framework.

External tools such as Hermes may support bounded experiments and evidence collection, but they are not Foundry itself and their use does not adopt them as a Foundry agent framework. Foundry remains the authoritative governance and evidence system.

`foundry-caller-1` is bounded production execution infrastructure for explicitly
authorized evaluator jobs; its commissioned boundary is recorded in
[`operations/foundry-caller-1/`](./operations/foundry-caller-1/). Caller-1 does
not replace or acquire authority over Foundry governance, scoring, fusion,
adjudication, founder approval, or sealed-truth controls.

A contained Foundry operational agent is commissioned for bounded implementation work; its current execution boundary is recorded in [`operations/foundry-agent/`](./operations/foundry-agent/). This does not automate Foundry gates or adopt a standing agent framework into Foundry doctrine.

## What Foundry contains

Foundry holds two kinds of content, and the distinction matters.

**Ratifiable pre-commitments** may exist before they have been exercised in anger:

- The **Constitution** — the founder's pre-commitments about how work is done here. It is authoritative from the moment it is ratified.
- **Templates** — blank forms for the kinds of artifacts Foundry produces (decisions, lessons, product charters). A template is a shape, not a claim.
- **Ratified product charters** — the founding document of each authorized product.

**Operational knowledge** earns continued authority through evidence from real engineering work:

- **Architecture Decision Records (ADRs)** — decisions made against real problems. Types are Doctrinal or Operational; Operational ADRs carry an expiry.
- **Lessons** — learning extracted from real work, promoted from Candidate to Verified only with evidence and explicit founder approval.
- **Operational records** — a narrow subtype of operational knowledge used to record current external tooling or environment state relevant to Foundry execution. They are subordinate to the Constitution and ADRs, carry no standing gate authority, and may become stale or be superseded as operating reality changes. A record of external tooling such as Hermes does not make that tooling part of Foundry architecture or adopt it as a Foundry framework.

## What Foundry is not

Foundry is not a wiki, a design system, a style guide, a process handbook, or a CI configuration. Content that is not a constitutional constraint, a blank template, a real decision, a real lesson from real work, a real product charter, or a narrowly scoped operational record does not belong here.

## Governance

See [`CONSTITUTION.md`](./CONSTITUTION.md). The Constitution governs Foundry. All other files are subordinate to it.
