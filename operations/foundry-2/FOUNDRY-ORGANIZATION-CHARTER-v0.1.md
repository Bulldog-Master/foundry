# Foundry Organization Charter v0.1

**Status:** DRAFT. Not ratified.
**Date:** 2026-10-11
**Companion:** `FOUNDRY-OPERATING-ARCHITECTURE-v0.1.md` (this document says who exists and who decides. The Architecture says where things run and how they communicate.)

## 0. Status and scope

This draft is not ADR-0003 ratification, Foundry 2 commissioning, Foundry 2 activation, an expansion of any current production authority, or authorization to implement the controller. It creates no agents, services, credentials, schemas, verifiers or conformance vectors. Foundry 1 remains the authoritative generation. Every "shall" is a proposal until the founder ratifies this Charter in a recorded founder act.

The founder approved three design decisions **for drafting only** (message of 2026-10-11):

- **D1.** Protected-branch merge stays founder-reserved through commissioning and shadow mode, using batched release decision cards. Any later relaxation is decided from shadow-mode evidence, stays narrowly scoped, and does not implicitly cover governance, security, controller, identity or other high-trust code.
- **D2.** Each product has its own reserved-act list from day one. ADR-0003 carries only the generic external-commitment rule. Routine activity is automatable only inside ratified envelopes.
- **D3.** The Executive Advisor may start internal investigations through typed proposals that the controller instantiates. They are read-only, source-cited, budget-capped and WIP-capped, and cannot reach secrets or sealed material or perform external or founder-reserved acts.

## 1. Principles

1. **Organization first, systems second, agents third.** Define the whole company now. Staff each function when its trigger fires.
2. **Founder by decision, not by procedure.** The founder decides reserved matters. The founder is never the relay, shell operator, file mover or GitHub operator.
3. **Chats are windows, not machinery.** Operational truth lives in controller state and GitHub. A chat that disappears loses nothing.
4. **Agent is not authority.** No role, model or chat gains authority by being useful. Authority comes from the founder through ratified documents and envelopes.
5. **Evidence invariant (ADR-0002).** No actor authors the record that proves its own compliance. Builder is not evaluator.
6. **Founder Interaction Principle.** Internal specialization must not require the founder to route work, transfer information, reconcile state or choose which agent to consult. If the founder must search conversations to learn current state, that is a design failure.
7. **Products drive Foundry.** A function with no recurring input and no consumer is defined, but not staffed or activated.
8. **Justification test.** Before anything is built, ask whether it directly reduces founder load, improves safety, enables ScoutProp, or creates durable capability we will use. If not, defer the build. The role card stays defined.

## 2. Authority in three layers

| Layer | Holds | Changed by |
|---|---|---|
| **Global** (ADR-0003) | Acts reserved to the founder everywhere, plus the generic external-commitment rule below | Founder, via ADR |
| **Product charter** (e.g. ScoutProp) | That product's reserved acts, budget, metrics and envelopes | Founder ratifies each product charter |
| **Ratified envelope** | Routine actions inside defined limits and a budget | Founder ratifies each envelope **class**. The controller instantiates inside a class. A new class is an authority widening. |

**Proposed ADR-0003 amendment (generic clause, reviewed separately):**

> External commitments are founder-reserved acts unless performed inside a founder-ratified envelope defined in a product charter. External commitments include: public statements or claims; pricing; contracts or acceptance of terms; spend beyond a ratified budget; communications to customers; collection, retention or deletion of customer data outside ratified policy; and legal or regulatory representations. Widening such an envelope is an authority widening.

ADR-0003 governs the global reserved list and is not restated here. If the two differ, ADR-0003 wins. The closed-list rule is unchanged: anything not reserved, not stopped by a fail-closed rule, and inside a ratified envelope class is automatable.

## 3. Function states and activation

- **ACTIVE:** staffed and operating.
- **LEAN:** minimum scope with a deterministic core. An LLM is added only where a recurring need justifies it.
- **DEFINED-DORMANT:** the role card exists. There is no agent, credential, budget, event subscription or authority.

