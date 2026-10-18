# Foundry Operating Architecture v0.1

**Status:** DRAFT. Not ratified.
**Date:** 2026-10-11
**Companion:** `FOUNDRY-ORGANIZATION-CHARTER-v0.1.md` (the Charter says who exists and who decides. This document says where things run and how they communicate.)

## 1. Scope and status

This draft is not ADR-0003 ratification, Foundry 2 commissioning, Foundry 2 activation, an expansion of any current production authority, or authorization to implement the controller. Foundry 1 stays authoritative. Nothing here changes Caller-1's or Sandbox-1's frozen baselines. BOOTSTRAP-0 is not Foundry 2 commissioning evidence.

Requirements are written as **R-numbers** so the controller commissioning scope can cite them. They are design requirements, not implementations. No schemas, verifiers or conformance vectors are created here.

## 2. Machine and process map

| Component | Machine | Service identity | Purpose and authority | Credentials held |
|---|---|---|---|---|
| Founder surface | Bulldog-Surface (Windows) | Bulldog-Master (human) | Decisions, status view. Sole holder of reserved acts. Not workflow infrastructure. | Hardware key for founder acts |
| Dev workstation | Foundry-Agent WSL (Bulldog-Surface) | `foundry-agent` | Temporary controller today. Dev workstation only after controller-1 is live. | None for Foundry infrastructure after the transition |
| Controller | `foundry-controller-1` (dedicated always-on Linux, separate provider account from Caller-1 and Sandbox-1) | `foundry-controller` | State, hash-chained log, envelopes, scheduler, budget ledger, status API, PAUSE/KILL. No LLM. | State database, Caller authorization signing key |
| GitHub operator broker | controller-1 | `foundry-broker` | Branch, commit, PR and comment operations as `foundry-operator[bot]`. No protected-branch merge. | Operator GitHub App key |
| Evaluator publisher | controller-1 | `foundry-publisher` | Posts validated evaluator results and the required status check as `foundry-evaluator[bot]`. No content write. | Evaluator GitHub App key |
| Notifier | controller-1 | `foundry-notifier` | Founder decision cards and status pushes. | Notification channel token |
| Evaluator invoker | Caller-1 job type or a separate Caller-2 (decision in section 11) | `foundry-evaluator-invoke` | Tool-less Anthropic Messages API call over a sealed packet. Validates schema and derives routing. | Anthropic API key (workspace-scoped) |
| Standalone | Standalone (Linux lab) | per-role unix users | Planner (Hermes slot), workers on leases, Advisor and Auditor as tool-less scheduled jobs, Research. | Proposal-queue token only |
| Caller-1 | `foundry-caller-1` | existing | Controlled external-provider execution within its frozen contract. | Provider keys, verification key |
| Sandbox-1 | `foundry-sandbox-1` | existing | Untrusted-code execution, Baseline v1 frozen. | None beyond runtime |
| Evidence anchor | Off-host write-once store (placement in section 11) | `foundry-anchor` | Holds the log's chain head outside the controller's write reach. | Append-only anchor-write token |

**R-2.1** The controller runs as four processes, one per trust boundary: controller (state, log, scheduler, status), broker, publisher, notifier. More services require a recorded justification.

**R-2.2** Bulldog-Surface and its WSL hold no agent credentials once controller-1 is live. Only the founder's hardware key remains.

## 3. Key custody and trust boundaries

**R-3.1 Key separation.** In v0.1 the controller, broker, publisher and notifier share one host, `foundry-controller-1`. Separation is by Unix user, process, systemd unit, filesystem permissions and credential. No Unix user or process holds two of: operator App key, evaluator-publisher App key, Caller authorization signing key. Key material is not cross-readable between those users. The evaluator API key is never on the controller host. It lives only on the evaluator invoker host.

**R-3.1a Residual risk (accepted for v0.1, to be restated at commissioning).** Root compromise of `foundry-controller-1` defeats user-level separation and yields the operator, publisher and Caller signing keys together. It cannot merge to a protected branch, because that is founder-reserved. Compensations are required: founder merge from a hardware key, chain-head anchoring off the host (section 5), tested App permission ceilings, and the R-3.4 external kill path. If ScoutProp release gates raise the stakes, the first split is moving the publisher to its own host.

