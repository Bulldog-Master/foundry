# Standalone Hermes lab

## Status and boundary

This document records the operating configuration and evaluator-isolation requirements of the dedicated Standalone Hermes lab. It is an operational record, not an architectural adoption of Hermes into Foundry. Foundry remains the authoritative governance and evidence system; Hermes is external experimental tooling.

The lab does not introduce CI gate enforcement, an automated gate runner, an orchestration layer, or an adopted Foundry agent framework. Manual gate records and human founder authority remain intact.

## Host

- Operating system: Ubuntu 24.04.
- Deployment: standalone machine.
- Hermes and xx Network coexist on this host.
- Hermes-lab operations must not modify xx Network core services.
- xxOps repair work is outside the scope of this document.

## Storage

The lab uses the second Corsair MP600 PRO NVMe, approximately 1.8 TB Linux-visible, with filesystem label `hermes-lab` mounted at `/srv/hermes-lab`.

| Directory | Purpose |
| --- | --- |
| `/srv/hermes-lab/disposable-envs` | Separate disposable evaluation environments. |
| `/srv/hermes-lab/docker` | Docker data root. |
| `/srv/hermes-lab/evidence` | Authorized evaluator-isolation and run evidence. |
| `/srv/hermes-lab/models` | Model-related operational artifacts. |
| `/srv/hermes-lab/repositories` | Repository material authorized for lab operations. |
| `/srv/hermes-lab/workspaces` | General lab workspaces that are not blinded evaluator environments. |
| `/srv/hermes-lab/hermes-home` | Normal Hermes home. |
| `/srv/hermes-lab/hermes-agent` | Hermes agent installation and working material. |

Docker uses `/srv/hermes-lab/docker` as its data root.

## Hermes configuration

- Version: `v0.21.5+3779.g8f897d2 (2026.9.24)`.
- Upstream commit: `8f897d2d`.
- Normal home: `HERMES_HOME=/srv/hermes-lab/hermes-home`.
- Gateway user service: intentionally disabled and inactive.
- Provider path: OpenAI/ChatGPT-Codex.
- Model: `gpt-5.6-sol`.
- Reasoning: `medium`.
- Anthropic subscription-token/API path: not configured for Hermes.

This record intentionally contains no secrets, credential contents, API keys, OAuth contents, token IDs, or authentication strings.

## Evaluator-lab requirements

Evaluator independence is governed by ADR-0002. The lab must preserve these operational boundaries:

- Blinded evaluator workspaces are constructed and bounded for the execution; they are not ordinary repository clones.
- They do not inherit normal Git history unless that history is explicitly authorized and justified as necessary evaluation context.
- They do not inherit persistent memory.
- They do not share the normal `HERMES_HOME`.
- Canary and real-evaluator work run in separate disposable environments.
- Sealed adjudication material is never stored in evaluator workspaces.
- The governed actor must not control frozen authoritative evidence used to establish its own compliance.
- Prior exposure to information deliberately withheld from evaluators disqualifies blinded evaluation for that execution and cannot be cured by resetting the environment.
- Evaluators receive the minimum bounded context reasonably necessary. Broader context is permitted only when genuinely required and justified in the independence record.

Evaluator evidence must record enough effective configuration and relevant state to make the claimed isolation boundary checkable. It must also state its limitations: the evidence may test defined retrieval and contamination paths, but it cannot prove the absence of undocumented provider-internal behavior.

## Change control

Changes to this operational record do not, by themselves, adopt Hermes as part of Foundry architecture or change the Foundry generation. Any proposal to change Foundry's standing gate authority, introduce automation, or adopt an agent framework requires its own evidence and authorization under the Constitution and applicable ADRs.
