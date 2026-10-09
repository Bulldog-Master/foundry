# Foundry 2 Commissioning Plan v0.1

- **Status:** DRAFT — NOT AUTHORIZED FOR ACTIVATION
- **Purpose:** Prove Foundry 2 safely before it becomes authoritative for product work

## Principles

- Foundry 1 remains the recovery/reference generation.
- Production Caller-1 and Sandbox-1 v1 stay frozen.
- Commissioning uses a separate Foundry 2 runtime/control plane or disposable clones.
- Shadow evidence precedes authority.
- Every stage has explicit pass/fail evidence.
- Founder-controlled fields remain pending until Bulldog acts directly.

## Stage 0 — Governance and design freeze

Required:

- ADR-0003 independently reviewed and founder-ratified;
- controller design hash recorded;
- reserved-act list frozen;
- work-envelope schema frozen;
- evaluator result schema frozen;
- rollback path documented.

No autonomous execution.

## Stage 1 — Controller preflight

Prove mechanically:

- out-of-envelope actions reject;
- reserved acts reject;
- stale/modified envelope rejects;
- path traversal/target substitution rejects;
- stop condition prevents continuation;
- result records are hashed and externally retained;
- PAUSE/KILL stops new work;
- controller cannot use founder signing or production-promotion authority.

Synthetic work only.

## Stage 2 — Evaluator independence preflight

For each evaluator arrangement:

- record accessible state and authority;
- record prior exposure;
- freeze effective configuration;
- verify no producer-controlled unauthorized retrieval path;
- prove evaluator cannot modify authoritative evidence;
- validate structured output;
- force malformed output and verify fail-closed handling;
- force runtime/config drift and verify invalidation.

No real product authority yet.

## Stage 3 — Shadow product workflow

Use real product work while Foundry 1/manual decisions remain authoritative.

Foundry 2 may:

- ingest an approved task;
- propose/decompose work;
- run workers in disposable or non-production scope;
- run tests;
- assemble evidence;
- invoke independent evaluators;
- produce routing decisions and a founder exception card.

It may not merge, promote, sign, or alter production.

Compare Foundry 2 decisions against the authoritative manual path and record divergence.

ScoutProp is the intended first shadow proving ground after its product charter is separately authorized.

## Stage 4 — Bounded autonomous operations

After Stage 3 passes:

- reversible routine work may proceed automatically inside versioned envelopes;
- ordinary implementation defects may loop back automatically;
- all required gate evaluators are invoked automatically;
- PASS paths may progress to the next non-reserved state;
- ambiguity, FAIL, drift, authority expansion, or integrity anomaly stops.

Protected-branch merge and production promotion remain founder-reserved.

## Stage 5 — Founder activation

Bulldog receives one consolidated activation packet containing:

- commissioned component versions/hashes;
- preflight results;
- shadow-mode results;
- divergence summary;
- unresolved limitations;
- independent review result;
- rollback procedure;
- exact authority being activated.

Only Bulldog may activate Foundry 2.

## Activation fields

| Field | State |
| --- | --- |
| ADR-0003 ratified | PENDING |
| Controller design reviewed | PENDING |
| Controller implementation hash | BLOCKED |
| Work-envelope schema | BLOCKED |
| Evaluator result schema | BLOCKED |
| Controller preflight | BLOCKED |
| Evaluator independence preflight | BLOCKED |
| Shadow ScoutProp run | BLOCKED |
| Rollback verification | BLOCKED |
| Founder activation | BLOCKED |

No agent may pre-complete these fields.
