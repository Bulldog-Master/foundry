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

The initial export matched the sources used for the original producer checks.
The readiness follow-up below distinguishes subsequent capture changes and checks.
[STAGE-B-HARNESS-SHA256SUMS](STAGE-B-HARNESS-SHA256SUMS) records the current
implementation/test hashes and this note's hash. Source paths already specified in the
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

## Initial producer checks

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

## Readiness follow-up

The seven evaluation-source files were staged in the packet's disposable work
directory and hash-verified against the published source snapshot. The checker,
fixture, Stage A tests and Python harness remain unchanged and unexecuted.

Native inert probes exposed two capture defects: quoting simple launcher flags
prevented a WSL command from reaching Python, and an asynchronous stdin write
leaked a task-result object into the PowerShell return stream. The capture helper
now leaves simple arguments unquoted, still escapes quoted arguments, and
suppresses the unused task result. Regression checks cover argument serialization
and the single capture-record return type.

The proposed execution prefix also pins the already-installed isolation tool by
hash and uses a fixed temporary namespace profile. The profile exposes read-only
runtime directories, a writable disposable work directory, a read-only root and
a separate network namespace. Inert probes observed only loopback, no default
IPv4 route, no effective capabilities, no-new-privileges enabled, and denial of
an attempted write outside the work directory. No packages, host settings,
permissions, containers or services were changed. These observations are bounded
producer checks, not an independent isolation certification.

| Follow-up check | Result | Coverage |
| --- | --- | --- |
| Python harness mechanics | 12 passed | Same stand-in-only suite; no real checker or Stage A test imports |
| Windows capture mechanics | 11 passed | Original nine cases plus argument serialization and fixed isolation profile; process cases check the single-record return type |
| Isolated inert execution prefix | Two commands exited zero | Hash-pinned launcher, stdin forwarding, unprivileged identity and loopback-only interface observation; no candidate or test execution |
| Raw prefix output comparison | Stdout identical; stderr differed | One invocation included an intermittent WSL user-session startup warning; both streams retained without filtering |

Raw-stream repeatability therefore remains an open readiness issue. The strict
comparison is unchanged: a later authorized evaluation with different raw streams
must be retained as failed or invalid, not normalized into a pass. Earlier
launcher failures, task-result diagnostics and an inert-probe newline mismatch
remain preserved; the probe input was corrected without changing candidate data.

Controller ACL observations were collected read-only. They do not designate a
final evidence root or establish independent custody. The controller remains
PAUSE, and no execution receipt or evaluation attempt was created.

## WSL startup investigation

Scoped diagnostics found the user-session manager failed with result `resources`,
an absent user-session bus, and startup logs reporting `Failed to spawn executor:
Device or resource busy`. The unit's cgroup has enabled controllers and a populated
child containing process IDs invisible in the distribution's PID namespace.
Read-only metadata from the existing Ubuntu distribution identifies the two
members as its running user manager and PAM process. This establishes a shared
cgroup ownership conflict, without proving the complete WSL/systemd defect or
its repair. It is not evidence of a Python
timeout or a candidate failure. Microsoft documents that WSL waits on a systemd
user-session startup during launch ([WSL systemd documentation](https://wsl.dev/technical-documentation/systemd/)).

The separate path-translation warnings came from inherited Windows path exports
being processed before Linux `env -i`. The capture helper now explicitly clears
`WSLENV` only in its WSL child's environment, records that policy in the capture
receipt, and leaves its parent environment and host configuration unchanged.
A new inert regression verifies that behavior and parent preservation. The final
mechanics checks passed 12 Python and 12 Windows cases; no checker or Stage A
tests ran. Two isolated inert prefix commands exited zero with matching stdout
and no path-translation warnings, but differing raw stderr: the first retained
the user-session startup warning. At that diagnostic stage, the primary startup
failure remained unresolved; the approved repair is recorded below.

During diagnosis no cgroup was cleared, process killed, user manager started or restarted,
delegation/permission changed, or WSL distribution restarted or upgraded.
Enabled user units include sockets and timers, so starting the manager is not
assumed harmless or equivalent to running a single inert command. Repair needs
a host-maintenance scope that protects the identified Ubuntu session and any
other affected workloads. Warning suppression, raw-stream filtering, UID changes and
disabling systemd or containment are not substitutes for that repair.

The original failures and diagnostic captures remain retained privately. They
are not relabeled as successful repair or evaluation evidence.

## Approved WSL repair and final preparation checks

After explicit maintenance-window approval, one root-owned, distribution-local
drop-in was created at
`/etc/systemd/system/user@1000.service.d/50-foundry-agent-wsl-slice.conf`:

```ini
[Service]
Slice=user-1000-foundryagent.slice
```

The installed file also contains two explanatory comments. Its SHA256 is
`1f3b4f3c0067412109842a48c35bcf3c68125e58b2924b2e6a01892b96f7496d`.
The dedicated child slice remains below the existing user slice, preserving its
ancestor resource limits. The service's delegation, task, memory and CPU settings
were checked before and after; none changed. The vendor unit, WSL configuration,
execution identity, existing filesystem permissions and Foundry approvals were not changed.
The placement mechanism follows systemd's documented slice hierarchy
([resource-control reference](https://freedesktop.org/software/systemd/man/latest/systemd.resource-control.html)).

Unit validation passed, the local service manager reloaded its unit definitions,
and the previously unavailable user manager started in its dedicated group. A
guarded restart terminated only `Foundry-Agent`, after checking that no additional
account workload was observed. A fresh unprivileged launch restored the user
manager and session bus with the override intact. Ubuntu's active user-manager
PID and control group were identical before and after; Ubuntu was not terminated.
No existing shared cgroup was cleared or its foreign processes killed.

| Final preparation check | Result |
| --- | --- |
| Python harness mechanics | 12 passed; stand-ins only |
| Windows capture mechanics | 12 passed; inert subprocesses and pure helpers |
| Isolated prefix after repair and after restart | Each two-command set exited zero with matching raw stdout/stderr; all four stderr streams empty |
| Cold-start health | Dedicated group, active user manager, session bus and unchanged ancestor limits verified |
| Source and runtime pins | Seven existing source files and runtime identity reverified; no source files added or replaced |
| Temporary isolation | Inert outside-write denial, loopback-only network, no default IPv4 route, zero effective capabilities and no-new-privileges reverified |
| Controller | PAUSE unchanged; custody observations remain producer-only |

The first maintenance guard rejected an inactive fresh-boot unit before any file
write; the guard was adjusted to accept `failed/resources` or `inactive/success`
only when no main process was running. An early health check observed an inactive
manager and failed before restart verification. Both records remain preserved,
alongside the original startup failures. Subsequent successful checks do not
rewrite those earlier records or prove every possible host state.

Rollback of the host repair requires a separate controlled maintenance action
to retire only this drop-in and reload/restart the affected environment. It must
not clear the shared group, disable delegation or change the account's UID.
No rollback, package upgrade, global WSL shutdown, integration change or standing
Foundry worker activation occurred. No checker, Stage A tests or Stage B pass ran.

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

The observed startup/repeatability fault is repaired and producer preparation
checks are complete. Before Stage B, name the reviewer and record independence
and independent expected-result confirmation, designate and verify
controller evidence custody, and freeze the final source, capture, isolation,
commands/environment and external manifest/packet bindings. Source staging and
inert boundary checks do not resolve those reserved freeze items. Then obtain
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
