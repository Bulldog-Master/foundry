# foundry-sandbox-1 Production Baseline v1

## Status and boundary

This directory is the reproducibility record for the frozen
`foundry-sandbox-1` Production Baseline v1. It captures an already-proven
runtime; it does not redesign, upgrade, or extend that runtime.

The source export was verified before import:

- source archive SHA256:
  `2be0d4b1339dfc0fc8999197463e25c99e9f9424ebdca0e15a81ac202c104b8e`
- production baseline SHA256:
  `7fe58f2ac55eec39a397069955f95d6fdcac2b9e518544151d2d42b341d342c3`
- `FILES.sha256`: all 16 captured files passed
- recorded live baseline verification: 57 passes, 0 failures

`REBUILD-FACTS.txt` is the concise machine-readable rebuild contract.
`baseline/production-baseline.txt` is the evidence captured from the proven
server. The files under `bin/` and `config/` are content-identical copies of
the verified production components.

This package contains no secrets, private keys, authorized keys, tokens, job
inputs, job outputs, or live evidence bundles.

## Security boundary and known limitation

The Baseline v1 candidate boundary is the disposable KVM VPS together with
rootless Podman, user and mount namespaces, seccomp, a non-root candidate user,
no candidate network, a read-only container root filesystem, dropped
capabilities, no-new-privileges, and systemd cgroup limits.

Rootless Podman is **not currently reporting AppArmor confinement**. Do not
claim AppArmor protection for this baseline. Changing that fact is a future
baseline change and must not be folded into a Baseline v1 rebuild.

Caller-1 is deliberately separate. Its host, credentials, transport,
authorization, and orchestration are not part of this package and must not be
installed on, inferred from, or coupled to Sandbox-1 during reconstruction.

## Verify this repository copy

Run from this directory:

```sh
sha256sum -c FILES.sha256
(
  cd baseline
  sha256sum -c production-baseline.sha256
)
for script in bin/*; do bash -n "$script"; done
```

The first check must report `OK` for every entry. The baseline check must
report `production-baseline.txt: OK`. Syntax checks are necessary but do not
replace verification on the rebuilt host.

## Rebuild and setup

Rebuild only on a disposable KVM VPS with console access. Keep the existing
production Sandbox-1 untouched. Commands below are an operator procedure, not
an unattended installer; inspect each result before continuing.

1. Install Ubuntu 26.04.1 LTS and patch it to the recorded baseline. Confirm
   the expected kernel and runtime versions in
   `baseline/production-baseline.txt`: kernel `7.0.0-38-generic`, Podman
   `5.7.0`, crun `1.21`, and systemd `259 (259.5-0ubuntu3.4)`. A rebuild with
   different versions is not an exact Baseline v1 reproduction and must be
   recorded as such.
2. Install the host dependencies: OpenSSH server, UFW, Podman, crun,
   fuse-overlayfs, uidmap, sudo, Python 3, and Bash.
3. Create system group `foundry-export`. Create `foundry-exec` with UID and GID
   `1002`, home `/home/foundry-exec`, and shell `/usr/sbin/nologin`. Give it no
   supplementary groups. Set these exact subordinate-ID mappings:

   ```text
   foundry-exec:231072:65536
   ```

   in both `/etc/subuid` and `/etc/subgid`.
4. Create the runtime paths with these owners and modes:

   | Path | Owner | Mode |
   | --- | --- | --- |
   | `/srv/foundry-sandbox` | `root:root` | `0711` |
   | `/srv/foundry-sandbox/jobs` | `root:root` | `0711` |
   | `/srv/foundry-sandbox/evidence` | `root:root` | `0700` |
   | `/srv/foundry-sandbox/export` | `root:foundry-export` | `0750` |
   | `/srv/foundry-sandbox/container-storage` | `foundry-exec:foundry-exec` | `0700` |
   | `/home/foundry-exec/.config/containers` | `foundry-exec:foundry-exec` | `0700` |
