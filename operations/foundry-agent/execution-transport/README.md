# Foundry-Agent P0 execution connection — preflight candidate

**Issue:** #31. **Status:** candidate only; no activation of a standing autonomous runner or Lane A.

This initial preflight establishes whether a commissioned **unprivileged** Foundry-Agent can see its operating contract and Codex binary without involving privileged root execution. It never invokes a model, provider, SSH action, or production dispatcher.

The authoritative operational record is `operations/foundry-agent/README.md`. Only existing Foundry-Agent environment `/home/foundry-agent/work` and `AGENTS.md` are valid. Windows drive automount/interop remain disabled. No permission widening. No change to Foundry 1 manual gate boundaries, ADR-0002, frozen Caller-1/Sandbox-1/evaluator, protected merges or PAUSE/KILL.

## Offline tests
`python3 -m unittest discover -p 'test_*.py' -v`

## Independent P0 readiness requirements — not completed
- Confirm the active Windows PAUSE/KILL implementation and Codex approval mode from the actual host rather than infer them from GitHub docs.
- Obtain a pre-authorized single-job envelope with explicit command/task scope, time/resource budget, allowed paths and expected evidence.
- Ensure job launcher identity cannot modify reviewer input or sole authoritative evidence and cannot assume founder/Lane B authority.
- Prove negative controls and a harmless agent-run task in a disposable workspace.
- Record execution and external evidence custody with exact hashes.
- Commission the transport only through the applicable frozen authorization process.

No agent runtime or automatic execution is claimed by this PR.
