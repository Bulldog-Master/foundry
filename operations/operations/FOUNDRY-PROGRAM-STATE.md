# Foundry Program State

- **Type:** Operational coordination record
- **Status:** Current
- **Authority:** Subordinate to the Foundry Constitution, ADRs, frozen protocols,
  frozen production baselines, signed evidence, and merged authoritative records
- **Purpose:** Maintain a concise program-wide picture across Foundry workstreams
  so specialist work does not silently conflict, duplicate completed work, or
  redefine frozen boundaries.

This file is not doctrine, a protocol, a production baseline, or an approval
artifact. It summarizes current authoritative state and points to the records
that establish that state.

If this file conflicts with a newer frozen, signed, or merged authoritative
record, the newer authoritative record wins.

## Program leadership

Bulldog remains the final human authority for Foundry.

The Foundry Lead coordinates program state across specialist workstreams,
including sequencing, reconciliation, bounded handoffs, dependency tracking,
and conflict detection.

The Foundry Lead does not replace:

- founder approval;
- independent evaluation;
- merge authority;
- signing authority;
- sealed-truth custody;
- production promotion authority;
- frozen protocol or baseline controls.

## Current production/reference environments

### Caller-1

`foundry-caller-1` is commissioned and production-ready within its frozen
one-authorized-job-at-a-time operating boundary.

Caller-1:

- executes explicitly authorized evaluator jobs;
- uses signed controller authorization;
- operates through the commissioned per-job service path;
- performs provider invocation only within its frozen configuration;
- produces evidence through the root-owned sealing path;
- does not hold scoring, fusion, adjudication, governance, founder-approval, or
  sealed-truth authority;
- is not commissioned for parallel, queued, unattended, or autonomous-retry
  operation.

Caller-1 remains a separate trust domain from Sandbox-1 and from the
controller/trust root.

Authoritative records:

- `operations/foundry-caller-1/README.md`
- `operations/foundry-caller-1/PRODUCTION-CONTRACT-v1.md`
- `operations/foundry-caller-1/PRODUCTION-BASELINE.txt`

### Sandbox-1

`foundry-sandbox-1` Production Baseline v1 is frozen.

Current verified state:

- deterministic verifier: 57/57 PASS;
- no detected drift from Production Baseline v1;
- production baseline remains valid for Caller integration.

Production Baseline v1 must not be modified for experimental hardening work.

Future hardening work, including gVisor, Tetragon, escape-corpus testing,
hostile/resource-abuse testing, stronger network-attribution evidence, and
related experiments belongs to a disposable clone / Baseline v2 candidate.

Unconfined hostile escape or resource-abuse testing on production Sandbox-1
is prohibited.

Authoritative records:

- `operations/foundry-sandbox-1/README.md`
- `operations/foundry-sandbox-1/SECURITY-SCAN-FOLLOWUP.md`
- frozen Baseline v1 artifacts under `operations/foundry-sandbox-1/`

## Controller / trust root

Bulldog-Surface WSL is the temporary Foundry controller/trust-root environment.

The Caller authorization-signing private key belongs only on the trusted
controller/admin environment.

Caller-1 receives only the corresponding verification material required by its
frozen contract.

Sandbox-1 does not receive Caller signing keys or provider credentials.

Standalone is not the Caller signing trust root.

## Standalone / Hermes

Standalone remains a lab, evaluator, and development environment.

Hermes is external experimental tooling and is not Foundry governance.

Blinded evaluator work on Standalone must preserve the evaluator-isolation
requirements established by ADR-0002, including bounded accessible state,
separate evaluator environments, no sealed-truth exposure, and independent
authoritative evidence.

Authoritative operational record:

- `operations/hermes-lab.md`

## Evaluator independence

ADR-0002 remains authoritative.

Key invariants include:

- evaluator independence is determined by accessible state and authority, not
  role labels or fresh-looking sessions;
- a governed actor cannot control the frozen authoritative evidence used to
  establish its own compliance;
- independence claims require recorded, checkable evidence;
- prior exposure to intentionally withheld information disqualifies blinded
  evaluation for that execution;
- evaluators receive the minimum bounded context reasonably necessary.

The evaluator-independence protocol and applicable frozen experiment rules must
not be casually revised during implementation.

## Run-009

Run-009 is INVALID for protocol-integrity reasons.

Its outputs are exploratory / diagnostic only.

They must not be used to support:

- performance classification;
- evaluator-superiority claims;
- architecture adoption;
- permanent evaluator assignment;
- production-policy changes.

Missing sealed truth or other frozen artifacts must not be reconstructed from
memory or evaluator output.

Authoritative record:

- `experiments/run009-integrity-record.md`

## Protocol enforcement

The protocol-to-enforcement matrix records the controls required before any
future valid replication of the frozen dual-evaluator experiment.

The matrix is an implementation/preflight design artifact. It does not itself
authorize replication or redefine Foundry governance.

Authoritative record:

- `experiments/protocol-enforcement-matrix.md`

## Active workstreams

### Agent Containment & Control

Status: approved to resume.

Scope remains bounded to the approved Foundry execution/control environments.

The objective is to reduce manual operational friction while preserving human
approval, trust-domain separation, bounded authority, and independent evidence.

Contained agents must not gain standing authority over:

- signing;
- secrets;
- provider authorization beyond frozen mechanisms;
- destructive/security-sensitive changes;
- merges;
- production promotion;
- sealed truth.

### Candidate Admission

Status: next governance-layer work.

Candidate Admission should begin as a versioned operational protocol, not
doctrine.

The first intended admission case is deterministic-rule promotion.

The admission process itself should be proven before higher-impact candidates
such as persistent memory systems, orchestration frameworks, alternate
runtimes, or similar external mechanisms are considered.

Approval must remain version-bound to the component, configuration, runtime,
environment, and evidence that were actually tested.

## Deferred work

The following are deliberately deferred unless explicitly reopened:

- Sandbox Baseline v2 hardening experiments;
- gVisor comparison;
- Tetragon/equivalent host tripwire;
- hostile escape/resource-abuse campaign;
- controlled persistent-memory admission;
- larger orchestration/runtime admission candidates;
- broader unattended Caller dispatch;
- parallel Caller job execution.

Deferred work is not a defect in the current production baseline unless new
evidence identifies a genuine trust-boundary failure.

## Current program sequence

The current intended sequence is:

1. Preserve Caller-1 and Sandbox-1 as frozen reference environments.
2. Resume bounded Agent Containment & Control work.
3. Formalize Candidate Admission Protocol v0.1.
4. Use deterministic-rule promotion as the first admission test.
5. Reconcile lessons from that test before expanding the admission process.
6. Test shared-state isolation as a later candidate because of its direct
   relevance to evaluator independence.
7. Test controlled persistent memory separately.
8. Consider larger orchestration or runtime candidates only after the admission
   machinery has been proven.

## Change discipline

Update this record when a material program-level state changes, including:

- a production baseline is frozen, superseded, or invalidated;
- a trust boundary changes;
- a major workstream begins or completes;
- a candidate is admitted, rejected, or deferred;
- an authoritative protocol or ADR changes;
- a material dependency or blocker appears or is resolved.

Do not place secrets, credentials, private keys, sealed answer material,
repeat mapping, raw sensitive logs, live databases, or unrestricted evidence
bundles in this file.

Changes to this record do not themselves authorize the changes they describe.
The underlying authoritative approval or evidence must already exist.
