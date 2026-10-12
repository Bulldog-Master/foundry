# Foundry HQ Telegram — notification and bounded-approval candidate

**Status:** Development candidate, **not installed, activated, or authorized for credentials**.

This development candidate includes outbound status notifications plus an offline bounded-approval contract for ordinary Foundry-Agent tasks. It does **not** activate live Telegram polling/webhooks, controller scheduling, evaluator routing, protected actions, or standing authority.

## Why this is intentionally limited

Foundry-Agent is commissioned for bounded implementation, while current Foundry 1 VERSION.md expressly excludes an adopted orchestration layer and automated gates. ADR-0003 (Foundry 2) is still **PROPOSED**. Neither the notification code nor the bounded approval-contract candidate amends either authority boundary or activates the proposed controller.

## Behavior and trust boundary

- No third-party Python dependencies. Runs in offline dry-run mode without secrets.
- Only accepts `https://github.com/Bulldog-Master/foundry/issues/N` or `pull/N` links. No URL shorteners, redirects, userinfo, query strings, or arbitrary domains.
- Telegram notifications alone **never constitute approvals**. The bounded approval-contract candidate can recognize an exact founder callback for an ordinary task only after deterministic binding checks; it is not live or commissioned and cannot authorize reserved acts.
- Real Telegram sending requires explicitly provisioned `FOUNDRY_TELEGRAM_BOT_TOKEN` and `FOUNDRY_TELEGRAM_CHAT_ID`; do not store either in the repository, tests, log files or chat transcript.
- No live incoming approval service is activated. Existing callback code is simulation/offline validation only. Bot compromise must not change Foundry governance or invoke signed or reserved actions.
- Delivery failure results in an error, not a silent approval or successful task transition.
- The fixed chat ID should be restricted by external notification dispatcher policy; this script alone is **not** a secure production dispatcher.

## Offline verification

```sh
python3 -m unittest -v test_notify.py
python3 notify.py --kind INFO --title "Foundry test" --summary "Notification candidate dry-run" --link https://github.com/Bulldog-Master/foundry/issues/29
```

## Activation work remaining (separate authorization)

Use existing Foundry Agent Containment & Control and controller commissioning process to decide sender host, outbound network allowlist, root-held secret provision, and identity of recipients. Prove negative tests for outbound destination, bot token exfiltration, message spoofing, replay, duplicate notices, and PII/log leakage. Independently review any authority-bound approval-link service. Telegram must never become a signing or founder-authentication root.

**Stopping point:** candidate code review; **do not run with --send** until the appropriate release and secret-authority approvals.

## GitHub watch candidate (not activated)

`event_watch.py` checks only PR #28, PR #30 and Issue #29 through the read-only public GitHub API. Its first successful run creates a baseline without sending a message; subsequent changes generate one notification and update a root-owned local deduplication checkpoint only after Telegram confirms delivery. State failure preserves the previous checkpoint. It does not run unattended until separately authorized and scheduled on an approved notifications host. It does not decide approvals or task advancement.

Offline checks: `python3 -m unittest -v test_notify.py test_event_watch.py`. No bot token is needed for these tests. Any eventual service must use `/etc/foundry-telegram/bot-token` and `/etc/foundry-telegram/chat-id` from the trusted host, with root-owned permissions and independently authorized outbound access; the notifier must not be executed as an unprivileged implementation agent holding those secrets.

## Scheduled GitHub summaries (candidate)

- Daily: every day at **08:00 host-local**, previous rolling 24 hours.
- Weekly: Monday **08:05 host-local**, previous rolling 7 days.
- Monthly: first of every month **08:10 host-local**, previous complete UTC calendar month.
- Timers are `Persistent=true`: missed scheduled activations may run after WSL resumes, so delivery can occur later than the clock time.
- Source: public `Bulldog-Master/foundry` GitHub API only. Counts repository commits by GitHub committer timestamp, and PR/issue records by updated-at timestamp within the window. This is **not** a complete event chronology; actor-host actions, evaluator invocations, Telegram deliveries, and any private repositories are not included until independent durable sources are connected. Full record links are provided for surfaced PRs/issues.
- The sender's root-owned existing token and chat-ID files stay at `/etc/foundry-telegram/`; no token is committed.
- `python3 -m unittest discover -p 'test_*.py' -v` is offline and credential-free.
- The systemd units provided with this candidate must be reviewed, verified and installed deliberately on the existing notification host; they are not enabled merely by being committed to GitHub.

