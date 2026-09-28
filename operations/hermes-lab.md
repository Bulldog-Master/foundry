# Standalone Hermes lab

## Status and boundary

This document records the operating configuration and evaluator-isolation requirements of the dedicated Standalone Hermes lab. It is an operational record, not an architectural adoption of Hermes into Foundry. Foundry remains the authoritative governance and evidence system; Hermes is external experimental tooling.

As an Operational record, this document is subordinate to the Constitution and ADRs, carries no standing gate authority, and must be revalidated or superseded when operating reality changes.

The lab does not introduce CI gate enforcement, an automated gate runner, an orchestration layer, or an adopted Foundry agent framework. Manual gate records and human founder authority remain intact.

Detailed machine baselines and version or provider specifics belong in the private execution and evidence record rather than this public governance record. Any machine-state or tooling fact on which a blinded experiment relies must be reverified before that experiment.

## Host

- Operating system: Ubuntu 24.04.
- Deployment: standalone machine.
- Unrelated production or network services on this host are outside Hermes-lab authority and must not be modified. This is an operational prohibition, not a claim of OS- or container-enforced isolation unless separate evidence establishes that enforcement.

## Storage

The lab root is `/srv/hermes-lab`. Blinded evaluator environments and authorized evidence are kept separate from normal Hermes state and general lab workspaces beneath that root. Detailed storage and directory topology belongs in the private execution and evidence record.

## Hermes configuration

Hermes is external experimental tooling. Its normal shared state, including its normal `HERMES_HOME`, must not bleed into blinded evaluator environments. Exact Hermes versions, provider and model selections, service state, and other execution-specific configuration belong in the private execution and evidence record and must be reverified before experiments.

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