**Activation.** Each row names a trigger and the state it moves to. When the trigger fires, the controller records the event and the move is automatic if it needs nothing beyond what the ratified Charter already authorizes. It requires a founder act if it needs new credentials or provider authority, spend beyond the ratified budget, a new envelope class, or any reserved act. Ratifying this Charter pre-approves every row's trigger and scope and nothing outside the row.

**Staffing is not authority.** Activating a function creates a worker with leases and a budget cap. It does not enlarge the envelope classes it may use.

## 4. Organization chart

```
BULLDOG: Founder / Owner (reserved acts and ratifications only)
│
├─ EXECUTIVE ADVISOR        read-only; front-door persona; briefs; investigation proposals
│
├─ CONTROL OFFICE           deterministic, no LLM; foundry-controller-1
│   ├─ PLANNER / OPERATIONS Hermes slot (replaceable); sequences work, drafts plans
│   │   └─ WORKERS on leases  Engineering, Research, Product analysis, business workers
│   └─ EXECUTION SERVICES   Caller-1, Sandbox-1 (infrastructure, not departments)
│
├─ SECURITY & RISK          threat model, baselines, key custody, incidents
├─ INDEPENDENT ASSURANCE    four gate evaluators; nothing else
├─ FRICTION AUDITOR         staff to Bulldog; read-only; capped queue
│
└─ BUSINESS FUNCTIONS       Product & Strategy · Sales · Marketing/Brand/Comms
                            · Customer Success/Support · Finance & Procurement
                            · Legal/Compliance/Privacy · Data & Analytics
                            · Partnerships · People/Contractors
```

**"Foundry Lead" is retired as an agent role.** Its duties are distributed: program state to the controller, sequencing to the Planner, cross-function reconciliation to the Advisor's brief. A chat with that name may remain as a window. It holds no authority or state.

## 5. Functions

Every function escalates to the controller's decision-card path, and the recipient is Bulldog unless a row names another.

### 5.1 Core functions

**Executive Advisor**
- **State:** ACTIVE (lean from day one).
- **Mission:** Tell the founder what changed, what matters, what can continue without them, and what only they can decide. Challenge the founder. Separate fact, inference and opinion. Track external developments.
- **May:** Read controller projections and cited external sources. Submit typed proposals, including D3 investigations.
- **May not:** Use side-effecting tools. Reach secrets, sealed truth or blinded evaluator material. Execute anything. Let external content enter instruction position.
- **Metrics:** One-screen brief with at most two decisions, citation coverage, decisions surfaced versus found missing later.

**Control Office (controller)**
- **State:** LEAN now (temporary controller on Bulldog-Surface WSL). ACTIVE at commissioning on `foundry-controller-1`.
- **Mission:** Durable state, hash-chained log, envelope enforcement, scheduling, budget ledger, status, notifications, PAUSE/KILL.
- **May:** Issue short-lived signed authorizations to execution services. Instantiate work inside ratified envelope classes.
- **May not:** Contain an LLM. Plan. Let one process hold more than one key class. Alter audit records. Perform founder-reserved acts.
- **Metrics:** Founder touches per PR, uptime, recovery time, restore-test pass.

**Planner / Operations (Hermes seat)**
- **State:** LEAN with interim planners (Codex and Claude workers). The Hermes seat is DEFINED-DORMANT until Hermes passes Candidate Admission.
- **Mission:** Decompose and sequence work, monitor progress, draft remediation plans. Hermes plans, the controller authorizes.
- **May:** Submit proposals to the controller queue. Use leased worker environments.
- **May not:** Hold any credential beyond the proposal queue. Merge, publish, evaluate, change envelopes, access sealed truth, close hard stops, or self-certify.
- **Metrics:** Plan accuracy, cost per accepted deliverable, rework rounds.

**Security & Risk**
- **State:** LEAN. Three duties now: the threat model, the baselines (Sandbox v1, key custody), and incident response.
- **Mission:** Design, monitor and protect. Organizationally distinct from Engineering. Does not grade itself.
- **May:** Propose controls. Operate monitoring. Declare an incident and invoke PAUSE.
- **May not:** Act as the independent security evaluator. Close its own hard stops. Resume after KILL.
- **Metrics:** Open incidents, time to contain, baseline drift, unreviewed credentials.

