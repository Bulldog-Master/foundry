# Foundry Controller v0.1 Design

> **DESIGN ONLY — NOT AUTHORIZED FOR IMPLEMENTATION**

- **Type:** Non-authoritative design note
- **Status:** DESIGN ONLY — no build, deployment, integration, or operating authority
- **Purpose:** Describe a possible deterministic Lane A controller without automating governance

## Boundary

This design is subordinate to the Foundry Constitution, ADRs, `VERSION.md`, and
`FOUNDRY-DELEGATION-AND-ESCALATION-v0.1.md`. It describes a possible mechanism;
it does not authorize its implementation or prove it safe.

The controller would operate only in Lane A. It would have no credentials,
permissions, endpoints, or fallback path for Lane B governance functions. It
would stop when a requested action is absent from, ambiguous within, or outside
the exact pre-authorized envelope.

## Deterministic action validation

The controller validates every proposed action before execution. Validation is
mechanical against a version-bound envelope: exact action, target, actor,
capability, input/artifact hashes where applicable, environment, limits,
expiry, prerequisites, and declared stop conditions. No action is allowed by
analogy, intent inference, model confidence, generic instructions such as
“proceed,” or prior authorization for a different action.

Validation produces a structured allow/stop result and an append-preserved
record. It does not decide whether the work is desirable, safe enough, or
governance-compliant; those remain Lane B judgments.

## Hermes decomposition

Hermes may decompose work only inside the exact pre-authorized envelope. Every
decomposed step must independently pass the same deterministic action
validation before execution. Decomposition cannot add targets, capabilities,
privileges, data access, retries, time, or side effects. If the work cannot be
completed without widening the envelope, the controller stops and escalates.

Hermes remains external tooling. It does not become Foundry governance, an
evaluator, or an authority source through this design.

## Structured reviewer outputs

Security and Evaluation components return data only in a versioned structured
schema. At minimum, each finding contains:

- finding category;
- severity;
- routing field supplied by the reviewer, limited to record, notify the single
  pre-authorized human intake point, or stop;
- evidence/result-record references;
- component and rule-set version; and
- integrity/error state.

Category, severity, and routing fields are retained and displayed as reviewer
output; the controller does not derive one from another and does not treat any
of them as governance authority. Free text may accompany a finding as
explanation, but it is never executable authority. Missing, malformed,
conflicting, or unknown structured fields fail closed.

## Mechanical routing only

The controller has one invariant, pre-authorized human intake destination. From
an authenticated, schema-valid structured routing field it may only record,
notify that same intake point, or stop the line. It does not choose a gate,
evaluator, sequence, review path, governance destination, or decision-maker.
The human Lane B actor performs all governance routing after receipt. The
controller never interprets review prose, summaries, model reasoning, tone,
absence of objections, or confidence language as authority. It cannot assign
evaluators, sequence gates, release visibility, score, fuse, adjudicate, approve
an override, merge, promote, or otherwise exercise governance.

No route may convert a reviewer finding into approval. No default or timeout may
be treated as consent. Any route requiring judgment terminates at the named
human decision point.

## Evidence and verification hooks

A future implementation would have to emit the operation, exposure, validation,
routing, and result records required by the delegation policy; preserve their
hashes outside the controller's sole control; support independent pre-launch
firewall verification; and support first-10, random-sample, mandatory-event,
stop-the-line, and independent-closure verification.

## Non-authorization

This document authorizes no code, configuration, credential, service, workflow,
deployment, trial, or change to Caller-1, Sandbox-1, Standalone, the contained
agent, or production infrastructure. Implementation requires a separately
bounded proposal, independent four-gate review, founder approval, and any other
applicable authorization.
