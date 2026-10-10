# Installation status

- External runtime: built and tested.
- Evaluator: `claude-opus-5-5`, 32,000 output tokens, high effort.
- GitHub identity: dedicated private App with `Contents: read`, `Checks: write`, and `Pull requests: write` only.
- Automatic merge: not granted.
- Activation: intentionally disabled until the founder completes `FOUNDER-SETUP.md` and commissioning verification succeeds.
- PR #26: remediation may be prepared, but every new head requires a newly sealed independent evaluation. No failed gate is overridden and this runtime status does not imply a verdict.
- Installation: `install-runtime.sh` verifies the complete release manifest, installs an immutable hash-addressed release, atomically updates `current`, preserves existing provider/GitHub credentials, and reloads (but does not enable) the systemd units.
