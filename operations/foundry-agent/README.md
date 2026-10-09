# Foundry Agent Operational Record

## Status

Operationally commissioned on 2026-10-09 for bounded Foundry implementation
work.

This record documents the contained `Foundry-Agent` WSL environment and its
approved remote management paths. It does not adopt an agent framework into
Foundry doctrine, automate Foundry gates, or expand signing, merge, promotion,
governance, scoring, adjudication, or sealed-truth authority.

## Local containment

The agent runs in the dedicated WSL distro `Foundry-Agent` as local user
`foundry-agent` (UID/GID 1000).

Verified containment properties:

- Windows drive automount is disabled;
- Windows interop is disabled;
- Windows paths are not inherited into the Linux PATH;
- the agent user has no local sudo authority;
- the normal working directory is `/home/foundry-agent/work`;
- the operating contract is loaded from
  `/home/foundry-agent/work/AGENTS.md`.

Local PAUSE/KILL controls are retained on the Windows control plane. The
contained WSL environment is not a Caller signing trust root.

## Codex runtime

The contained agent uses OpenAI Codex CLI:

```text
codex-cli 0.162.0
```

Codex is installed under the unprivileged agent user's home directory and is
authenticated with the operator's ChatGPT account.

The Codex workspace is `/home/foundry-agent/work` with granular workspace
permissions. Network actions are currently configured to ask for approval
rather than run with unrestricted network authority.

## Approved remote paths

The commissioning preflight verified dedicated SSH identities and accounts for:

- `caller-1` -> `foundry-agent`, UID/GID 1002;
- `sandbox-1` -> `foundry-agent`, UID 1003 / GID 1004;
- `standalone` -> `foundry-agent`, UID/GID 1001.

The commissioning preflight also verified that Windows drives were not mounted
and that the local working directory and identity were correct.

### Caller-1

Passwordless sudo authority is limited to:

```text
(root) NOPASSWD: /usr/local/sbin/foundry-agent-caller-dispatch
```

The Caller production contract and production baseline remain frozen and
separate from this management-plane access.

### Sandbox-1

Passwordless sudo authority is limited to:

```text
(root) NOPASSWD: /usr/local/sbin/foundry-agent-sandbox-dispatch
```

Sandbox-1 Production Baseline v1 remains frozen. The agent integration is the
separately documented management-plane overlay.

### Standalone

Standalone remains a lab/evaluator/development machine, not a signing trust
root. The agent is limited to approved Hermes working areas.
`/opt/xxnetwork` and unrelated host services remain outside agent authority.

## Commissioning result

The read-only commissioning preflight completed with overall `PASS`.

Verified results:

- local identity: PASS;
- working directory: PASS;
- no Windows drive mounts: PASS;
- Caller-1 SSH identity: PASS;
- Sandbox-1 SSH identity: PASS;
- Standalone SSH identity: PASS;
- Caller-1 sudo boundary: PASS;
- Sandbox-1 sudo boundary: PASS.

No changes were made by the commissioning preflight.

## Known limitation and future hardening

A distro-level structural outbound egress allowlist has not yet been
commissioned.

Current outbound control relies on the combination of:

- disabled Windows interop and drive mounts;
- no local sudo for the agent account;
- Codex network actions requiring operator approval;
- dedicated remote SSH identities;
- remote account separation and narrow privileged dispatchers;
- the `AGENTS.md` operating boundary.

This is sufficient for bounded operational use, but it is not a claim that
arbitrary outbound destinations are technically unreachable from the WSL
network namespace.

Structural egress allowlisting remains a future hardening item and must be
designed so that required OpenAI authentication/service access, GitHub access,
DNS, and approved dynamic endpoints remain functional.

## Human approval boundaries

Human approval remains mandatory for signing, secrets/provider credentials,
trust-boundary changes, destructive actions with meaningful blast radius,
frozen production-contract or baseline changes, final merge/protected-branch
actions, production promotion, new provider authorization, governance/doctrine
changes, and founder overrides.
