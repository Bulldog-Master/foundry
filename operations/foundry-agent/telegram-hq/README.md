# Foundry HQ Telegram — notification-only candidate

**Status:** Development candidate, **not installed, activated, or authorized for credentials**.

This narrowly scoped transport sends status messages containing links to already-existing Foundry GitHub issues/PRs. It **does not** implement Telegram webhooks, bot commands, approval buttons, approval receipts, controller scheduling, evaluator routing, or protected actions.

## Why this is intentionally limited

Foundry-Agent is commissioned for bounded implementation, while current Foundry 1 VERSION.md expressly excludes an adopted orchestration layer and automated gates. ADR-0003 (Foundry 2) is still **PROPOSED**. A notification-only code candidate does not amend either authority boundary or activate the proposed controller.

## Behavior and trust boundary

- No third-party Python dependencies. Runs in offline dry-run mode without secrets.
- Only accepts `https://github.com/Bulldog-Master/foundry/issues/N` or `pull/N` links. No URL shorteners, redirects, userinfo, query strings, or arbitrary domains.
- Telegram messages **never constitute approvals**. An ACTION_REQUIRED message is only a navigational notice to a GitHub review; no decision is inferred.
- Real Telegram sending requires explicitly provisioned `FOUNDRY_TELEGRAM_BOT_TOKEN` and `FOUNDRY_TELEGRAM_CHAT_ID`; do not store either in the repository, tests, log files or chat transcript.
- No incoming updates and no credential access other than the single designated outbound bot token. Bot compromise cannot change Foundry governance or invoke signed actions.
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
