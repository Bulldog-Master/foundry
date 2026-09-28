<!--
Every pull request into this repository must complete this template.
Sections may not be deleted. If a section does not apply, say so explicitly.
Under Foundry 1, the four gate records and the failed-gate disposition are mandatory.
-->

## Purpose

What is this pull request trying to change, and why now? One or two sentences.

## Declared scope

List exactly the files and directories this PR is authorized to change. Anything outside this list is out of scope for this PR.

## Evidence

What real work, observation, incident, measurement, or prior artifact supports this change? Link ADRs, lessons, issues, or code. If evidence is thin, say so honestly.

## Constitutional Principle

Which Foundry constitutional principle(s) does this change rest on, and is any principle placed under tension by it? Reference `CONSTITUTION.md` by principle name.

## Expected Improvement

What is expected to be better after this change lands? Describe the observable improvement, not the activity.

## Rollback

How is this change reversed if it turns out to be wrong? If rollback is expensive or effectively impossible, say so.

## Foundry impact classification

Check all that apply:

- [ ] Doctrinal — changes or establishes constitutional / durable commitments
- [ ] Operational — changes how work is currently done, without changing doctrine
- [ ] Lesson — records or promotes a lesson
- [ ] Charter — creates or amends a product charter
- [ ] Editorial — wording, formatting, or non-substantive fixes only

---

## Repository authorization boundaries

Broad or general instructions such as "proceed" do not expand a previously bounded scope. Commit, push, pull-request creation or update, and merge are separate authorization boundaries; each requires fresh explicit authorization before that boundary is crossed.

---

## Gate records

Each gate must record one outcome: **Pass**, **Fail**, **Pass with conditions**, or **N/A with a specific reason**. The evaluator must be an **independent source** under ADR-0002. Independence depends on accessible state and authority, not a separate session or role label alone. **Naming the same person under two role labels on the same change does not satisfy independence.** The founder remains the final approval authority; founder approval does not by itself substitute for independent gate evaluation when the founder produced the change.

Record the following for every evaluator arrangement, distinguishing between gates where necessary:

- **Evaluator identity and role:**
- **Independence basis:**
- **Recorded/checkable independence evidence appropriate to this arrangement:**
- **Prior exposure:** If blinded evaluation is claimed, confirm that the evaluator had no exposure to deliberately withheld information that would disqualify it for this execution.
- **Authorized evaluation context:** Describe the bounded context supplied and justify any broader access required by the gate.
- **Known limitations of the independence evidence:**

No single mechanism is universally required. A different human reviewer may rely on organizational and access-separation evidence; a model evaluator may require environment and effective-configuration evidence; a deterministic check may have a mechanical evidence basis. Do not claim that hashes, canaries, fresh sessions, or any other one technique proves independence beyond the boundary it actually tests.

### 1. Architecture Gate

- **Outcome:**
- **Evaluator (role and identity):**
- **Findings:**
- **Evidence (links, measurements, reasoning):**
- **Conditions (if Pass with conditions):**
- **Possible misses (what this gate is unlikely to have caught here):**
- **Value added by this gate on this PR:**

### 2. Security and Cryptography Gate

- **Outcome:**
- **Evaluator (role and identity):**
- **Findings:**
- **Evidence:**
- **Conditions:**
- **Possible misses:**
- **Value added:**

### 3. Privacy and Metadata Gate

- **Outcome:**
- **Evaluator (role and identity):**
- **Findings:**
- **Evidence:**
- **Conditions:**
- **Possible misses:**
- **Value added:**
- **Engineering-to-product identity leakage check:** Does this PR risk leaking engineering-side identifiers (author, tooling, environment, model, build metadata) into product-side artifacts, telemetry, or user-visible surfaces? State explicitly, with reasoning.

### 4. Quality and Verification Gate

- **Outcome:**
- **Evaluator (role and identity):**
- **Findings:**
- **Evidence:**
- **Conditions:**
- **Possible misses:**
- **Value added:**

---

## Failed-gate disposition

**A failed gate blocks merge by default.** If any gate above records Fail, one of the following must be true before merge:

- [ ] No gate above records Fail (this section is otherwise not required).
- [ ] An explicit, recorded founder override is documented below. An override does **not** convert a failure into a pass.

If a founder override is being invoked:

- **Failed gate(s):**
- **Accepted risk:**
- **Rationale for proceeding despite failure:**
- **Follow-up (action, owner, target date):**
- **Reassessment condition (what would cause this override to be revisited):**
- **Founder acknowledgement:** I acknowledge that the gate result remains Fail on the record and that this override is a decision to accept risk, not a re-evaluation of the change.

## Gate-value review

Briefly: on this PR, did each gate earn its keep? Note any gate that fired without catching anything, any gate that caught something the others would have missed, and any candidate recalibration for a future ADR.

## Human approval checklist

- [ ] No files outside the declared scope of this PR.
- [ ] AI-generated content received human review.
- [ ] Each gate record names an independent evaluating source (not the same person under a second role label).
- [ ] No doctrine change, lesson promotion, security exception, or failed-gate override occurred without explicit founder approval.
- [ ] A human founder has approved this PR for merge.