**R-3.2** The publisher holds the App key. The evaluator never does.

**R-3.3 Fail idle on controller death.** Authorizations to Caller-1 and Sandbox-1 are short-lived and signed. If the controller dies or is stopped, authorizations lapse and work stops. This covers a dead controller, not a compromised one. A compromised issuer can keep issuing, so R-3.4 does not rely on expiry.

**R-3.4 External kill.** Commissioning must prove at least one founder-controlled kill path outside the controller's authority, one the controller cannot override even if compromised. Candidates include a provider-console power or network cut of `foundry-controller-1`, a firewall or ACL cut between the controller and Caller-1 and Sandbox-1, revoking both GitHub App installations, and revoking provider and API keys at the provider. Any Caller-side mechanism must work without modifying Caller-1's frozen verifier or baseline, and commissioning verifies that against the frozen contract. The mechanism is chosen at commissioning. The path is documented and tested.

**R-3.5** Caller-1 and Sandbox-1 have separate authorization keys and separate administrative paths. They never talk to each other. The shared SSH-identity arrangement on the temporary controller is accepted only until controller-1 is live.

**R-3.6 Standalone containment.** Separate unix users per role, no shared writable paths, an egress allowlist, a tool-less Advisor, disposable worker environments per lease. Standalone never holds a merge, publisher or founder credential.

**R-3.7 Model-family diversity.** Where feasible the evaluator model family differs from the producer family for the same change.

## 4. Identity model

Three external GitHub identities only:

| Identity | Use | Limits |
|---|---|---|
| `Bulldog-Master` | Founder acts only, hardware-key backed, signed commits and approvals | Never used by agents |
| `foundry-operator[bot]` | Routine automated repo work: branches, commits, pushes, PR create and update, remediation commits, routine issues | Non-protected branches. No admin, no merge to protected branches, no protection changes. |
| `foundry-evaluator[bot]` | Review and status-check publication | Reviews and checks only. No content write. |

**R-4.1** `Bulldog-z` is retired from the normal workflow and is not used for approvals or independence evidence. The recommendation is to delete it and use offline recovery codes, not to keep a standing backdoor account.

**R-4.2** Internal worker attribution (which worker, which lease, which envelope) lives in controller records, not as per-worker GitHub accounts.

**R-4.3** A founder act must come from the founder's own authenticated session or a key no agent holds. No agent may set or pre-complete a founder-controlled field.

**R-4.4** Installing the Apps, setting their permissions and creating the hardware-backed signing arrangement are founder credential acts.

## 5. Controller requirements

**R-5.1** No LLM in any controller process.

**R-5.2** Envelope enforcement is deterministic. A request outside a ratified envelope class is rejected and logged, never queued for an agent to decide.

**R-5.3 Budget ledger.** Every envelope carries a spend cap. Provider spend is recorded against it and enforced as a hard stop. This matters because the provider workspace offers no spend limit.

**R-5.4 Log.** Append-only, hash-chained, with periodic chain-head anchoring to the evidence anchor. A broken chain is an INTEGRITY_ANOMALY and a hard stop.

**R-5.5 PAUSE / KILL / RESUME.** PAUSE and KILL are available to Security and the founder. Resuming after PAUSE or KILL is a founder act.

**R-5.6 Backup and restore.** Backups and a tested restore from backup exist before activation.

## 6. Event and state rules

**R-6.1 Typed events.** Events carry typed fields and references. Free text from outside the company (PR titles, customer messages, web content) travels in a quarantined data field and is never placed in instruction position for any agent.

**R-6.2 Single writer.** One writer per state domain. Agents submit proposals. The controller commits.

**R-6.3 Projections.** Advisor, Auditor and business functions get read-only projections of the state. Subscriptions are by event type and authorization.

**R-6.4 Event table.** The event bus is an append-only table in the controller database. A message-queue or workflow engine requires a recorded justification and review.

