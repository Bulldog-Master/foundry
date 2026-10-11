# Root installation and final PR #26 sealing

Run the supplied commit-and-manifest-pinned PowerShell command on the Windows host containing WSL distro `Foundry-Agent`. It downloads public source without Git credentials into a new root-private staging directory, verifies the independently supplied manifest digest, installs, and seals. Keep the returned `packet_sha256`, `packet_dir`, `base_sha`, and `head_sha` for the next independent invocation. No provider or App key is needed to seal.

The existing provider key remains `/etc/foundry-evaluator/api-key`; the existing App key and config remain `/etc/foundry-evaluator/github-app.pem` and `/etc/foundry-evaluator/github-app.json`. This release does not create or replace them. The publisher permits only App ID `5263160`, installation `169955633`, repository `1297877588`, and verifies observed GitHub identity and bounded permissions before acquiring an installation token. It never falls back to a PAT, founder user token, gh credential, environment credential, or SSH identity. Missing or mismatched credentials refuse publication.

Later root invocation and publication remain separate from seal-only installation. Every current-head valid result is retained and never redrawn. Terminal invalidity produces `action_required`; a valid adverse result produces a failing check (or `action_required` for founder escalation) and `REQUEST_CHANGES`. Uncertain publication stops rather than posting duplicate judgments.

The timer remains disabled. Branch protection acceptance, exact App source binding, custodian independence, live shadow publication, and any Foundry 2 activation require separate commissioning evidence and applicable founder acts. Offline tests do not attest to those live conditions.
