# Foundry-Agent P0 execution connection — preflight candidate

**Issue:** #31. **Status:** candidate only; no activation of a standing autonomous runner or Lane A.

This initial preflight establishes whether a commissioned **unprivileged** Foundry-Agent can see its operating contract and Codex binary without involving privileged root execution. It never invokes a model, provider, SSH action, or production dispatcher.

The authoritative operational record is `operations/foundry-agent/README.md`. Only existing Foundry-Agent environment `/home/foundry-agent/work` and `AGENTS.md` are valid. Windows drive automount/interop remain disabled. No permission widening. No change to Foundry 1 manual gate boundaries, ADR-0002, frozen Caller-1/Sandbox-1/evaluator, protected merges or PAUSE/KILL.

## Offline tests
Run from `operations/foundry-agent/execution-transport` (repository-root discovery finds no tests):
`python3 -m unittest discover -p 'test_*.py' -v`

## Reconciled operational facts

The readiness-task input confirms that Foundry-Agent runs unprivileged as UID
1000, Codex CLI 0.162.0 is available, Windows PAUSE/KILL is implemented and
verified, one bounded Codex task completed successfully, and the Windows-side
launcher candidate exists and is hash-pinned. No standing autonomous authority
is commissioned. Windows verification, task evidence, and the launcher hash are
external to this candidate; this preflight does not independently verify them.

## Remaining independent P0 evidence requirements
- Attach the existing Windows PAUSE/KILL verification evidence and record the actual Codex approval mode.
- Obtain a pre-authorized single-job envelope with explicit command/task scope, time/resource budget, allowed paths and expected evidence.
- Ensure job launcher identity cannot modify reviewer input or sole authoritative evidence and cannot assume founder/Lane B authority.
- Attach the successful bounded-task evidence and prove the applicable negative controls in a disposable workspace.
- Record execution and external evidence custody with exact hashes.
- Commission the transport only through the applicable frozen authorization process.

No agent runtime or automatic execution is claimed by this PR.
