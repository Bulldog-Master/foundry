# Sandbox-1 Security Scan Follow-up

## No-drift verification

On 2026-10-07, the production `foundry-sandbox-1` host was checked against
the frozen Production Baseline v1:

- live verifier result: `PASS=57`, `FAIL=0`,
  `FOUNDRY_SANDBOX_BASELINE=PASS`;
- Production Baseline v1 SHA-256:
  `7fe58f2ac55eec39a397069955f95d6fdcac2b9e518544151d2d42b341d342c3`;
- hostname: `foundry-sandbox-1`;
- kernel: `7.0.0-38-generic`.

These results show no detected drift. Production Baseline v1 remains valid
and frozen. This follow-up records security-review conclusions only; it does
not amend the baseline, its checksum, the verifier, or runtime configuration.

## Security Scan classification

### Already implemented and proven

- The hardened container boundary uses rootless Podman, a non-root UID, a
  read-only root filesystem, no candidate network, zero capabilities,
  `no-new-privileges`, seccomp, namespaces, and cgroup resource limits.
- The runtime image is pinned by immutable digest and its exact provenance is
  recorded and verified by policy and baseline evidence.
- The AppArmor posture is explicit and accepted for v1: rootless Podman is not
  reporting AppArmor confinement, no AppArmor protection is claimed, and any
  change belongs to a future baseline.
- The disposable outer VPS boundary and the current deny-out/listener posture
  are documented and proven for Production Baseline v1.

### Implemented, but an evidence gap remains

- IPv4 and IPv6 firewall controls are present, but explicit attribution
  evidence for candidate-originated network attempts has not yet been
  retained to the newer Security Scan standard.
- Firewall cleanup and the resulting deny-out/listener behavior are proven,
  but a formal before-and-after rule diff for temporary rules was not retained
  as a standalone artifact.

These are evidence-quality follow-ups, not evidence of a defect in the
current production boundary.

### Missing experimental coverage

- There is no dedicated, reusable, tool-neutral escape/denial corpus.
- Hostile escape and resource-abuse experiments have not been run as a
  formal comparative test campaign against alternative isolation runtimes.

### Deferred to Baseline v2

- A gVisor comparison is deferred to a Baseline v2 candidate.
- Tetragon, or an equivalent host-runtime tripwire, is deferred to a Baseline
  v2 candidate.
- Any change intended to add or claim AppArmor confinement requires a future
  baseline rather than a modification to Production Baseline v1.
- The stronger network-attribution evidence and formal firewall rule-diff
  artifact should be evaluated as part of Baseline v2 evidence design.

gVisor, Tetragon, the escape corpus, and all hostile escape or resource-abuse
testing belong only on a disposable clone used as a Baseline v2 candidate.
Unconfined hostile escape or resource-abuse testing on production
`foundry-sandbox-1` is prohibited.

These deferred items do not block Caller↔Sandbox integration unless testing
or review discovers a genuine trust-boundary defect.
