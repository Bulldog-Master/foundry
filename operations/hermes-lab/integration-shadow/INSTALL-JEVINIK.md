# Jev/Jevinik installation candidate — Standalone only

**Distinct components:** Jev is the TypeSafe AI typed evaluation model available as `typesafe-ai/jev` through Vercel AI Gateway and AI SDK `experimental_evaluate`. Jevinik is the Next.js stock-analysis demo [unicodeveloper/jevocks](https://github.com/unicodeveloper/jevocks), using Valyu for financial evidence. **Valyu is not necessary for generic Foundry task routing.**

## Install / stage Jevinik
Upstream README specifies Node.js >=20.9, npm, a Valyu API key and a Vercel AI Gateway API key to *run* the demo. The candidate stages source/dependencies **without credentials, model calls, service activation or altered Hermes runtime**. Installation on Standalone has not yet occurred.

Under existing contained Standalone `foundry-agent` (never root), select and review an **exact upstream 40-character source commit SHA**, including its lockfile, then from the approved lab run:
```bash
JEVINIK_COMMIT=<reviewed-40-character-SHA> bash install_jevinik_lab.sh
```
The script stages only under `/srv/hermes-lab/foundry-agent/jevinik-candidate`, with `npm ci --ignore-scripts`. It refuses root, other users, unpinned source, stale target and unsupported Node versions. It stops before running the demo. Retain source SHA, lockfile hash, identity, exit and externally held evidence. Candidate dependencies remain untrusted until independently reviewed.

## Jev model evaluation
After explicit provider/key/cost authorization, evaluate synthetic Foundry triage packets in a **disposable** runtime with a minimum-data evidence state and typed questions using Vercel's published `experimental_evaluate({model:'typesafe-ai/jev',state,questions})`. Store provider credentials in the existing approved secret authority, never in GitHub, Hermes memory or `.env.local` checked into source. Pin AI SDK/runtime versions at the evaluation stage. Compare against independently established labels; capture provider response, token usage, time, errors, evidence freshness, and abstentions. Jev's signal does not authorize launches, merges, signing, evaluator selection or production promotion.

## Admission and activation checkpoint
Preserve existing Hermes→ChatGPT/Codex and Ollama configuration. Exact Hermes installed state, Jev API support, Valyu usefulness, and Jevinik dependency safety must be verified on Standalone. No new network permission, credential, service, production activation or frozen gate change is implied by this repository candidate. Issue #36 / PR #37. 
