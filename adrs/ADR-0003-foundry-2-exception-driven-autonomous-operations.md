# ADR 0003: Foundry 2 exception-driven autonomous operations

- **Status:** Proposed
- **Type:** Doctrinal
- **Expires:** Does not expire
- **Date:** 2026-10-09
- **Author(s):** Bulldog-Master (founder), with AI-assisted coordination and independent review required before ratification
- **Related:** ADR-0001, ADR-0002, VERSION.md, operations/FOUNDRY-DELEGATION-AND-ESCALATION-v0.1.md, operations/PR-22-INTEGRITY-RECORD.md

## Context

Foundry 1 proved the four-gate operating contract, evaluator-independence doctrine, bounded execution infrastructure, Caller-1, Sandbox-1, and contained agent operations. It also exposed a coordination cost that now dominates routine work: the founder is still used as a transport and approval surface for operational steps that do not require founder judgment.

Foundry 2 addresses that operating mismatch. Its goal is not zero-human governance. Its goal is **autonomous by default, human by exception**.

Foundry 1 remains the frozen reference generation. Its production Caller-1 and Sandbox-1 baselines are not modified by this ADR.

## Decision

Foundry declares a proposed next generation, **Foundry 2**, whose standing operating model is exception-driven autonomous operations under the existing Constitution and ADR-0002 independence doctrine.

Foundry 2 preserves the four mandatory gates from ADR-0001, builder/evaluator separation, failed-gate blocking, and founder override semantics. It supersedes only Foundry 1's manual-only operating assumption: gate invocation, evidence collection, deterministic routing, remediation loops, and routine operational progression may be automated so long as authority boundaries, evaluator independence, and evidence integrity remain enforceable and auditable.

### Basis for declaring a new generation

