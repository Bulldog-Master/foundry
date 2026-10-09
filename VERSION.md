# Foundry Version

This file describes the current maturity state of Foundry. It is not software semantic versioning.

## Proposed next generation: Foundry 2

Foundry 2 is proposed in `adrs/ADR-0003-foundry-2-exception-driven-autonomous-operations.md`.

Until ADR-0003 is independently reviewed and explicitly ratified by Bulldog, **Foundry 1 remains the current authoritative generation** and no Foundry 2 automation is activated.

Foundry 2's target operating model is autonomous-by-default, human-by-exception. It preserves the Constitution, the four mandatory gates, failed-gate blocking, and ADR-0002 evaluator independence while allowing routine operational execution, gate invocation, evidence collection, deterministic routing, and remediation loops to be automated inside frozen authority envelopes.

Foundry 2 is product-neutral and intended to support multiple authorized products over time. ScoutProp is the intended first real proving ground after Foundry 2 commissioning and separate product authorization; it is not the sole product target.

### Founder-reserved acts

The proposed Foundry 2 reserved acts are defined normatively in ADR-0003. They remain unavailable to automated agents/controllers.

### Activation

Foundry 2 is not activated by this proposal or by design documents alone. Activation requires the commissioning evidence and direct founder activation described in `operations/FOUNDRY-2-COMMISSIONING-v0.1.md`.

## Current generation: Foundry 1

Foundry 1 ratifies the four-gate operating contract on top of the Foundry 0 foundation. See `adrs/ADR-0001-model-neutral-foundry-boundaries.md` for the doctrinal basis.

Foundry 1 remains the frozen reference generation while Foundry 2 is proposed and commissioned.

Its standing boundaries remain authoritative until Foundry 2 activation, including:

- manual four-gate governance;
- failed gates block by default;
- explicit founder override only;
- builder/evaluator separation under ADR-0002;
- bounded Lane A operational delegation only as authorized by the adopted v0.1 policy;
- no Foundry 1 orchestration layer;
- no adopted Foundry 1 agent framework;
- no automated Foundry 1 gate runner.

Frozen Caller-1 and Sandbox-1 production baselines remain reference infrastructure and are not silently upgraded by the Foundry 2 proposal.
