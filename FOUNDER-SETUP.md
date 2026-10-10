# One-time founder setup

This is the only interactive setup required for standing GitHub publication. It does not give the evaluator merge, branch, administration, workflow, secret, or repository-write authority.

1. Open the prefilled private GitHub App registration page:
   `https://github.com/settings/apps/new?name=foundry-evaluator&description=Independent%20Foundry%20review%20publisher&url=https%3A%2F%2Fgithub.com%2FBulldog-Master%2Ffoundry&public=false&webhook_active=false&checks=write&contents=read&pull_requests=write`
2. Create the App, install it only on `Bulldog-Master/foundry`, and generate one private key.
3. Record the App ID and installation ID. Place the downloaded private key in `/etc/foundry-evaluator/github-app.pem` as root-owned mode `0600` and create `/etc/foundry-evaluator/github-app.json` with the App ID, installation ID, repository ID `1297877588`, owner `Bulldog-Master`, and repo `foundry`.
4. Run the commissioning verification. Enable the timer only after its offline tests and a shadow publication test pass.

After this checkpoint, the service discovers PRs labeled `foundry-review`, creates one immutable packet per head, invokes Claude Opus with no tools, validates bindings and routing, and publishes the check plus review through the App. A new PR head is evaluated automatically. Valid results are never rerun. Invalid evaluator output gets at most one retry. Failed or stale review never merges.

