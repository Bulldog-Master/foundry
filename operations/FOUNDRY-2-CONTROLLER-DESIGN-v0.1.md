# Foundry 2 Controller Design v0.1

- **Status:** DESIGN ONLY — NOT AUTHORIZED FOR IMPLEMENTATION
- **Scope:** Product-neutral Foundry 2 control plane
- **Authority:** Subordinate to ADR-0003 if ratified, ADR-0001, ADR-0002, the Constitution, and frozen production baselines

## Purpose

Record the minimum architecture needed to implement Foundry 2 without making planning software the authority.

## Control flow

```text
Bulldog
  |
  | reserved acts / exceptions only
  v
Foundry Lead
  |
  | authorizes bounded work class / envelope
  v
Deterministic Controller
  |
  | validates every requested action
  v
Planner / Orchestrator (candidate: Hermes)
  |
  +--> Codex / repository workers
  +--> test / verifier workers
  +--> bounded Caller-1 interface
  +--> bounded Sandbox-1 interface
  +--> approved Standalone workers
  |
  v
Independent Security / Evaluation
  |
  | structured category/severity/verdict/routing
  v
Deterministic Controller
  |
  +--> permitted next step: continue
  +--> ordinary implementation defect: return to Operations
  +--> reserved act / ambiguity / integrity issue: STOP and escalate
```

## Work envelope

Every task must have a versioned, hashable envelope containing at least:

- task ID;
- product/workstream ID;
- authorized repository/host/workspace;
- permitted paths/resources;
- allowed actions;
- prohibited actions;
- required tests/verifiers;
- required review roles;
- evidence requirements;
- stop conditions;
- expiration or revision identifier where applicable;
- exact authority boundary;
- terminal state.

Hermes or any other planner may refine steps only within the envelope. It cannot add a new target, privilege, work category, reserved act, or trust boundary.

## Deterministic controller rules

The controller must independently reject:

- an action not explicitly allowed;
- any reserved founder act;
- missing or stale envelope identity;
- path or target outside scope;
- unexpected credential or capability request;
- missing required evidence;
- malformed structured review output;
- an evaluator result lacking the required routing fields;
- any action after a stop condition;
- any attempt to infer authority from prose.

The controller never treats Hermes output as authorization.

## Structured review result

Security/Evaluation results must include machine-readable fields:

```text
category
severity
verdict
routing
requires_human
evidence_refs
reviewer_identity
independence_record
```

The controller routes only on the frozen structured fields.

Examples:

- `IMPLEMENTATION_DEFECT / MAJOR / RETURN_TO_OPERATIONS`
- `TRUST_BOUNDARY_DEFECT / CRITICAL / HARD_STOP`
- `PASS / CONTINUE`
- `FOUNDER_RESERVED / ESCALATE`

Free-form explanation is retained as evidence but cannot override the structured route.

## Evidence and custody

Every operation produces a structured result packet with:

- operation ID and envelope hash;
- actor/executor identity;
- actions requested and performed;
- files/systems affected;
- test/verifier outputs;
- hashes of changed artifacts and relevant evidence;
- review status;
- routing decision;
- escalation/stop events.

Authoritative result records must be append-preserving and outside the sole write authority of the actor being governed.

## Trust boundaries

The controller, planner, workers, evaluators, Caller, Sandbox, and sealed-truth custody are separate roles. Co-location is allowed only when structural access controls still establish the required separation.

Hermes must never receive:

- founder signing keys;
- sealed truth;
- unrestricted Caller/Sandbox root;
- unrestricted provider credentials;
- authority to merge protected branches;
- production-promotion authority;
- founder-override authority;
- evaluator-assignment authority.

## Product neutrality

The controller schema is generic. Product-specific logic belongs in a product package that supplies:

- product charter;
- repositories/workspaces;
- product test suite;
- product-specific evaluator context;
- deployment/promotion policy;
- product secrets references;
- product-specific reserved resources.

ScoutProp may be the first proving ground, but no ScoutProp-specific assumption belongs in the generic controller.

## Implementation status

No controller code, Hermes adapter, automatic gate routing, or autonomous execution is authorized by this document. Implementation begins only after ADR-0003 is ratified and a separate commissioning scope is approved.
