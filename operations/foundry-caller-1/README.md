# foundry-caller-1 Production Record

## Purpose and scope

`foundry-caller-1` is the bounded production execution host for authorized
Run-008 evaluator jobs. It verifies a controller-signed job authorization,
invokes the hash-bound OpenAI adapter and evaluator configuration, validates
the structured evaluator response, assembles the production evidence package,
and requests publication through a separate root-owned sealing path.

This record preserves the production boundary that was commissioned on
2026-10-08. It is an Operational record subordinate to the Constitution and
ADRs. It does not grant gate authority or expand Foundry 1.

## Production status

Caller-1 is production-ready for the verified operating mode described here
and in `PRODUCTION-CONTRACT-v1.md`. Commissioning covered signed authorization,
root approval, live provider invocation, strict schema validation, evidence
package construction, root-owned sealing, terminal state recording, verifier
suites, and a non-destructive backup/restore drill.

Production-ready does not mean unrestricted automation. The commissioned
boundary is one authorized job at a time, started deliberately through the
static per-job systemd service. Parallel dispatch, queued dispatch, unattended
dispatch, and autonomous retry have not been commissioned and are not
authorized by this record.

The retired placeholder `foundry-caller.service` must remain disabled and must
not be enabled or started. Production jobs use `foundry-caller-job@.service`.

## Authority and separation

Caller-1 is an evaluator execution and evidence-custody component. It is not
the Foundry scoring, fusion, adjudication, governance, or founder-approval
authority. A `COMPLETE` Caller job means that execution, validation, evidence
packaging, and root-owned sealing completed; it does not mean that the
candidate received a green verdict.

Caller-1 is separate from `foundry-sandbox-1`. Neither host's credentials,
privileged services, state databases, or write authority belong on the other.
Future Caller-to-Sandbox integration must preserve that separation and requires
its own reviewed authorization and evidence-transfer boundary.

Caller-1 receives only the frozen evaluator packet and explicitly permitted
context. The sealed answer key, truth, rationales, repeat mapping, scoring, and
adjudication material are not evaluator inputs and must remain inaccessible to
Caller-1 and the provider.

## Repository contents

- `PRODUCTION-CONTRACT-v1.md` records the six frozen production decisions.
- `PRODUCTION-BASELINE.txt` records sanitized commissioning facts and hashes.
- `FILES.sha256` authenticates the three substantive files in this package.

This package contains no credentials, private keys, live database contents,
raw provider logs, evidence bundles, or sealed Run-008 truth.
