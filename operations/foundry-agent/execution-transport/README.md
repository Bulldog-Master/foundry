# Foundry-Agent P0 execution connection — preflight candidate

**Issue:** #31. **Status:** candidate only; no activation of a standing autonomous runner or Lane A.

This initial preflight establishes whether a commissioned **unprivileged** Foundry-Agent can see its operating contract and Codex binary without involving privileged root execution. It never invokes a model, provider, SSH action, or production dispatcher.

The authoritative operational record is `operations/foundry-agent/README.md`. Only existing Foundry-Agent environment `/home/foundry-agent/work` and `AGENTS.md` are valid. Windows drive automount/interop remain disabled. No permission widening. No change to Foundry 1 manual gate boundaries, ADR-0002, frozen Caller-1/Sandbox-1/evaluator, protected merges or PAUSE/KILL.

## Offline tests
Run from `operations/foundry-agent/execution-transport` (repository-root discovery finds no tests):
`python3 -m unittest discover -p 'test_*.py' -v`

## Reported operational facts (unverified here)

The readiness-task input reports that Foundry-Agent runs unprivileged as UID
1000, that Codex CLI 0.162.0 is available, that Windows PAUSE/KILL was
implemented and verified, that one bounded Codex task completed, and that a
Windows-side launcher candidate exists and is hash-pinned. None of this is
contained in this PR, and this preflight verifies none of it. No standing
autonomous authority is commissioned.

## What the output does and does not establish

The preflight checks only that the effective UID is 1000, the workspace is a
directory owned by UID 1000, `AGENTS.md` resolves to a regular file owned by UID
0 or 1000, and some executable named `codex` is found on the process `PATH`.

It does not establish the identity, integrity or version of the contract or
binary. It does not check symlinks, modes, path ancestors, groups,
capabilities, `NoNewPrivs`, sudo authority or the protected paths named in the
source. The `production_targets`, `provider_call` and `task_execution` output
values are hard-coded declarations, not observations. The
`read_only_preflight: PASS` value means only that the limited checks above
completed successfully.

Any output record is written by the actor into its own workspace. It therefore
cannot be the sole authoritative evidence of actor identity, containment or
restraint.

## Remaining independent P0 evidence requirements
- Attach the existing Windows PAUSE/KILL verification evidence and record the actual Codex approval mode.
- Obtain a pre-authorized single-job envelope with explicit command/task scope, time/resource budget, allowed paths and expected evidence.
- Ensure job launcher identity cannot modify reviewer input or sole authoritative evidence and cannot assume founder/Lane B authority.
- Attach the successful bounded-task evidence and prove the applicable negative controls in a disposable workspace.
- Record execution and external evidence custody with exact hashes.
- Commission the transport only through the applicable frozen authorization process.

No agent runtime or automatic execution is claimed by this PR.
