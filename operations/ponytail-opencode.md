# Ponytail and OpenCode advisory tooling

## Status and scope

As of 2026-10-20, producer setup is complete for manually launched OpenCode
advisory work using public or synthetic inputs. The instruction-only
Ponytail-Foundry adaptation is also installed in ChatGPT. Neither installation
is autonomous Foundry commissioning, architectural adoption, or gate approval.

This Operational record is subordinate to the [Constitution](../CONSTITUTION.md),
[ADR-0001](../adrs/ADR-0001-model-neutral-foundry-boundaries.md), and
[ADR-0002](../adrs/ADR-0002-evaluator-independence-and-isolation.md). The
[Hermes lab record](hermes-lab.md) governs the public/private evidence boundary.

## Role and limits

Ponytail-Foundry guides the smallest complete, tested change: reuse appropriate
existing helpers, avoid unnecessary abstractions, and preserve security checks
and Foundry governance. Instructions are not an authorization mechanism.

The OpenCode lab profile permits only the existing local inference provider;
shell and file tools are denied by configuration. Its scope excludes autonomous
execution, Hermes dispatch, schedules, standing services, remote providers,
deployment, publishing, and merging. The portable skill package adds no hooks,
tool servers, credentials, or operational permissions.

A separate application profile and inspected deny policies are not an
OS-enforced sandbox or proof against every bypass. Protected Foundry material,
normal agent sessions, and secrets remain outside this advisory scope.

## Producer verification and retained limitation

Producer checks established local inference and exact Ponytail ruleset inclusion
in an OpenCode provider request. The latter used a synthetic response endpoint;
it does not itself prove model inference. Structural adapter tests are not live
integration or independent gate evidence.

A subsequent synthetic code-review response produced correct boundary behavior
but duplicated logic instead of reusing the supplied helper. This instruction-
following failure is retained, not replaced by a passing retry. Outputs require
human review; setup completion is not a claim that every behavioral check passed.

Follow-up native discovery checks confirmed all six Ponytail skills and six
commands were registered, and all six skill bodies matched the pinned source.
The initial empty lists were read before asynchronous plugin activation had
completed. Waiting for activation resolved the discovery gap without changing
the installation. Registration does not imply permission to load a skill;
model-side loading remains denied by the existing profile.

Analysis of the saved failing response confirmed that the helper was supplied
and explicitly requested, and the response was not truncated. One targeted
follow-up used the unchanged local launcher and model with an explicit
helper-call constraint. It returned direct helper delegation and passed six
boundary checks using structural analysis and bounded expression evaluation;
model-generated code was not executed.

That single success is a prompt-level mitigation example, not a general
reliability fix or a controlled causal experiment. The original failure remains
on record and human review is still required. No persistent prompt, profile,
permission, or adapter change was made.

Independent review remains with the separate review workflow. This producer
record assigns no independent gate outcome or standing evaluator authority.

## Evidence custody and change control

Exact versions, model selections, configuration, launchers, provenance, checksums,
execution records, and rollback details remain in private execution custody.
Do not publish environment files, encryption keys, OAuth tokens, credential
exports, database volumes or backups, SSH keys, session data, or protected material.

This documentation update changes no running integration, service configuration,
permission, frozen decision, or approval gate. Expanding these tools' scope needs
separate authorization and applicable evidence. Reverting this note would revert
documentation only; it would not roll back the private lab installation.