**State entities (first set):** Product, Project, PR, Branch, Release, Job, Evidence, Finding, Decision, Risk, Incident, Envelope, Budget, Claim, Agent lease, LearningEvent, Lesson, Autonomy rung (bound to a tuple hash). The capability registry is a view over tuple records, not an entity. Customer, Opportunity and Metric entities are defined now and populated when their functions activate.

**Starter event types:** PR_OPENED, PR_UPDATED, BUILD_PASSED, BUILD_FAILED, EVALUATION_STARTED, EVALUATION_COMPLETE, HARD_STOP, REMEDIATION_COMPLETE, INCIDENT_OPENED, INCIDENT_RESOLVED, FRICTION_FINDING_CREATED, INVESTIGATION_PROPOSED, FOUNDER_DECISION_REQUIRED, PROMOTION_READY, FUNCTION_ACTIVATED. Business events (CUSTOMER_SIGNAL, SALE_WON, CHURN_RISK and similar) are defined when their function activates.

**Knowledge domains** are directories of reviewed documents in git: engineering, security, operations first. Others when the function activates.

## 7. Evidence and review flow

1. A work request becomes a versioned envelope.
2. Workers build as `foundry-operator[bot]` on a non-protected branch.
3. The controller validates, builds the sealed review packet bound to an exact head, and dispatches it to the evaluator invoker.
4. The invoker returns a validated result. The controller derives routing from the routing table. A mismatch invalidates the result.
5. The publisher posts the result and the status check.
6. The controller routes: CONTINUE, RETURN_TO_OPERATIONS, HARD_STOP, or ESCALATE_FOUNDER.

**R-7.1 Fail-closed retry.** Retry is allowed only where frozen policy deterministically proves that no evaluator judgment was produced (for example an empty provider response). Adverse or ambiguous content never creates retry eligibility. The raw response, attempt number, hashes and head binding are always retained. Resealing the same head never erases a valid non-PASS result.

**R-7.2 Stale heads.** A result is bound to its evaluated head. Stale results never become approval. Head checks occur at acceptance, publication and before any founder action card.

**R-7.3 Integrated remediation.** Remediation uses the full finding set, root-cause and invariant analysis, one complete correction, the full deterministic suite and adversarial tests, regenerated evidence, hash verification against the final files, then a new head and a new evaluation. Piecemeal patch-and-resubmit loops are not used.

**R-7.4 Evaluator independence.** The evaluator never authors identity or independence claims. Builder is not evaluator (ADR-0002).

**R-7.5 Review convergence** follows Charter section 9.

## 8. Front door (Foundry HQ)

Foundry HQ is an **interface over controller state**. It is not an agent and not a new source of truth. It consists of a status view, decision cards, and the Advisor as default conversational persona.

**R-8.1** Chats and agents are replaceable windows (Charter principle 3). If Claude, Codex or a chat disappears, state and obligations remain in the controller and GitHub.

**R-8.2 Decision card.** A founder action card shows: reason, subject (PR or item), exact head or version, evaluation summary, open hard stops, and the single requested action. Routine work produces no card.

**R-8.3 Status view.** Every job exposes repository, PR, exact head, phase, packet hash and size, config, runtime and task hashes, attempt, validation results, gate results, publication state, next action, founder action required, and hard-stop reason.

**R-8.4 Notification channel.** One channel for decision cards and incident alerts, chosen by the founder (section 11).

**R-8.5 Daily brief.** One screen, at most two founder decisions, sources cited, facts and inferences labeled.

## 9. Merge model

Per D1, protected-branch merge remains founder-reserved through commissioning and shadow mode.

**R-9.1** Routine work lands on an unprotected integration branch. The founder merges to main in **batched release decision cards**, one per release, each showing all included heads and their gate results.

**R-9.2** Governance, security, controller, identity and other high-trust paths always require a card of their own. Any later relaxation is decided from shadow-mode evidence, stays narrowly scoped, and excludes these paths by default.

## 10. Failure and recovery

