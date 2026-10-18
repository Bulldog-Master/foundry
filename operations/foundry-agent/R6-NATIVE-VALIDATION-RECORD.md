# R6 Native Validation Record

## Status

`R6 NATIVE VALIDATION PASS`

Independent adjudication completed on 2026-10-18 for the exact corrected R6
candidate identified below. All eight authorized Linux validation modes passed
on the recorded disposable WSL2 environment.

This is an operational evidence record. It does not authorize production use,
deployment, promotion, or a broader platform claim.

## Candidate identity

| Artifact | SHA-256 |
|---|---|
| Corrected candidate archive | `3cc05f442629cf5173ffcf5a1482ddd1375418a054108710cba72dacae6228e7` |
| Package manifest | `c143973b7e5179cc9b70db746bb9ac445c49d16558455015e38bae237dbd3104` |
| Source manifest | `5bd46f3b84a838ab4151bd9ae498b057bcbf5aa4a44c7007fd5ff6511d63df4f` |
| Detached verification receipt | `752da6c033319aebe8952d474934802a8784380e0af7dd9e78601434c2620f68` |
| systemd unit | `9415e40dd59feccb9ebe03e54810651fbc334feb0dfc16194557eced905d989a` |
| Supervisor | `3763a0720477700007108eb7175127fa7ceb2636fb06788cc5c00ebea01c6650` |
| Native Linux driver | `7ab59a1124370a13893745af00ae0ce2b8ab32f1aa675f6f3ad355bbe5f1eed4` |
| Evidence recorder v4 | `7008f455b90e65f9083397ec0ac05f42eca3402a3036c4e949f1a00ab15a391a` |

The former candidate archive identity
`63b823c40467e2343973e61977381769e68843c26d464a9bde650007fed0da87`
is superseded for future native-validation work. Evidence produced for that
former candidate was not relabelled.

## Recorded environment

- disposable distribution: `R6-Disposable-227443978ae3752a-P01`;
- WSL: 2.7.12.0, WSL2;
- kernel: `6.18.33.2-microsoft-standard-WSL2`;
- distribution: Ubuntu 26.04.1 LTS;
- systemd: 259, running as PID 1;
- Python: 3.14.4;
- cgroup v2 mounted at `/sys/fs/cgroup`;
- worker account: `foundry-agent`, UID/GID `1000:1000`;
- Windows drive automount and Windows interop disabled;
- clone network mode isolated with no default IPv4 or IPv6 route.

The disposable distribution was unregistered after adjudication. The original
`Foundry-Agent` distribution remained preserved and stopped.

## Authorized mode results

| Mode | Result |
|---|---|
| `stop` | PASS |
| `leader-exit` | PASS |
| `detached` | PASS |
| `escaped-group` | PASS |
| `worker-loss` | PASS |
| `ipc-loss` | PASS |
| `timeout` | PASS |
| `supervisor-failure` | PASS |

`windows-client-death` was excluded by the frozen charter and was not run.

## Acceptance claim satisfied

For this exact candidate and recorded environment, the evidence established
that every authorized mode:

- contained its processes within the intended systemd/cgroup boundary;
- transitioned the worker to the required nonroot identity and security
  restrictions;
- reached an accepted terminal state within the frozen 30-second bound; and
- cleaned up the tested unit, processes, cgroup membership, runtime socket and
  lock within the frozen 30-second cleanup bound.

Transient workers were adjudicated under the separately accepted
fresh-challenge READY and kernel `SCM_CREDENTIALS` policy. The `timeout` mode
also captured the worker live and directly confirmed its UID/GID, cleared
supplementary groups, zero capability sets and `NoNewPrivileges=1`.

## Evidence identity

| Record | SHA-256 |
|---|---|
| Final eight-mode manifest | `d47bc236331d12851042d07dce75ad7ea69c45f1077119c2663fe1dc0fd1b25d` |
| Final eight-mode evidence set | `f505cea72a188c5e18bd1dcaacf9a679d71dda5644b4e928a13c10293ce85722` |

The complete evidence set remains in operator-controlled custody outside the
disposed clone. Raw evidence is not committed to this repository.

## Scope and limitations

This PASS applies only to the exact candidate and recorded environment above.
It does not independently certify:

- production readiness or deployment authorization;
- `windows-client-death`;
- other WSL hosts, WSL versions, kernels, Linux distributions or platforms;
- unrelated host hardening; or
- any candidate with different bytes.

The clean-terminal modes exposed a native-driver `InvocationID` comparison
limitation after systemd unloaded the unit. Independent adjudication treated
the driver output as supplementary and resolved those modes from authoritative
journal, systemd, `/proc` and cgroup evidence. `supervisor-failure` retained its
invocation identity and completed with recorder exit 0.
