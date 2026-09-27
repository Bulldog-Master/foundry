# ADR 0002: Evaluator independence as a property of accessible state and authority

- **Status:** Accepted
- **Type:** Doctrinal
- **Expires:** Does not expire
- **Date:** 2026-09-27
- **Author(s):** Bulldog-Master (founder), with AI-assisted coordination and adversarial cross-review during doctrine design
- **Related ADRs:** ADR-0001 (four-gate operating contract, builder/evaluator separation — this ADR extends its independence requirement rather than replacing it)

## Context

ADR-0001 established that the producer of a change cannot be its sole evaluator, and that naming the same person under two role labels does not satisfy that requirement. That was sufficient for Foundry 1's manual, human-and-single-model operation. It leaves an open question that only became concrete while designing a bounded pilot experiment (`experiments/dual-model-pilot-preregistration.md`) to test whether two independently isolated model evaluators produce genuinely complementary defect detection: **what makes an evaluator actually independent, once "evaluator" can mean a model invocation rather than a different human?**

Two gaps surfaced during that design work that ADR-0001 does not resolve:

- **A fresh-looking session is not evidence of independence.** A new conversation, a differently-named role, or a nominally separate invocation can still share retrieval paths with the thing it is evaluating — a persistent memory layer, a shared workspace, an inherited tool or connector, a document store the producer also wrote to. Foundry has no standing rule that names this as a failure mode, so nothing currently stops an evaluator from being independent in name only.
- **A governed actor can, in principle, manufacture the evidence of its own compliance.** If an evaluator can create, modify, select, or suppress the record that will be used to judge it — its own transcript, its own configuration, which candidate it sees, what history it is invoked against — then evaluator independence is not actually enforced, however the roles are labeled.

This ADR ratifies the durable doctrine that closes both gaps. It deliberately does not adopt any of the specific mechanics developed to operationalize it for a particular pilot: which models are used, how a terminal or orchestration environment is configured, sentinel generation, canonicalized-configuration hashing, or numeric thresholds. Those remain in the preregistration that motivated this ADR, because they are model-specific operational detail in exactly the sense ADR-0001 already distinguishes from doctrine, and are expected to change as intelligences, tools, and environments change. This ADR states only the principle that any such mechanics must satisfy.

## Decision

Foundry adopts the following as durable, model-neutral doctrine, extending ADR-0001's builder/evaluator separation:

### 1. Independence is a property of accessible state and authority, not of visible session separation

An evaluator is independent from a producer only to the extent that its judgment cannot be influenced by producer-controlled state **beyond the explicitly authorized evaluation inputs**, and the producer cannot alter the evaluator's authority, evidence sources, evaluation packet, or relevant environment once those inputs are frozen. This is not a rule against the evaluator seeing anything the producer created — an evaluator ordinarily must receive the candidate or change under review, and may legitimately need producer-authored tests, design documents, or evidence to do its job. The rule is about **unauthorized producer-controlled state outside the frozen evaluation inputs**, and about producer control over the evaluation environment after those inputs are fixed. A fresh conversation, an empty-looking context window, or a nominally distinct role assignment is not, by itself, evidence of this. **State isolation means eliminating unauthorized retrieval paths — not merely starting an empty conversation, and not refusing the evaluator the authorized inputs it needs to do its job.**

This applies uniformly regardless of what kind of actor is filling the evaluator role: a second human reviewer, a separate AI model, a separate session of the same model, or a deterministic mechanical check. The question is always the same one: *what hidden or persistent context can this invocation retrieve?* If that question cannot be answered with confidence for a given environment, that environment does not qualify as an independent evaluator, whatever it is called.

### 2. The evidence invariant

**An actor being governed must not be able to create, modify, select, or suppress the authoritative evidence used to establish that actor's own compliance, once that evidence has been frozen for the evaluation.**