| Failure | Behavior | Recovery |
|---|---|---|
| Controller down | Authorizations lapse. Work idles. Nothing runs unattended. | Restore from backup, replay log, verify chain head against anchor |
| Broker or publisher key compromised | That App's writes stop. Checks stay pending, so merges are blocked. | Revoke and rotate the App key |
| Evaluator provider down or invalid output | Hard stop on invalid output. Transport errors consume no attempt. | Retry per R-7.1. Escalate if persistent. |
| Hermes or a worker misbehaves | Bounded by lease, budget cap and envelope. | Revoke lease, rebuild disposable environment |
| Standalone compromised | No merge, publisher or founder credentials there. Damage limited to bad plans and wasted budget. | Rebuild, rotate proposal-queue token |
| Caller-1 or Sandbox-1 fault | Fail closed, reject invalid authorizations | Frozen baseline restore |
| GitHub unavailable | Controller queues locally and does not merge. Founder cards are paused. | Resume when available. Local log is authoritative for state. |
| Founder unreachable | Work already inside ratified ENVELOPE or WIDENED classes and existing budgets continues. Reserved decisions queue. The system does not widen authority, promote autonomy, add credentials or providers, exceed budgets, merge protected or high-trust changes, or make external commitments needing founder approval. Work that reaches a reserved act waits. A founder-set maximum unattended period applies (section 11). | Founder returns to a queue of decision cards. |

## 11. Open decisions and dependencies

1. **Caller-1 contract questions.** Answer each from the frozen contract, not from convenience, and do not modify the frozen baseline to find out. (a) Does the evaluator-invocation job type fit, or is a Caller-2 needed? (b) Does the proposed Caller-side revocation mechanism fit the frozen contract (R-3.4)?
2. **Hosting for controller-1** (provider, size, separate account) and **placement of the evidence anchor** (an off-host write-once store the controller cannot rewrite).
3. **Notification channel** for decision cards.
4. **Hardware key and signing method** for founder acts.
5. **Founder continuity:** a documented procedure for extended unavailability, including the founder-set maximum unattended period after which no new work starts and in-flight work completes, and who, if anyone, holds a break-glass path.
6. **External single points of failure:** GitHub, Anthropic (sole evaluator provider), OpenAI (worker side). Degradation plan for each.
7. **Duplicate controller design documents** (`operations/FOUNDRY-2-CONTROLLER-DESIGN-v0.1.md` and `operations/FOUNDRY-CONTROLLER-v0.1-DESIGN.md`): one is marked superseded by this Architecture.

## 12. Carried design debt (PR #26 override)

The founder override on PR #26 accepted four findings. They are inputs to the controller commissioning scope, not closed.

- **FND-SEC-001:** replace the denylist adverse-signal retry rule with R-7.1.
- **FND-SEC-002:** dependency pins carry hashes (`--require-hashes`).
- **FND-PRIV-001:** a provider-terms transmission block needs a recordable decision. Owner: Legal (review) and the founder.
- **FND-QUAL-003:** make the zero-byte timeout behavior consistent.

FND-QUAL-001 and FND-QUAL-002 were corrected after evaluation and not re-evaluated. They are independently verified before commissioning. The PR #26 override is not PASS evidence, implementation authority, commissioning authority or activation authority.

## 13. Critical path

1. **Identity and signing:** Apps installed, founder acts signed, Bulldog-z retired.
2. **ADR-0003 and review debt:** independent ratification review, generic external-commitment amendment, section 12 items folded into the controller scope.
3. **Controller MVP (commissioning scope and build as one):** log, state, status, notifier, broker, publisher, budget ledger. No Hermes. Success: one ordinary PR with zero founder relays.
4. **Shadow operation with synthetic fault injection:** forbidden and reserved acts reject, stale heads reject, evidence cannot be overwritten, identity boundaries, evaluator isolation, retry semantics, restart, PAUSE/KILL, restore from backup.
5. **Founder activation packet:** one consolidated decision.
6. **Hermes admission and integration:** after Candidate Admission, behind a replaceable planner interface.
7. **ScoutProp lifecycle activation:** business functions activate on their Charter triggers.

## 14. Non-goals

A message-queue or workflow engine, vector stores or shared memory, per-worker GitHub identities, an LLM Friction Auditor before the metrics exist, a custom HQ web app before the status API exists, Jev or Laya, automatic governance changes, further contract versions beyond what the controller scope needs, per-PR founder cards for routine work, and any retention of Bulldog-z.
