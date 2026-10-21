# CA-001 Stage B harness preparation results

Status: implementation and producer mechanics checks only. No CA-001 evaluation
has run. Independent review remains with the other chat; no gate, admission,
integration, deployment or standing-operation approval is asserted.

## Source and scope

This increment adds the harness, controller capture, their mechanics tests and
this record. The [evaluation packet](CA-001-EVALUATION-PACKET-v1.md),
[trial plan](CA-001-deterministic-rule-promotion.md),
[protocol](PROTOCOL-v0.1.md), Stage A checker, twelve-case fixture and Stage A
test source remain unchanged. The packet SHA256 remains
`77031cfda7f240405ef6b211b16c7232c4336ad895b1468da9c5e8189e1362c4`.

The four exported implementation/test files are byte-identical to the sources
used for the producer checks. [STAGE-B-HARNESS-SHA256SUMS](STAGE-B-HARNESS-SHA256SUMS)
records their hashes and this note's hash. Source paths already specified in the
public packet are retained; private runtime state and concrete custody bindings
are not exported.

## Implemented behavior and limits

- `ca001_harness.py` prepares one pass with frozen source/runtime checks, strict
  JSONL integrity handling, the unchanged Stage A unit tests and comparison of
  the twelve frozen expected results. Only requested action and authorization
  are passed to the candidate; extra-field checks concern fixture representation,
  not a new authorization predicate.
- Its deterministic report uses fixture order and an untimed unittest result,
  rather than the timing-bearing CLI formatter. Raw pass streams are not
  normalized afterward. An absolute worker deadline bounds this no-subprocess
  worker; that is not OS isolation or independent cleanup proof.
- `Capture-CA001StageB.ps1` is designed to use the existing controller and direct
  unprivileged WSL path, not Codex/model execution. It binds frozen source,
  runtime/launcher and prerequisite receipts, transmits a checked controller-held
  harness copy, captures binary streams with limits, and compares reported
  results against the controller's frozen fixture.
- Capture is disabled without explicit execution arguments and bound inputs.
  Exclusive locking, receipt consumption, expiry, PAUSE reads, raw-stream hashes
  and retained failure records are implemented. The script never writes controller
  PAUSE/KILL state. Receipt authenticity and custody must be established outside
  this producer code; files and hashes alone are not founder authentication.
- The intended limits remain exactly two passes, 60 seconds and 1 MiB combined
  retained stdout/stderr per pass, with no automatic retries. An output overrun
  retains a bounded prefix and marks incomplete capture; it is not a valid pass.

These descriptions are implementation intent, not an end-to-end evaluation or
proof that every orchestration branch or host control has been exercised.

## Producer checks

| Check | Result | Coverage |
| --- | --- | --- |
| Python harness mechanics | 12 passed | Inert callbacks/suites and stand-in fixture data; deterministic bytes, malformed inputs, mismatches, source checks and default refusal |
| Windows capture mechanics | 9 passed | Seven inert subprocess cases plus byte hashing and path-traversal checks |
| Saved capture records | Receipts matched | Seven capture records and retained stdout/stderr sizes and hashes |
| Existing runtime inspection | Direct Python inspection succeeded | Account/interpreter facts only; not whole-runtime integrity or service health |

The nine capture checks cover raw stdout/stderr, nonzero exit, timeout, stdout
limit, stderr limit, combined limit, launch failure, byte hash and path traversal.
PowerShell parsed the capture source and loaded its library-only path. The actual
Stage B orchestration was not invoked. The Python checks did not import the real
checker or Stage A test module; stand-in results are not scored CA-001 outcomes.

Earlier file disappearance and launcher failures remain recorded privately.
Following operator-reported quarantine recovery, the known self-test bytes were
restored and their hash rechecked; the final nine checks passed. Earlier blocked
records and the first seven-check record were not rewritten as final validation.
No security settings were changed by this work.

Runtime inspection retained path-translation and user-session startup warnings.
No service repair was attempted. Those warnings must remain raw in any later
capture; no claim of healthy services or guaranteed cross-pass equality follows.

## Private producer receipts

| Record retained privately | SHA256 |
| --- | --- |
| Completed mechanics and runtime summary | `d0bc319cd4ead16ea4a9f6e40bd12ebaf4ed1177218f77b0eb26895ba992b827` |
| Final nine-check capture summary | `fba04143ed576d662612757c5d2e624537d2ccf559d7d24d6b79cb3d1e14d100` |

These receipts provide producer traceability, not signatures, independent custody
or gate outcomes. Raw logs, runtime/kernel versions and binary identities, concrete
machine/custody paths, approval receipts, credentials, SSH details, sessions,
databases, backups and protected material remain outside this increment.

## Remaining execution prerequisites

Before Stage B, resolve the packet's pre-execution items: staged frozen artifacts,
named reviewer/independence and independent expected-result confirmation, verified
controller evidence custody, relevant filesystem/network boundaries, exact
commands/environment and final external manifest/packet bindings. Then obtain
separate Stage B authorization for that exact tuple. The code is not wired into
a working integration and grants none of those approvals by itself.

## Safe preparation checks and rollback

The Python mechanics checks alone can be selected explicitly from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -p 'test_ca001_stage_b.py' -v
sha256sum -c STAGE-B-HARNESS-SHA256SUMS
```

Do not use unrestricted test discovery as a substitute: it would also run the
Stage A tests, which have not been executed under this preparation scope.
The Windows self-test script uses only inert processes and requires a new local
output directory. No execution command, authorized manifest or approval receipt
for the actual two-pass trial is supplied here.

Rollback is to leave these uninstalled files unused or revert an authorized
repository increment. There is no newly deployed worker or service to stop.
Existing integrations and earlier failure records remain unchanged. PRs
#42/#43/#44 and independent review are outside this update.