The freeze boundary matters: a producer may legitimately have authored the candidate or change under review, and may even have contributed to a rubric before it was ratified — none of that is a violation on its own. What the evidence invariant forbids is the actor being judged retaining the power to **modify, replace, select, or suppress** the evaluation packet, rubric, sealed truth, or authoritative evidence set **after it has been frozen for that evaluation**. This generalizes ADR-0001's rule that founder approval does not substitute for independent gate evaluation when the founder produced the change. It extends the same logic to any producer-evaluator relationship Foundry recognizes, present or future: a model cannot be the sole author of the post-freeze record that will be used to score it, cannot choose after the fact which of its own outputs are presented for evaluation, and cannot retain write access to the sealed truth, rubric, or candidate set once those materials are frozen for the evaluation in question.

### 3. Independence must be verified, not assumed

Claimed isolation is not sufficient. Before any evaluator invocation is treated as independent, its independence must be supported by **recorded, checkable evidence appropriate to that evaluator arrangement** — not merely asserted by the evaluator, the producer, or whoever configured the environment. A model's own claim of freshness, on its own, is not that evidence, and neither is a role label.

This doctrine deliberately does not prescribe one universal verification mechanism. What counts as sufficient evidence depends on what kind of actor is filling the evaluator role and what retrieval paths are actually in question: a different human reviewer's independence is typically evidenced by organizational and access separation already outside this document's scope; a model invocation's independence may be evidenced by a record of its effective configuration and a probe designed to test a specific claimed retrieval boundary; some future arrangement may need a different form of evidence entirely. Any such technique — including archived configuration hashes and contamination probes, as used in `experiments/dual-model-pilot-preregistration.md` — is an operational implementation of this principle, adopted and refined where it is used, not a doctrinal requirement imposed uniformly by this ADR.

Whatever form the evidence takes, it must be honest about what it does and does not establish. A verification technique that can only rule out a specific, named class of contamination must say so, rather than being presented as a general independence guarantee it cannot support.

### 4. Prior information exposure, not job title, decides eligibility

A job title of "designer" or "coordinator" is not what disqualifies an actor from later serving as a blinded evaluator — **exposure to information intentionally excluded from the blinded evaluation packet is what disqualifies it, and that exposure cannot be cured by a later configuration or isolation check.** An actor exposed to sealed truth, specific candidates, or other information deliberately withheld from evaluators cannot later serve as a blinded evaluator for that same execution, regardless of how its environment is subsequently reset or verified: isolation checks establish the absence of unauthorized *retrieval* paths going forward, not the erasure of information an actor has already been told.

An actor that participated only in generic protocol design — reasoning about rules, thresholds, or mechanisms without exposure to sealed truth or specific candidates — is not disqualified by that participation alone, and may serve as an evaluator if its accessible state and prior exposure satisfy the same independence standard required of any other candidate evaluator. No actor's own recommendation about its continued role, scope, or necessity carries extra evidentiary weight for having been self-proposed; that judgment belongs to whoever holds final authority over the evaluation — for Foundry, the founder — informed by the recorded evidence of exposure and isolation, not by the actor's self-assessment.

### 5. Bounded, justified access — not necessarily a minimal packet

Evaluators receive the **minimum bounded context reasonably necessary to perform the evaluation** — not, as a matter of universal doctrine, only a tiny fixed packet of candidate, rubric, and permitted evidence. What is "necessary" depends on the gate and the evaluation: a narrow blinded pilot may need nothing beyond the candidate and rubric, while an Architecture evaluator may legitimately need the surrounding source tree, dependency graph, prior ADRs, or interface definitions to judge whether a change violates architectural commitments, and a human reviewer may need broad read access as a matter of course.

Broader source or repository access may therefore be included when the gate genuinely requires it. What must always be excluded is access that is not required for the evaluation and creates a contamination path anyway — unrelated history, sealed truth, producer-side state the producer could still alter, prior judgments on the same candidate, or other material irrelevant to the gate at hand. Any broader-than-minimal access granted to an evaluator must be justified as part of the independence record (Decision 3), not simply assumed convenient.

