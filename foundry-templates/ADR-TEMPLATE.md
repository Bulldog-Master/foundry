# ADR NNNN: <short title>

- **Status:** Proposed | Accepted | Superseded | Rescinded
- **Type:** Doctrinal | Operational
- **Expires:** YYYY-MM-DD | Does not expire
- **Date:** YYYY-MM-DD
- **Author(s):**
- **Related ADRs:** (list ADR IDs this supersedes, extends, or depends on; or "None")

<!--
Type is either Doctrinal or Operational.

  - Doctrinal ADRs ratify durable commitments about how work is done. They are
    adopted on founder authority and do not require prior evidence, though they
    describe how evidence will be produced. Doctrinal ADRs normally have
    `Expires: Does not expire`.

  - Operational ADRs describe a decision that is expected to earn continued
    authority through evidence. Any temporary decision is an Operational ADR
    with an explicit `Expires` date, after which the decision must either be
    renewed on the strength of evidence, replaced, or allowed to lapse.

Supersession is a *relationship and a status* (`Superseded`, with `Related ADRs`
pointing to the superseding ADR), not a separate Type. A Doctrinal ADR that
replaces an earlier Doctrinal ADR is still Doctrinal; the earlier one becomes
Superseded.
-->

## Context

Describe the real situation that forced this decision. What problem appeared in real product or Foundry work? What made the existing approach insufficient? Avoid hypothetical framing — this is a record of a decision made against reality.

## Decision

State the decision in a single, unambiguous sentence, then expand as needed. A reader should be able to answer "what changed?" from this section alone.

If this ADR ratifies a **pre-commitment** (how work will be done, adopted on founder authority), say so. If it asserts an **operational claim** (that a mechanism, threshold, or process produces a particular outcome in the world), say so — operational claims must earn continued authority through evidence and are appropriate targets for Operational ADRs with an `Expires` date.

## Evidence

What evidence supports this decision at the moment of writing? Link to code, incidents, measurements, prior lessons, or user-observable outcomes. If the evidence is thin, say so honestly — an ADR may be accepted on limited evidence, but the limits must be visible.

For Doctrinal pre-commitments, the "evidence" is often the founder's ratification itself plus the reasoning; state that explicitly rather than manufacturing empirical support.

## Consequences

Describe the expected effects of this decision — what becomes easier, what becomes harder, what constraints this places on future work, and what future decisions this makes more likely.

## Rollback

Describe how this decision can be reversed if it proves wrong. If rollback is expensive or effectively impossible, say so — that is itself important information.

## Measurement or review trigger

State how and when this decision will be re-examined.

- For **Operational ADRs**, list the measurements, signals, or outcomes that would confirm or invalidate the decision, and the date or condition at which it will be reviewed. `Expires` names the outer bound; this section names how the intervening period is judged.
- For **Doctrinal ADRs**, list the conditions under which the doctrine would be reconsidered — for example, a class of failure the doctrine did not anticipate, or a change in operating reality that makes the doctrine inappropriate.

A decision with no measurement, no review trigger, and no expiry is a decision that cannot be corrected by evidence. If that is intentional, say so explicitly.

## Notes

Optional: open questions, follow-ups, references, or things a future reader will need to make sense of this decision.
