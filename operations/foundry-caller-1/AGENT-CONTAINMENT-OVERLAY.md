# Caller-1 Agent Containment Overlay

## Status

Installed and verified on 2026-10-09.

This record documents a post-commission management-plane overlay on production
`foundry-caller-1`. It does not amend or redefine the frozen Caller Production
Contract v1 or Production Baseline v1.

## Added identity and paths

The overlay added the dedicated identity:

- account: `foundry-agent`, UID `1002`
- primary group: `foundry-agent`, GID `1002`
- supplementary groups: none

Verified active overlay paths/files:

- `/home/foundry-agent`
- `/home/foundry-agent/.ssh`
- `/home/foundry-agent/.ssh/authorized_keys`
- `/home/foundry-agent/agent-inbox`
- `/usr/local/sbin/foundry-agent-caller-dispatch`
- `/etc/sudoers.d/foundry-agent-caller`

The dispatcher also uses the bounded temporary staging directory
`/run/foundry-agent-caller` when handing a manifest to the existing
commissioned acceptance path.

No Agent-related systemd units were added.

## Authority

The dedicated sudo authorization is limited to:

```text
(root) NOPASSWD: /usr/local/sbin/foundry-agent-caller-dispatch
```

The dispatcher accepts only a manifest from the agent inbox, rejects absolute
paths and parent traversal, copies the manifest through bounded temporary
staging, and invokes the existing commissioned entry point:

```text
/opt/foundry-caller/app/accept-and-stage-seal-authorization
```

An invalid-manifest test reached the commissioned manifest validator and was
rejected. Temporary staging cleanup was subsequently verified.

The overlay does not grant `foundry-agent` signing authority, provider
credentials, unrestricted/general root access, sealing authority, sealed-truth
access, scoring/fusion/adjudication authority, or authority to modify the
commissioned Caller runtime.

## Recorded hashes

Hashes captured during the 2026-10-09 verification:

```text
cdc01c3a62096df6166d84e3faed94035d93e7cba7c0d1c91018a211e94cc9ba  /home/foundry-agent/.ssh/authorized_keys
ace9f0df2c7c4834d6a94ca72d097bfd7d6a0edecf956b78a8a68a64524b0f59  /usr/local/sbin/foundry-agent-caller-dispatch
6f898dd0375a2976a1207db15868083b82e4b3e2edbdada3b4b64dfce05482ea  /etc/sudoers.d/foundry-agent-caller
```

## Verification and classification

After installation of the overlay, the existing commissioned verifier suite was
rerun and matched the frozen production record exactly:

```text
baseline:          24 passed, 0 failed
network:            6 passed, 0 failed
egress:             9 passed, 0 failed
confinement:       27 passed, 0 failed
runtime exclusion: 16 passed, 0 failed
```

The retired `foundry-caller.service` remains disabled, and the root-owned
authorization and sealing paths remain active.

Caller-1's commissioned production boundary therefore remains valid in its
verifier-covered scope. No verifier-covered Caller runtime, network, egress,
confinement, or runtime-exclusion invariant was changed by this overlay.

The production host as a whole does contain post-commission management-plane
additions and must not be described as byte-for-byte unchanged since
commissioning.

These additions are classified as a management-plane overlay, not a new Caller
production-contract version. The frozen `PRODUCTION-CONTRACT-v1.md` and
`PRODUCTION-BASELINE.txt` remain unchanged.