## Evidence

No empirical results exist yet under this doctrine — the pilot that motivated it (`experiments/dual-model-pilot-preregistration.md`) has not been executed. The evidence for this ADR is therefore the same kind ADR-0001 named for its own doctrinal commitments: founder ratification plus the reasoning that produced it, not manufactured empirical support. That reasoning was developed and adversarially cross-reviewed while specifying an actual evaluation protocol in detail — including a case where a model session's persistent memory layer created a self-blinding failure mode that a purely abstract discussion of "independence" would not have surfaced. The specificity of that design work is what justifies extracting a doctrinal rule now rather than waiting for pilot results; the pilot's numeric outcomes, when they exist, will bear on whether *dual-model cross-review* is worth adopting operationally — a separate and later question this ADR does not answer.

## Consequences

**Easier:**

- Future evaluator arrangements — additional models, additional environments, human-plus-model combinations not yet in use — can be checked against a single durable standard instead of requiring a bespoke independence argument each time.
- A design that turns out to leak evaluator independence (as the model-session memory case in the Evidence section did) has a named principle to catch it against, rather than relying on someone happening to notice.

**Harder:**

- Any future proposal to use a model or session as an independent evaluator must show recorded, checkable evidence appropriate to the retrieval paths actually in question, not just a role label. "It's a fresh conversation" is no longer, by itself, an adequate independence argument. What evidence is appropriate is chosen at the operational level (as the pilot preregistration does for this pilot), not fixed by this ADR.
- Convenience shortcuts — giving an evaluator broader repository or environment access than its task requires, on the grounds that it is simpler to provision — are now a named doctrinal violation rather than a judgment call.

**Constraints on future work:**

- Any ADR or operational proposal that introduces a new evaluator arrangement must state how it satisfies Decisions 1–5, or must explain why a given decision does not apply.
- The pilot preregistration remains the place where model-specific isolation mechanics live; amendments to those mechanics do not require amending this ADR, and amendments to this ADR's principles do not retroactively rewrite the pilot's frozen protocol.

## Rollback

This ADR is Doctrinal and does not expire. It may be superseded by a later Doctrinal ADR that ratifies a different independence standard, but rollback is not routine: superseding this ADR would return Foundry to ADR-0001's role/session-level separation (which already permitted a different human reviewer, a separate AI model, or a separate AI session as evaluator) without ADR-0002's explicit requirement to reason about accessible state, authority, and verifiable isolation. That reversion would need to be an explicit, recorded founder decision.

Nothing in this ADR is retroactive to work already merged under ADR-0001's original builder/evaluator separation; it applies going forward and to any evaluator arrangement adopted after this ADR's acceptance.

## Measurement or review trigger

This is a Doctrinal ADR; it is reconsidered on conditions, not a schedule:

- A class of contamination or independence failure that this doctrine did not anticipate — for example, a retrieval path or contamination mode that survives the verification evidence used to establish independence.
- Evidence from the pilot, or from any future evaluator arrangement, that the verification requirements in Decision 3 are unworkable in practice (too costly, too slow, or unable to be satisfied by any available environment) without providing real independence assurance in return.
- A change in operating reality — such as Foundry supporting evaluator arrangements this ADR's authors did not consider — that makes the doctrine as stated inappropriate or insufficient.

## Notes

- This ADR intentionally contains no candidate information, sealed-key material, sentinel or canary values, or any content specific to the pilot it was drawn from. It is written to remain valid whether or not that pilot's eventual result is PROMISING, FAIL, INCONCLUSIVE, or INVALID.
- The pilot's own numeric thresholds, fusion rules, and per-model isolation matrices are operational detail in the ADR-0001 sense and belong in `experiments/dual-model-pilot-preregistration.md`, not here. If a future Operational ADR proposes adopting a dual-model (or other multi-evaluator) architecture into Foundry's standing operating contract on the strength of replicated pilot evidence, it should cite this ADR for the independence principle it must satisfy, rather than restating it.
