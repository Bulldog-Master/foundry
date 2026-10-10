# Foundry Evaluator External Runtime Policy

This runtime is a commissioning trust anchor outside every subject pull request. It is not activated Foundry 2 and has no merge, branch-write, workflow-write, administration, deployment, signing, promotion, override, ratification, or founder-approval authority.

## Fixed separation

- The packet builder reads immutable Git objects by SHA and writes a root-sealed packet.
- The evaluator receives only the sealed packet and fixed task; it receives no GitHub credential, repository access, tools, or network capability beyond the provider request made by the invoker.
- The publisher receives no Anthropic credential. It validates the sealed packet, result, invocation record, deterministic routing, and current PR head before acquiring a short-lived GitHub App installation token.
- The GitHub App is installed only on `Bulldog-Master/foundry` with `Contents: read`, `Checks: write`, and `Pull requests: write`.
- The App has no permission capable of pushing commits, changing branches or protection, merging, modifying workflows, reading secrets, or performing founder acts.

## Publication rules

- A stale result is never published as passing or approving.
- A valid `PASS` publishes a successful `foundry/four-gate` check and an `APPROVE` review.
- `FAIL` publishes a failed check and `REQUEST_CHANGES` review.
- `PASS_WITH_CONDITIONS` and any human-required route publish `action_required` and `REQUEST_CHANGES`.
- Invalid bindings, hashes, schema, routing, current-head checks, or credential configuration fail closed before publication.
- Publication is idempotent by `(repository, PR, head SHA, packet SHA, review-record SHA)`.

## Custody and retention

- `/opt/foundry-evaluator/releases/<release-hash>` is root-owned and read-only.
- `/etc/foundry-evaluator` is root-only and contains provider and GitHub App credentials in separate files.
- `/var/lib/foundry-evaluator/packets` and `/var/lib/foundry-evaluator/runs` are root-only and append-preserving during commissioning.
- Provider request IDs and GitHub response IDs are retained for commissioning evidence; credentials are never written to evidence.
- Removal/retention policy is a founder activation decision. Until then, commissioning evidence is retained.
