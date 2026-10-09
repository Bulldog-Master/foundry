# ADR 0003: Foundry 2 exception-driven autonomous operations

- **Status:** Proposed
- **Type:** Doctrinal
- **Expires:** Does not expire
- **Date:** 2026-10-09
- **Author(s):** Bulldog-Master (founder), with AI-assisted coordination and independent review required before ratification
- **Related:** ADR-0001, ADR-0002, VERSION.md, operations/FOUNDRY-DELEGATION-AND-ESCALATION-v0.1.md

## Context

Foundry 1 proved the four-gate operating contract, evaluator-independence doctrine, bounded execution infrastructure, Caller-1, Sandbox-1, and contained agent operations. It also exposed a coordination cost that now dominates routine work: the founder is still used as a transport and approval surface for operational steps that do not require founder judgment.

Foundry 2 addresses that operating mismatch. Its goal is not zero-human governance. Its goal is **autonomous by default, human by exception**.

Foundry 1 remains the frozen reference generation. Its production Caller-1 and Sandbox-1 baselines are not modified by this ADR.

## Decision

Foundry declares a proposed next generation, **Foundry 2**, whose standing operating model is exception-driven autonomous operations under the existing Constitution and ADR-0002 independence doctrine.

Foundry 2 preserves the four mandatory gates from ADR-0001, builder/evaluator separation, failed-gate blocking, and founder override semantics. It supersedes only Foundry 1's manual-only operating assumption: gate invocation, evidence collection, deterministic routing, remediation loops, and routine operational progression may be automated so long as authority boundaries, evaluator independence, and evidence integrity remain enforceable and auditable.

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

The following acts remain reserved to Bulldog and require a directly recorded founder act:

1. merge to a protected branch where the Constitution requires founder approval;
2. production promotion;
3. signing-key creation, use, rotation, revocation, or trust-root replacement where founder custody is required;
4. new secrets or provider-credential authority;
5. founder override of a failed gate or Security block;
6. amendment of the Constitution or durable doctrine;
7. authorization of a new Foundry product charter;
8. material widening of an agent, controller, evaluator, or infrastructure trust boundary;
9. release of sealed truth or material change to sealed-truth custody;
10. change to this reserved-act list.

No model, controller, workflow, timeout, default, silence, or second account controlled by the same human may substitute for these acts.

Agents may draft founder-controlled fields only as `PENDING` or `BLOCKED`. They may never set or pre-complete approval, adoption, override, activation, promotion, or equivalent founder-attestation fields.

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

Security and Evaluation return structured authoritative routing fields. The controller routes mechanically on those fields and must not infer authority from free-form prose.

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
