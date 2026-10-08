# Caller Production Contract v1

- **Status:** Frozen and commissioned
- **Applies to:** `foundry-caller-1`
- **Commissioned operating mode:** one authorized job at a time
- **Date frozen:** 2026-10-08

These six decisions are the production contract. Implementation details may be
repaired without changing the contract, but expanding authority or operating
mode requires a new reviewed contract version.

## Decision 1 — Provider and evaluator bindings are explicit and immutable per job

Caller accepts only a signed manifest that names the approved provider,
provider adapter, evaluator configuration, and candidate artifact together
with their required SHA-256 bindings. Caller re-verifies those bindings before
invocation. The production adapter is restricted to HTTPS, `api.openai.com`,
TCP 443, `/v1/responses`, `POST`, no redirects, and bounded timeouts. The
Run-008 evaluator has no tools and receives only the frozen permitted packet.

## Decision 2 — Every job requires a short-lived signed authorization

The controller authorizes a job with an Ed25519-signed manifest containing a
unique job ID and nonce and a maximum five-minute first-submission validity
window. Acceptance verifies the signature, schema, time window, exact bound
configuration and candidate hashes, persists the exact manifest bytes, and
atomically consumes the job ID and nonce so replay or ambiguity fails closed.

## Decision 3 — Invocation requires independent root authorization

Acceptance alone cannot invoke a provider. The unprivileged Caller stages the
accepted authorization through a fixed inbox. A root-owned processor validates
that record independently and publishes a job- and manifest-hash-bound
`AUTHORIZED` result. `ACCEPTED` may transition to `INVOKING` only when that
matching root result exists. Caller receives no general root command authority.

## Decision 4 — Provider output is strictly validated before success

Caller preserves the raw provider response, accepts only a completed provider
response, extracts the evaluator result, and validates it against the bound
strict response schema. Refusal, incomplete output, HTTP/provider failure,
malformed output, schema mismatch, endpoint mismatch, redirect, timeout, or
credential failure is a failed execution and must not be reported as success.

## Decision 5 — Evidence publication is complete, bound, and root-owned

Caller builds the required production evidence package with the authorization
manifest, frozen evaluator input, provider request and response, evaluator
result, effective configuration, execution record, job-state history, and
package manifest. Every payload is size-limited and hash-recorded. A root-owned
validator and sealer verify the package, authorization, state, and bindings and
publish an immutable bundle. Caller cannot select an arbitrary source or
destination, modify the sealer, or write a published bundle.

## Decision 6 — State, authority, and operating scope fail closed

Job history is append-only and monotonic. `ACCEPTED` transitions only to
`INVOKING` or terminal `FAILED`; `INVOKING` transitions only to terminal
`COMPLETE` or `FAILED`. `COMPLETE` requires a matching root `SEALED` result and
published bundle; it means transaction and validation completion, not a green
evaluation verdict. A failed or abandoned consumed authorization is terminal,
and retry requires a new signed authorization. Production operation is one job
at a time under deliberate operator dispatch. Parallel or unattended dispatch,
autonomous retry, scoring, fusion, adjudication, and sealed-truth access are
outside Caller-1's commissioned authority.
