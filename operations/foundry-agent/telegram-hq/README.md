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