5. Install the captured files without editing them:

   | Repository source | Host destination | Owner | Mode |
   | --- | --- | --- | --- |
   | `bin/*` | `/opt/foundry/bin/` | `root:root` | `0755` |
   | `config/policy.conf` | `/etc/foundry/sandbox/policy.conf` | `root:root` | `0644` |
   | `config/containers/*` | `/home/foundry-exec/.config/containers/` | `foundry-exec:foundry-exec` | `0644` |
   | `config/ssh/90-foundry-hardening.conf` | `/etc/ssh/sshd_config.d/90-foundry-hardening.conf` | `root:root` | `0644` |
   | `config/ssh/ssh-socket-override.conf` | `/etc/systemd/system/ssh.socket.d/override.conf` | `root:root` | `0644` |
6. While controlled outbound access is still available, pull exactly the
   digest-pinned image named in `config/policy.conf` into `foundry-exec`'s
   rootless Podman storage. Confirm the local image digest before closing
   outbound access.
7. Validate the SSH configuration before reloading it. Keep console access
   open while moving SSH to TCP port `2222`; confirm key-only login on a second
   session before closing the original session.
8. Configure UFW as recorded: deny incoming, deny outgoing, and allow incoming
   TCP `2222` for IPv4 and IPv6. Do not add unrecorded listeners or egress
   exceptions.
9. Run `/opt/foundry/bin/foundry-sandbox-verify` as root. An exact rebuild must
   finish with `PASS=57`, `FAIL=0`, and
   `FOUNDRY_SANDBOX_BASELINE=PASS`. Save its output as rebuild evidence.
10. Compare the rebuilt host's fixed facts and installed component hashes with
    `REBUILD-FACTS.txt` and `baseline/production-baseline.txt`. The archived
    baseline SHA256 authenticates the captured evidence file; a newly captured
    report contains a new timestamp and is not expected to have that same
    digest. Investigate every substantive difference and do not relabel a
    divergent host as Production Baseline v1.

## Job evidence export

The root operator creates a job, stages an input directory, runs the bounded
candidate command, and exports only a completed job:

```sh
JOB_ID="$(sudo /opt/foundry/bin/foundry-job-create)"
sudo /opt/foundry/bin/foundry-stage-input "$JOB_ID" /path/to/input
sudo /opt/foundry/bin/foundry-run-job "$JOB_ID" command arg1 arg2
sudo /opt/foundry/bin/foundry-export-job "$JOB_ID"
```

The export command re-verifies the sealed evidence packet and output tree
before producing `/srv/foundry-sandbox/export/$JOB_ID.tar` and its companion
`.sha256`. Export files are `root:foundry-export` mode `0440`; `foundry-exec`
must not be a member of `foundry-export` and must not be able to read that
directory.

Transfer the tar and checksum through the separately authorized export path.
Do not give the candidate execution account export access.

## Independent verification

The verifier works from copies outside Sandbox-1 and does not trust the
producer's statement that verification passed.

1. Compare the downloaded tar's SHA256 with the digest in its companion file.
   The companion may contain the original absolute server path, so compare the
   first field rather than relying on the recorded filename.
2. List the archive and reject absolute paths, `..` traversal, device nodes,
   or unexpected top-level entries before extraction.
3. Extract into a new empty temporary directory.
4. From the job bundle root, run `sha256sum -c export-files.sha256`.
5. From `evidence/`, run `sha256sum -c packet.sha256`.
6. Confirm that job state is `COMPLETE`; the job IDs agree; the input and
   output hashes agree across `job/input.sha256`, `evidence/manifest.txt`, and
   `export-manifest.txt`; and the recorded command, exit code, image digest,
   policy hash, runner hash, timestamps, and resource boundary are present.
7. Independently hash the extracted `output/` with the captured
   `bin/foundry-tree-hash` and compare it with `OUTPUT_SHA256` in both
   manifests.
8. Record who verified the bundle, when, the bundle SHA256, the result of each
   check, and any limitation. Verification failure makes the evidence
   unusable until explained; it is not waived by producer attestation.

## Readiness checklist

A rebuilt Sandbox-1 is not ready until every item is true:

- [ ] The rebuild uses a disposable KVM VPS and leaves production untouched.
- [ ] OS, kernel, runtime versions, identity values, and subordinate IDs match.
- [ ] Every repository component passes `FILES.sha256` before installation.
- [ ] Installed component hashes match the recorded component hashes.
- [ ] The image is present locally at the exact immutable digest.
- [ ] `foundry-exec` is non-login, rootless, and has no supplementary groups.
- [ ] Candidate networking is `none`; rootfs is read-only; capabilities are
