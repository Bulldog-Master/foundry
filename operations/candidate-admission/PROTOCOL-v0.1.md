# Candidate Admission Protocol v0.1

- Type: Operational protocol
- Status: DRAFT — unapproved, untested; no standing authority
- Scope: First bounded trial: deterministic-rule promotion
- Owner and final decision authority: Bulldog
- Review trigger: After the first trial, before expansion, or on an integrity failure

## Purpose and limits

Provide a small, repeatable route from a proposed component to a reviewable
admission decision. Adoption of this protocol is a pre-commitment to a trial;
it does not establish that the process or a candidate works.

This protocol is subordinate to the [Constitution](../../CONSTITUTION.md),
[ADR-0001](../../adrs/ADR-0001-model-neutral-foundry-boundaries.md),
[ADR-0002](../../adrs/ADR-0002-evaluator-independence-and-isolation.md), and
applicable frozen contracts, baselines and experiment rules. It does not change
the evaluator protocol, automate the four gates, or grant signing, secrets,
merge, production, adjudication or sealed-truth authority. Run-009 remains
INVALID and cannot support admission claims. Deferred work stays deferred.

## 1. Intake: one candidate record

Record an ID/revision, proposer, operational problem, intended use and explicit
non-goals; exact component/source revision and artifact hashes; configuration,
dependencies, runtime and environment; requested capabilities and data/state
access; intended integration target; rollback/disable path and owner.

Search current repository records, relevant PR discussions and pending work
for completed, frozen, rejected or deferred decisions. Cite the results and
state whether the proposal is new, duplicates an existing mechanism, or requires
explicit reopening. A conflict or missing reopening blocks evaluation readiness.

## 2. Evidence and plan: freeze before evaluation

The record must contain or reference:

- The concrete source observation, current baseline and expected improvement.
- Exact candidate artifacts and a bounded test corpus with independently
  justified expected behavior, including positive, negative and boundary cases.
- Commands, comparison method, predeclared acceptance criteria, resource/time
  limits, stop conditions, permitted outputs and retention location.
- Risks, failure modes, false acceptance/rejection costs, limitations and exit cost.
- Named producer, evaluation operator, independent reviewer and evidence custodian;
  their accessible state, authority and prior exposure, with checkable evidence.

Bulldog authorizes the exact evaluation packet and bounded execution scope
before the trial. The custodian freezes its manifest and preserves all attempts,
including failures, timeouts and aborted runs. The producer may supply draft
artifacts but must not retain post-freeze control to replace, select or suppress
authoritative evaluation evidence. Hashes detect changes; they do not establish
custody or isolation. If custody/independence cannot be established, defer.

## 3. Bounded evaluation

Run only the frozen plan in its authorized non-production environment. The
first trial uses inert synthetic fixtures; no production hosts, provider calls,
credentials, signing or sealed evaluation material are involved. Do not treat
this protocol as authorization to replicate the dual-model pilot.

Compare the candidate with the declared baseline. Capture commands, effective
configuration, input/output hashes, exit status, measurements and every attempt.
Stop on unauthorized access, scope expansion, packet/environment drift,
contamination, missing evidence, or exhausted limits. An integrity failure makes
the attempt INVALID; retain it as diagnostic evidence only. A changed candidate,
plan or environment requires a new revision and fresh authorization, never an
in-place repair of the scored record. Model agreement is not ground truth.

## 4. Independent review

The producer cannot be the sole evaluator. Apply ADR-0002 Decisions 1–5:
record reviewer identity, accessible state and authority, checkable independence
evidence, prior exposure, justified bounded context and evidence limitations.
Fresh sessions or different role labels alone are insufficient. Do not claim
blinding when relevant withheld information was previously exposed.

Record the four existing gates: Architecture, Security and Cryptography,
Privacy and Metadata, and Quality and Verification. For each, retain outcome
(Pass, Fail, Pass with conditions, or N/A with a specific reason), findings,
evidence, conditions, possible misses and value added; include the identity
leakage check. Review criteria and evidence provenance as well as test results.
All review conditions must be resolved and verified before an admission approval.
A failed gate blocks by default. Any founder override remains a separately
recorded risk acceptance under existing rules and does not turn Fail into Pass.

## 5. Decision and version binding

Bulldog records one disposition with date, rationale and evidence references:

| Disposition | Meaning and follow-up |
| --- | --- |
| Approve for specified integration proposal | Evidence and independent review support only the named use of the exact tested tuple; integration is still separately gated. |
| Reject | Valid evidence fails the criteria or use is unacceptable; retain reasons and prohibit treating this revision as admitted. |
| Defer | Evidence, readiness, authorization or independence is insufficient; record missing items, owner and explicit reopening trigger. |

INVALID describes an evaluation attempt, not candidate performance; its admission
disposition is Defer until a separately authorized valid attempt exists. Reject
and Defer records stay in the durable history. Resubmission links the prior
record, states what changed, and does not erase failures or override deferred work.

An approval names protocol version/hash, candidate ID/revision and source/artifact
hashes, effective configuration, dependency/runtime versions, environment,
evaluation-plan/corpus/result hashes, independent review, intended use/target,
limits, and expiry or reassessment trigger. No approval transfers to a changed
tuple. Missing bindings mean no approval; changes require recorded reassessment
and fresh Bulldog approval before use. A generic instruction to proceed does
not widen any bounded authorization.

## 6. Exact stop before integration

Admission ends at a preserved decision packet and a proposed integration scope.
STOP before installing, enabling, wiring into a workflow, changing permissions
or baselines, granting authority, or relying on the candidate as a standing gate.
Approval to evaluate or an admission disposition alone does not authorize these
actions. The next integration action needs explicit Bulldog approval bound to
the exact target, diff/artifacts, capabilities, rollback and tested tuple, plus
applicable independent gates. Commit, push, PR creation/update and merge remain
separate explicit boundaries under the existing repository requirements.

Reconcile trial findings before expanding this protocol to other candidate types.
Record any actual decision in the program-state record only after it exists;
drafting this protocol does not change program status.
