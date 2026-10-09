# Foundry Delegation and Escalation v0.1.1

- **Type:** Ratifiable operational policy
- **Status:** v0.1 ADOPTED; v0.1.1 APPROVED pending integrity-record closure; Lane A is not activated
- **Owner and final authority:** Bulldog (founder)
- **Founder adoption of v0.1:** APPROVED — directly confirmed by Bulldog for PR #21
- **Effective date of v0.1:** 2026-10-09T20:43:03Z — policy only; not Lane A activation
- **Founder approval of v0.1.1:** APPROVED — Bulldog's direct PR #23 review and comment on 2026-10-09
- **Effective date of v0.1.1:** Upon founder merge of the exact independently reviewed integrity-closure PR; policy only, not Lane A activation
- **Ongoing independent verifier:** BLOCKED — founder must name an ADR-0002-qualified independent verifier before Lane A launch
- **Review trigger:** Any firewall failure, stop-the-line event, material anomaly, verifier-independence change, or proposed scope expansion

## 1. Purpose and authority ceiling

This policy permits bounded operational delegation in Lane A while keeping all
governance in Lane B. It is subordinate to the Constitution, ADR-0001,
ADR-0002, frozen protocols and baselines, and newer authoritative records. It
does not amend their approval, independence, evidence-custody, or failed-gate
requirements.

Delegation under this policy is authority to perform only the exact operational
actions inside a pre-authorized envelope. It never grants authority to decide
what work should pass, who should evaluate it, what an evaluator may see, how
evidence should be scored or combined, whether an exception is acceptable, or
whether a result may enter production.

The following remain exclusively in Lane B and may not be automated or
delegated to Lane A: gate routing; evaluator assignment or sequencing;
visibility-release decisions; scoring; fusion; adjudication; founder overrides;
production promotion; doctrine or policy adoption; merge into a protected
branch; signing; sealed-truth custody; security exceptions; trust-boundary
changes; and any other governance authority. An automated recommendation,
default, timeout, confidence score, or absence of objection cannot substitute
for the required human decision.

### Founder-authority field invariant

No agent, model, controller, script, workflow, or other automated actor may set,
complete, pre-complete, or represent as decided any field asserting founder
approval, adoption, override, activation, production promotion, or an equivalent
founder act. Automated actors may prepare drafts and supporting evidence, but
every such authority field must remain explicitly `PENDING` or `BLOCKED` until
the founder's act is directly recorded.

An account name, commit author, automation identity, prepared checkbox, inferred
intent, prior general authorization, or absence of objection is not a directly
recorded founder act. The authoritative record must identify the founder's
specific act and its evidence without relying solely on an identity or field an
automated actor could have written. This invariant does not disturb the valid
v0.1 adoption recorded for PR #21, which Bulldog directly confirmed.

## 2. Lane A / Lane B structural firewall

### Lane A — delegable operations

Lane A may inspect, diagnose, test, edit, and perform branch, commit, push, and
pull-request preparation or update work when every action is explicitly inside
a current, pre-authorized envelope. It may collect and format evidence, report
status, detect declared stop conditions, and propose Program State changes.
Lane A actions must be bounded, attributable, reversible where practical, and
incapable of crossing a Lane B boundary through credentials, permissions,
interfaces, defaults, or fallback behavior.

Lane A evidence work is limited to operational source artifacts and result
records. Lane A must not author, complete, alter, or submit a gate record or
gate conclusion as an evaluator. Gate evidence and outcomes remain independently
authored and reviewed by the authorized human actors under Foundry's manual
four-gate contract.

### Lane B — non-delegable governance

Lane B contains every reserved authority listed in Section 1. Lane B decisions
require the authorized human actor and the existing Foundry evidence and review
rules. Lane A may request or prepare a Lane B decision but must stop before it,
must not encode an outcome as already decided, and must not continue on an
assumed approval.

### Required structural separation

Before launch and throughout operation, the implementation must demonstrate
that Lane A lacks the credentials, permissions, write paths, service roles, and
decision interfaces needed to perform Lane B actions. Policy text, prompts,
role labels, and voluntary compliance are not sufficient structural controls.
The firewall must fail closed: an ambiguous action, missing authorization,
unavailable verifier, stale envelope, or attempted boundary crossing stops the
operation without a governance side effect.

Caller-1 and Sandbox-1 frozen production baselines remain untouched. A change
to a frozen baseline, production contract, containment boundary, privileged
dispatcher, signing path, evidence-custody path, or sealed-truth boundary is a
Lane B matter and is outside this policy's standing delegation.

## 3. Launch prerequisites and independent verification

Lane A must not launch until all of the following are recorded:

1. The founder has adopted this exact version and supplied its effective date.
2. The founder has named the ongoing independent verifier and recorded the
   verifier's qualification and independence basis under ADR-0002.
3. An independent pre-launch firewall verification has demonstrated that Lane A
   cannot exercise Lane B authority, including negative tests for every reserved
   authority in Section 1.
4. The verifier has confirmed the result-record, hashing, retention, exposure,
   sampling, stop-the-line, and independent-closure mechanisms are ready.
5. Any implementation-specific envelope, identities, permissions, endpoints,
   and rollback controls have been frozen or version-bound for launch.

The producer of the firewall or controller cannot be its sole verifier. The
verifier must not be controlled by Lane A and must retain independent access to
the authoritative evidence needed to verify containment.

## 4. Verification schedule

The named ongoing independent verifier must verify the first 10 delegated
operations at 100%. An operation counts toward the first 10 only after its
record and verification are complete; aborted or failed attempts remain
operations and do not disappear from the sequence.

