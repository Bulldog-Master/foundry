# Sandbox-1 Agent Containment Overlay

## Status

Installed and verified on 2026-10-09.

This record documents a post-freeze management-plane overlay on production
`foundry-sandbox-1`. It does not amend or redefine Production Baseline v1.

## Added identity and paths

The overlay added the dedicated account and group:

- account: `foundry-agent`, UID `1003`
- primary group: `foundry-agent`, GID `1004`
- supplementary groups: none

The following paths/files were added for Agent Containment:

- `/home/foundry-agent`
- `/home/foundry-agent/.ssh`
- `/home/foundry-agent/.ssh/authorized_keys`
- `/srv/foundry-sandbox/agent-inbox`
- `/usr/local/sbin/foundry-agent-sandbox-dispatch`
- `/etc/sudoers.d/foundry-agent-sandbox`

No Agent-related systemd units were added.

## Authority

The dedicated sudo authorization is limited to:

```text
(root) NOPASSWD: /usr/local/sbin/foundry-agent-sandbox-dispatch
```

The dispatcher path is:

`/usr/local/sbin/foundry-agent-sandbox-dispatch`

The overlay does not grant `foundry-agent` signing authority, provider
credentials, unrestricted/general root access, sealed-truth access, or
authority to modify the candidate runtime boundary.

## Recorded hashes

Hashes captured during the 2026-10-09 verification:

```text
8682974e305890e99dd193781c85dca083b1ffa14fa6569dc48f9ad38dd93547  /home/foundry-agent/.ssh/authorized_keys
7f7e56a1676ca4d81026ea9c6fa8dad0ad04ccbcf847eaeb264e457dde40d34e  /usr/local/sbin/foundry-agent-sandbox-dispatch
5aa1a3cbd21efc6d1c5cebd61c62e33b4a009f73a5be338ea45d59295eac30ce  /etc/sudoers.d/foundry-agent-sandbox
```

Baseline-sensitive configuration hashes observed during the same verification:

```text
aac0236ae904b06ff2a68b39c6b8ebb360c1c6d00edaa04047cc68cad5ab463b  /etc/foundry/sandbox/policy.conf
1e273fe90a29a2867eacc31a5b6416d0f855faf5e44280ce01882693d79a0e71  /home/foundry-exec/.config/containers/containers.conf
408829a447bc8fa8f67242a7db3392fb1bc7a1116c1ee3149728885a9e4a4536  /home/foundry-exec/.config/containers/storage.conf
d8d3418701369e726c414b06c300a72dc673de3ae2b908cac8c73f9116a11340  /etc/ssh/sshd_config.d/90-foundry-hardening.conf
a961b5126c30434d5c002e4af415f09797056a620395ab6918c79f1dcd365662  /etc/systemd/system/ssh.socket.d/override.conf
```

## Verification and classification

The existing production verifier was rerun after installation of the overlay
and reported:

```text
PASS=57
FAIL=0
FOUNDRY_SANDBOX_BASELINE=PASS
```

Production Baseline v1 candidate execution therefore remains valid and
unchanged in its verifier-covered boundary. No verifier-covered candidate
runtime invariant was changed by this overlay.

The production host as a whole does contain post-freeze management-plane
additions and must not be described as byte-for-byte unchanged since the
Baseline v1 freeze.

Foundry Lead classified and accepted these additions as a management-plane
overlay rather than a Production Baseline v2 candidate-execution change. The
frozen Production Baseline v1 artifact remains unchanged.