## Workstream accountability candidate (not yet deployed)

`accountability.py` adds tracked owner, next action, last observed GitHub update and explicit STALE/UNKNOWN flags for scanner review #29, architecture PR #28 and Telegram HQ PR #30. Default threshold: 24 hours. It explicitly **does not** equate GitHub updates or journal lines with successful execution. If sources are unavailable, status is UNKNOWN, never healthy. Stale work is flagged for coordination but **cannot be automatically dispatched**, because Foundry 1 prohibits automating evaluator assignment, gate routing and the still-uncommissioned Foundry 2 controller. The daily report includes these states after deployment. `test_accountability.py` covers stale, unknown, recent, closed and future-timestamp cases.

Immediate Telegram escalation and agent-first recovery need a separate, authorized controller event producer and delegation envelope; neither is made live by this patch. Verified host/agent progress requires immutable activity records outside the actor's writable domain. No new secret or permission is required for this read-only reporting candidate.

## Simulated Telegram button callback candidate

`callback_test.py` handles only the **already-created** simulation-only inline-button request, stored in `/etc/foundry-telegram/approval-test.json`. It verifies exact nonce + chat ID + message ID; acknowledges a callback with Telegram and records at most one test decision under a root-only local path. It never writes GitHub approvals, merges, signatures or actual founder decisions. `test_callback_test.py` covers exact binding, rejection, replay, unrelated callbacks and acknowledgment failures.

This is still development code, not a standing live callback service. Initial execution should be a one-shot offline test and then an authorized one-shot test handler; do not enable a polling service that processes real approval decisions. Telegram callbacks alone never satisfy founder-authentication requirements.


## Bounded Telegram approval front-end candidate

`approval_frontend.py` adds an **offline controller-contract layer** for ordinary bounded Foundry-Agent tasks. Telegram is the human approval interface, not the trust root. A callback produces a controller handoff only when the frozen task envelope, task ID, nonce, envelope SHA-256, founder Telegram user ID, chat ID, message ID, expiry, task hash, sandbox, workdir, explicit action list, repository, branch, expected head SHA and PR number where applicable all still match.

The currently modeled non-reserved repository actions are `commit`, `push`, `pr-create`, and `pr-update`. Authorization for one does not authorize another. Reserved actions—including merge, signing, production promotion, doctrine/governance changes, founder overrides, sealed-truth changes and provider authorization—are rejected by this candidate and remain on their stronger existing approval paths.

The approval record grants no standing authority and cannot survive a task-envelope or repository-target change. Before dispatch, the controller must re-read the current repository target and require an exact match on repository, branch, expected head SHA and PR number where applicable. Dispatch must revalidate expiry immediately before handoff, require a canonical workdir under `/home/foundry-agent/work/`, and require the controller-resolved real workdir to match the approved path so traversal or symlink-equivalent resolution cannot widen scope. Task hashes must be valid SHA-256 hex. `test_approval_frontend.py` covers exact approval/rejection binding, founder user/chat/message mismatch, nonce/hash mismatch, callback-time and dispatch-time expiry, reserved/unknown actions, stale/cross-action envelopes, non-canonical/traversal workdirs, resolved-workdir mismatch, invalid task hashes, repository/branch/head/PR drift, malformed or conflicting PR target bindings and replay.

This PR still **does not** activate Telegram polling, invoke Foundry-Agent, change PAUSE/KILL, provision new secrets, write GitHub from Telegram, or commission standing approval authority. Before live use, the controller-side pending-envelope store, decision record, launcher binding, evidence custody, bot/user/chat identity and one-shot approval -> task -> evidence -> PAUSE path require separate independent review and commissioning.