After the first 10, the verifier must independently select and verify a random
sample of at least 10% of delegated operations. A sampling period closes after
each next block of 10 operations or at the end of each UTC calendar month,
whichever occurs first. The population cutoff is immutable once the period
closes, and the verifier selects the sample only after that cutoff. The sampling
method, population, selection, and result must be recorded so Lane A cannot
predict, suppress, replace, or frame the sample. Rounding is upward, and every
period containing delegated operations includes at least one sampled operation.

Regardless of sampling, independent verification is mandatory for:

- anomalies or suspected boundary crossings;
- failed, aborted, timed-out, or invalid work;
- privilege or identity changes;
- configuration changes;
- containment or trust-boundary changes; and
- any operation selected by the verifier or founder.

Mandatory-event verification is additional to the random minimum and cannot be
counted to reduce it.

## 5. Stop the line and independent closure

Any actor or control must stop the line immediately on an attempted Lane B
action, ambiguous authorization, firewall or containment failure, anomalous
result, missing or mutable evidence, verifier-independence concern, unexpected
privilege, or material configuration drift. Stop means no further delegated
operations, retries, repair-in-place, promotion, or restart under the affected
envelope.

Lane A may trigger a stop but cannot close its own stop. The named independent
human verifier is the independent stop closer unless the verifier is implicated
or not independent for the event; in that case the founder must name another
eligible independent human closer. Closure requires a retained incident record,
scope and exposure assessment, preserved evidence, corrective action where
applicable, independent re-verification, and the human closer's explicit
recorded decision to resume. A controller, model, script, workflow, default,
silence, elapsed time, or successful retry cannot verify closure or authorize
resumption.

## 6. Exposure tracking

Every delegated operation must record the identities, systems, repositories,
branches, environments, data classes, artifacts, credentials or capabilities
made reachable, and the start and end of that exposure. The record must state
what was actually accessed or changed, not only what the envelope permitted.
Unknown exposure is an anomaly and triggers stop-the-line and mandatory
verification.

Exposure history is retained across failures, aborts, retries, and revisions.
An actor with disqualifying exposure cannot become a blinded evaluator by
resetting its session or environment.

## 7. Program State reconciliation

Lane A may draft or propose a change to the Foundry Program State record. It
must label the proposal as un-reconciled and may not represent the proposed
state as authoritative. The Foundry Lead alone reconciles proposed Program
State changes against authoritative records and resolves duplication,
sequencing, and conflicts. Reconciliation does not itself confer founder
approval or any other reserved Lane B authority.

## 8. Delegated-operation result records

Each delegated operation must produce a durable result record containing at
least:

- unique operation ID and sequence number;
- authorizing envelope identifier and exact version/hash;
- requested and executed actions, actor identity, environment, start/end time,
  and outcome;
- relevant input, output, configuration, and changed-artifact identifiers and
  cryptographic hashes;
- exposure record;
- stop conditions, anomalies, failures, aborts, retries, and escalation events;
- whether verification was mandatory, first-10, randomly selected, or otherwise
  requested; and
- verifier identity, independence basis, findings, disposition, and closure
  reference when applicable.

The completed record and its manifest must be cryptographically hashed and
retained in an append-preserving location outside Lane A's sole control. Lane A
must not be able to delete, replace, select, or suppress authoritative result
records. Hashes establish change detection, not custody or truth.

Records must be retained at least through the lifetime of the authorization and
until every related verification, incident, stop, condition, and reassessment is
closed. Destruction thereafter requires an explicit founder-authorized retention
decision recorded outside Lane A; expiration or controller action cannot delete
the authoritative history.

## 9. Change and escalation discipline

Lane A stops and escalates before any action outside its envelope or touching a
Lane B authority. Ordinary operational errors inside the envelope may be fixed
and re-verified without founder involvement unless they trigger a mandatory
event or reveal a trust-boundary contradiction.

Any proposal to automate, delegate, approximate, or mechanically default a
Lane B function is outside this policy and requires a separately reviewed and
explicitly founder-adopted governance change. No operational evidence gathered
under this policy silently raises that ceiling.

## 10. Adoption record

Founder adoption made v0.1 the operational policy. Bulldog directly approved
the v0.1.1 substance in PR #23 while explicitly preserving Lane A inactivity,
all activation blockers, and the Hermes/controller and production-promotion
prohibitions. The correction becomes authoritative only when the PR #22
integrity record closes through founder merge of the exact independently
reviewed integrity-closure PR. Neither version activates Lane A. Lane A may
become active only when every activation field below is completed in the merged
authoritative record:

| Field | Required value |
| --- | --- |
| Adopted policy version/hash | v0.1; final SHA-256 recorded in PR #21 |
| Founder adoption decision for v0.1 | APPROVED by Bulldog; directly reconfirmed; Lane A activation explicitly withheld |
| Adoption record for v0.1 | PR #21 founder review and merge approval; subsequent direct founder confirmation |
| Effective date and time for v0.1 | 2026-10-09T20:43:03Z (policy only) |
| v0.1.1 correction approval | APPROVED — Bulldog's direct PR #23 review and comment, 2026-10-09T21:55:41Z / 2026-10-09T21:55:52Z |
| v0.1.1 adoption record | PR #23 founder review and comment; effectiveness is conditional on founder merge of the exact independently reviewed integrity-closure PR |
| Named ongoing independent verifier | BLOCKED — not yet named or qualified under ADR-0002 |
| Verifier independence record | BLOCKED — not yet supplied |
| Pre-launch firewall verification | BLOCKED — not yet performed/recorded |
| Authorized Lane A implementation/envelope | BLOCKED — not yet authorized |
| Audit and result-retention controls | BLOCKED — not yet independently verified |

Until every activation field is complete, neither the adopted policy nor this
correction grants standing Lane A authority. The controller design remains
design-only, and none of the reserved Lane B authorities in Section 1 is
authorized or automated.