`VERSION.md` states that a new generation is declared when operating reality has materially changed, including when automation of any part of the gate contract becomes appropriate on evidence, or when the current operating model has demonstrably stopped fitting the work. This ADR relies on both: the founder is being used as a transport and approval surface for non-judgment steps (PR #22 and its integrity record are a worked example), and Foundry 1's explicit exclusions (no orchestration layer, no adopted agent framework, no automated gate runner) cannot be relaxed silently.

Declaring the generation in this ADR is a proposal only. The evidence that automation is appropriate is produced by commissioning, and no automation is active until the founder activates it. Foundry 1's section of `VERSION.md`, including its exclusions, is not rewritten by this ADR.

### Autonomous-by-default operations

Foundry 2 may automate, within pre-authorized scopes:

- work intake and task decomposition;
- repository inspection and bounded implementation;
- testing and verifier execution;
- evidence capture, hashing, and retention;
- branch creation, commits, pushes, and pull-request preparation/update;
- invocation of independent evaluators for all required gates;
- structured collection of evaluator outcomes;
- deterministic routing of PASS / FAIL / PASS WITH CONDITIONS / N/A outcomes according to frozen policy;
- automatic remediation loops for ordinary implementation defects;
- status reconciliation and exception reporting.

Automation must fail closed on ambiguity, drift, malformed evaluator output, missing evidence, authority expansion, unresolved disagreement, or integrity anomalies.

### Founder-reserved acts

The following global acts are reserved to Bulldog and require a directly recorded founder act:

1. **Merge to any protected branch.** Unconditional: not limited to cases where a rule happens to require it.
2. **Production promotion**, including first activation of a new production runtime or production baseline.
3. **Signing and trust-root authority:** signing-key creation, use, rotation, revocation, or replacement; creation of any GitHub App private key or other trust-root credential; installation of a GitHub App or any expansion of its permissions or repository access.
4. **Foundry governance changes:** the Constitution; adoption or supersession of ADRs; `VERSION.md` generation or authority statements; gate definitions; this reserved-act list.
5. **Founder override of a failed gate or Security block.** The underlying FAIL remains recorded.
6. **Authority and trust-boundary widening:** any expansion of the reachable authority, credentials, systems, write paths, or privileged interfaces of an agent, controller, evaluator, planner, or infrastructure component. Creating a new work-envelope class (see below) is a widening.
7. **Unresolved evaluator or Security conflict** that frozen deterministic evidence cannot resolve.
8. **New secrets or provider authority:** a new provider; access by an actor to a new secret or credential class; material expansion of an existing provider authorization.
9. **Sealed-truth authority:** releasing sealed truth; changing who may access it; changing its custody, recovery, or adjudication authority.
10. **Authorization of a new Foundry product.** Foundry may prepare a charter automatically; adding a product to the governed portfolio is a founder decision.
11. **Exceptional destructive or irreversible action** with meaningful blast radius that is not already explicitly authorized by a frozen, tested operational procedure.
12. **Closing a hard stop** raised for an integrity anomaly, trust-boundary defect, or Security block, and resuming after a PAUSE/KILL. Ordinary implementation-defect remediation loops are not hard stops and are not reserved.
13. **Alteration, deletion, or retention-policy change of authoritative audit or evidence records.**

Product charters may add product-specific reserved acts without amending this ADR (for example contracts or legal commitments, spending above an approved envelope, public launch). A product charter may add reserved acts but may never remove or narrow a global one.

**Closed-list rule.** Any action that is not on the global list, not added as a product-specific reserved act, not stopped by a frozen fail-closed rule, and inside a controller-validated work envelope of a ratified class is automatable. Everything else is not.

**Directly recorded founder act.** A founder act is valid only if it is performed in the founder's own authenticated interactive session, or signed with a key held in founder custody that no agent, controller, or planner can use, and is recorded in a form that distinguishes it from agent-originated actions. No agent, controller, or planner may hold credentials for `Bulldog-Master` or `Bulldog-z`. Automated actors must publish under their own distinct identities. A second account controlled by the same human is neither an independent evaluator nor a founder act. The specific mechanism is selected and proven during commissioning; until it is, no Foundry 2 reserved act may be treated as satisfied.

No model, controller, workflow, timeout, default, silence, or retry may substitute for any reserved act.

Agents may draft founder-controlled fields only as `PENDING` or `BLOCKED`. They may never set or pre-complete approval, adoption, override, activation, promotion, or equivalent founder-attestation fields. After a founder act is directly recorded, an automated actor may mechanically reflect it without broadening or reinterpreting it.

### Evaluator independence and evidence

ADR-0002 carries forward unchanged.

The producer of a change cannot be its sole evaluator. Independence is determined by accessible state and authority, not account, session, or role labels.

An actor being governed must not be able to create, modify, select, suppress, or delete the sole authoritative evidence used to establish its own compliance.

Evaluator inputs, configuration, identity, exposure record, runtime, and outputs must be frozen and independently checkable where the evaluation requires it.

Malformed required output is a failure condition under the applicable frozen policy, not an invitation for retrospective interpretation.

Evaluator substitution, visibility sequencing, retry behavior, and runtime equivalence must be governed by versioned operational policy and fail closed when their preconditions are not met.

### Deterministic controller, untrusted planners

Foundry 2 separates authority enforcement from planning.

A deterministic controller enforces work envelopes, allowed actions, reserved acts, stop conditions, routing fields, and evidence requirements.

Planning or orchestration tools such as Hermes may decompose and sequence work only inside a controller-approved envelope. They are not governance authority and cannot widen their own scope.

Work envelopes are instantiated only from **envelope classes** that the founder has ratified. The Foundry Lead role may instantiate an envelope within a ratified class and may never create or widen a class. This keeps "authorized envelope" from becoming a path by which an AI coordination role expands authority incrementally.

Security and Evaluation return structured authoritative routing fields. The controller routes mechanically on those fields and must not infer authority from free-form prose.

### Publishing identities and review binding

Automated actors publish to GitHub only through their own distinct identities, such as a `foundry-evaluator` GitHub App for reviews and status checks and a separate worker identity for branches and commits. The evaluator identity is a publishing identity. Evaluator independence under ADR-0002 belongs to the evaluator invocation behind it, not to the account.

- The evaluator never holds the App private key. A separate deterministic publisher in the controller's trust root validates the review record and posts it.
- The controller, not the evaluator, constructs the independence record from observable invocation facts.
- A review record binds at least: PR number, exact head SHA, review-packet SHA-256, evaluator identity and model, evaluator configuration hash, independence record, four gate verdicts, finding IDs, category, severity, routing, `requires_human`, and review-artifact hash.
- The publisher refuses to post a PASS if the record's head SHA differs from the PR's current head. The head SHA is re-checked when a review is accepted and immediately before `FOUNDER_ACTION_REQUIRED` is emitted. A later push makes the review stale and triggers a fresh one.
- The evaluator identity must be unable to merge, push, create or update branches, modify branch protection, access secrets, or set founder-controlled fields. This is proven on a test PR during commissioning, not assumed from the permission list.

### Product-neutral operation

Foundry 2 is a reusable operating model for multiple products.

Product-specific prompts, environments, tests, schemas, and policies live in product charters or product-scoped operational artifacts. They must not be hard-coded into the generic Foundry 2 controller.

ScoutProp is intended to be the first real Foundry 2 proving ground after Foundry 2 itself is commissioned, but this ADR does not authorize ScoutProp or make it the sole product target.

### Reference infrastructure

Caller-1 and Sandbox-1 remain frozen Foundry 1 reference environments unless separately superseded through their own versioned baseline process.

Foundry 2 commissioning occurs on separate controller/runtime infrastructure or disposable clones. No Foundry 2 experiment may silently mutate frozen Production Baseline v1 environments.

## Evidence required before activation

Foundry 2 is not active merely because this ADR is merged.

Activation requires a commissioning record showing, at minimum:

- deterministic work-envelope enforcement;
- structural separation between routine operations and reserved authority;
- independent evaluator provisioning and evidence under ADR-0002;
- structured evaluator result schema and deterministic routing;
- stop-the-line behavior;
- result-record hashing and custody outside the governed actor's sole control;
- PAUSE/KILL or equivalent human emergency control;
- rollback/recovery procedure;
- shadow-mode evidence against real product work;
- proof on a test PR that the evaluator identity can post a review and status check but cannot merge, push, or alter protection, and that branch protection trusts the intended mechanism;
- proof that stale-head reviews are refused at publication and before founder notification;
- selection and proof of the founder-act mechanism, and proof that no automated actor holds founder credentials;
- ratified envelope classes for the first authorized workstream;
- explicit founder activation decision.

## Consequences

### Easier

- Routine Foundry work can proceed without repeated founder involvement.
- Evaluations can be invoked automatically while remaining independent.
- The founder is notified only at reserved acts or genuine exceptions.
- Multiple products can use the same product-neutral operating system.

### Harder

- The controller, evaluator environments, and evidence custody become security-critical infrastructure.
- Automation can amplify a bad policy quickly, so fail-closed boundaries and independent evidence become more important.
- Exposure and authority must be tracked mechanically rather than by conversational convention.

## Rollback

Before activation, rollback is deletion/reversion of the Foundry 2 proposal artifacts.

After activation, rollback means disabling Foundry 2 autonomous routing and returning affected workstreams to the frozen Foundry 1/manual path. Frozen Foundry 1 reference environments remain available as the recovery baseline.

## Ratification

This ADR is **PROPOSED** until Bulldog directly approves the reviewed PR that carries it. No agent may change this status to Accepted on Bulldog's behalf.