**Independent Assurance**
- **State:** ACTIVE (BOOTSTRAP-0 now, commissioned path later).
- **Mission:** Four-gate evaluation (Architecture, Security/Cryptography, Privacy/Metadata, Quality/Verification) of sealed packets.
- **May:** Return gate verdicts and findings. Publish as `foundry-evaluator[bot]` through the publisher.
- **May not:** Remediate. Hold content-write authority. See producer reasoning. Author identity or independence claims.
- **Metrics:** Rounds to convergence, malformed outputs, stale results, unique catches, false positives, cost.

**Friction Auditor**
- **State:** LEAN. A deterministic counter comes first. An LLM narrator is added after the metrics exist.
- **Mission:** Measure where the founder and the organization lose time. Escalates to the Advisor.
- **May:** Read a sanitized event export. Open improvement candidates into a capped queue (at most two open).
- **May not:** Implement its own recommendations. Touch governance, evaluator configuration, or its own charter and metrics.
- **Metrics:** Founder touches, retries, evaluation rounds, failed transfers, wait times, auth failures, decisions auto-defaulted (sample-audited).

### 5.2 Operating functions

| Function and mission | State → trigger | May | May not | Metrics |
|---|---|---|---|---|
| **Engineering:** build, test and release code | ACTIVE | Workers commit as `foundry-operator[bot]` to non-protected branches inside envelopes. Use Sandbox-1. | Evaluate own work. Merge to protected branches. Sign. Touch evaluation evidence. | Cycle time, escaped defects, remediation rounds, cost per accepted deliverable |
| **Product & Strategy:** problem, roadmap, priorities, per-product P&L view, lifecycle | ACTIVE (ScoutProp first) | Draft product charters and roadmaps. Prioritize inside budgets. | Authorize a new product. Set pricing, launch or public claims outside an envelope. | Validation evidence quality, stage time, signal-to-roadmap latency |
| **Reliability / SRE:** keep Foundry running if a chat, Codex, the laptop, a worker or Hermes dies. Degrade safely when a provider fails. | LEAN: health checks, backups, restore tests, key rotation | Operate backups and monitoring. Restore under a recorded procedure. | Change baselines (Security's) or envelopes | Availability, recovery time, failed jobs, manual recoveries |
| **Research & Market Intelligence:** technology, competitors, markets, regulation, threats. Feeds Advisor and Product. | LEAN | Read cited external sources through a stripping fetch step. | Use side-effecting tools. Put fetched text in instruction position. | Citation coverage, usefulness |
| **Finance & Procurement:** budgets, caps, vendors, billing, pricing analysis | LEAN (budget ledger) → full at first revenue, first paid vendor beyond infrastructure, or ScoutProp stage 4 | Enforce caps. Report spend. Analyze pricing. | Spend beyond budget. Add a vendor. Set pricing. | Spend versus cap, cost per accepted deliverable, runway |
| **Legal / Compliance / Privacy:** terms, privacy policy, licenses, data handling, store and payment rules, provider terms (e.g. FND-PRIV-001) | DEFINED-DORMANT → LEAN at stage 4 or on the first public-facing document. Provider and dependency terms review runs on request before then. | Review and draft. Mark documents approved for envelope use. | Publish terms. Make legal or regulatory representations. Give final legal advice (counsel handles binding matters). | Checklist completion, open items, review time |
| **Data & Analytics:** product, funnel and unit-economics metrics | DEFINED-DORMANT → LEAN when ScoutProp is instrumented or the controller emits its first product metric | Read analytics projections. | Collect a new category of customer data outside policy (escalates to Legal) | Metric freshness, data-quality failures |

### 5.3 Commercial functions

All DEFINED-DORMANT until the trigger fires. Each moves to LEAN.

| Function and mission | Trigger | May | May not | Metrics |
|---|---|---|---|---|
| **Sales:** pipeline, outreach, deals | ScoutProp stage 4 with approved positioning and a ratified pricing and discount envelope | Draft outreach. Send approved templates to approved segments. Apply discounts up to the cap. | Contracts, terms, non-template claims, outreach beyond the envelope | Pipeline, conversion, cycle length, discount rate |
| **Marketing / Brand / Comms:** positioning, content, launch, site, social | Positioning approved and the claims register has entries | Draft content. Publish preapproved posts and campaigns inside the envelope and budget. | Any public claim without a register entry. Ad spend beyond cap. Crisis or press statements without a founder act. (Legal reviews claims.) | Reach, acquisition cost, register coverage, takedowns |
| **Customer Success / Support:** onboarding, tickets, feedback to Product, retention | First beta or paying user | Reply from approved templates. Take policy-defined account actions. | Refunds or account actions outside policy. Customer data access beyond need. (Escalates to Product, Legal, then Bulldog.) | First response, resolution time, churn, satisfaction |
| **Partnerships:** research and manage partner relationships | A named partnership proposal or founder directive | Research and draft. | Commitments. Disclosing non-public information. | Qualified partners, outcomes |
| **People / Contractors:** engagements, access scoping, offboarding. No hiring is contemplated. | First contractor or outside engagement | Prepare scopes. | Engage anyone. Grant access. | Access reviews on time, offboarding completeness |

### 5.4 Execution services (infrastructure, not departments)

- **Caller-1:** controlled external-provider execution, one authorized job at a time inside its frozen contract. It holds no scoring, fusion, adjudication, governance, founder-approval or sealed-truth authority.
- **Sandbox-1:** untrusted-code execution on frozen Production Baseline v1 (57/57 PASS). Isolation experiments belong to Baseline v2 clones.
- They are separate trust domains. Only the controller talks to them. They never talk to each other. Open questions about Caller-1's frozen contract are in Architecture section 11.

## 6. Product lifecycle (controller state)

| Stage | Owner | Exit evidence | Founder act |
|---|---|---|---|
| 1. Authorize | Product | Problem, customer, success metric, budget | New product |
| 2. Validate | Product, Research | Evidence a stranger would pay | None |
| 3. Build | Engineering | Four gates PASS on the release candidate | Protected-branch merge (batched card) |
| 4. Prelaunch | Product, Legal, Security, Finance | Terms and privacy reviewed, pricing proposal, claims register complete, support ready, instrumentation, rollback plan | Pricing, terms, public launch |
| 5. Launch | Marketing, Sales | Launch runs inside the ratified envelope | None unless outside the envelope |
| 6. Operate and learn | Customer Success, Data, Product | Signals reach Product through the event log | Production promotion where reserved |

Dormant functions activate at the stage in their trigger, not at launch.

**Product charter** (one per product): customer and problem; lifecycle stage; reserved-act list; envelope classes; budget and spend caps; metrics; claims register location; data-handling policy; open TBDs.

**ScoutProp charter (skeleton).** The first full product and business proving ground. These fields are **TBD: founder/product decision** and do not block this Charter: pricing, discount limits, channels, target customer, launch criteria, refund policy, data-retention rules, spend caps, public-claim list. Initial reserved acts: pricing, launch, terms and privacy claims, customer-data rules, refunds and discounts outside policy, spend beyond cap.

## 7. Claims register

Every public claim about a product (features, security, privacy, performance) is a record linked to evidence. Marketing and Sales cannot publish a claim without an entry. A security or privacy claim passes the relevant Assurance gate before the entry is usable. Retired claims are kept.

## 8. Self-improvement

Foundry learns. Models do not retrain themselves. Agents improve because Foundry changes the instructions, checklists, tests, tools, permissions and autonomy limits around them, based on measured evidence. The underlying model may stay the same.

### 8.1 Three change tiers

1. **Tier 1, operational tuning inside an envelope** (timeouts, templates, scheduling): automatic and logged.
2. **Tier 2, process and documentation changes:** a normal PR through the gates.
3. **Tier 3, reserved:** governance, gate logic, evaluator prompts and configuration, authority and envelope classes, controller code, and the Friction Auditor's charter and metrics.

The improver never edits its own measurement or its own judge. Improvement candidates are WIP-capped. Founder-load metrics come from the event log, not agent narrative.

### 8.2 Learning loop

Every incident, hard stop, remediation round, friction finding and evaluator catch is recorded as a **learning event**: a typed entry the controller writes from the event log. Learning events are telemetry, not documents.

```
learning event -> deduplicate / cluster -> lesson candidate
-> evidence + root cause -> Tier 1 / 2 / 3 change -> measure again
```

The Friction Auditor or Independent Assurance consolidates clusters into lesson candidates. Only a material, recurring or systemic candidate becomes a reviewed **lesson**, which is a document in git. A lesson changes behavior only through the tiers above.

**Replay check.** Once a replay corpus exists, a change to worker instructions, templates, checklists or planner heuristics runs against a frozen set of past tasks and must not worsen accepted-deliverable rate, cost or rework. The controller computes the result, never the proposing agent. A smaller **held-out set** sits outside the proposer's read and write authority, and the change must hold on it too. Until a corpus and held-out set exist, such changes go through a normal Tier 2 PR with no replay claim.

**Ratchet toward determinism.** Repeated knowledge moves out of model memory and into infrastructure whenever possible: lesson, then checklist, then test, then deterministic rule. Agents spend their effort on novel problems.

**Evaluators.** An evaluator is never tuned on the work it judges. Changing an evaluator profile is a Tier 3 process: a frozen calibration corpus, a comparison of the old and candidate profiles, and version-bound adoption.

**Knowledge** lives as reviewed documents in git. There is no unreviewed agent memory shared across roles.

**Projects teach projects.** A lesson from one product (for example a launch-readiness gap found in ScoutProp) updates the shared lifecycle checklists, so the next product starts from the improved baseline.

### 8.3 Autonomy ladder

Every envelope class sits on one rung:

1. **SHADOW:** the agent proposes and existing authority decides.
2. **SUPERVISED:** the agent acts and every result is gated. The founder sees batches, not items.
3. **ENVELOPE:** the agent acts inside its limits and only exceptions surface.
4. **WIDENED:** larger limits, ratified by the founder.

Moving up is a founder act, presented as a **promotion proposal** built from log evidence (runs, escaped defects, rework, cost, incidents). The evidence thresholds are set per class by risk. None are fixed here. Moving down is automatic on defined triggers (an incident in the class, an escaped defect, a budget breach) and is logged. Going back up is a new proposal.

**Autonomy is version-bound.** A rung attaches to a tested tuple: worker model, controller version, instructions and prompts, toolset, permissions, runtime environment, and the envelope class definition. The controller records a hash of the tuple. Any change to a tuple element is material by default. After a material change the class falls to SUPERVISED, or to SHADOW if permissions or tools widened or the model family changed, even with no incident. A prior rating never transfers.

**Capability registry.** What each tested tuple has demonstrated (task types, evidence, cost, rung) is a view over tuple records, not a separate system. The planner assigns work from it by proven capability instead of model reputation. Build it when there is something to route.

**Founder load.** Routine founder terminal commands, file transfers, agent-relay actions and PR operations target zero. Founder-decision volume (cards per week, batching rate) and decisions auto-defaulted are measured and sample-audited, so the target cannot be met by hiding decisions.

**Advisor investigations (D3)** need a cited source. A poisoned external source must not trigger a flood, so uncited triggers are rejected.

## 9. Document review rules (this Charter and the Architecture)

- **Severity and routing are separate.** A MINOR finding that is an integrity anomaly, trust-boundary defect or security issue, or one of several MINORs exposing a systemic invariant failure, still stops progression under the applicable routing rule. A MINOR implementation or wording defect returns to the author without a stop.
- **Two-round cap.** Unresolved issues after round two stop the review and produce **one founder decision card**. The cap never means remaining findings are accepted or waived. Only a recorded founder act can waive a finding.
- One independent review of the exact head. A valid non-PASS result is not re-run for the same head.

## 10. Open items

- Ratification of this Charter (founder act).
- ADR-0003 generic external-commitment amendment, reviewed independently.
- ScoutProp charter fields (section 6).
- Hermes Candidate Admission outcome.
- Notification channel for founder decision cards (Architecture section 8).
