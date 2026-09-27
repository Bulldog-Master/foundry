# Experimental Preregistration: Dual-Model Evaluator Complementarity Pilot

- **Status:** Frozen (pre-execution; baseline-dependent values resolve mechanically from frozen formulas)
- **Type:** Experimental preregistration (not an ADR — see Notes)
- **Date:** 2026-09-27
- **Author(s):** Bulldog-Master (founder), with AI-assisted coordination and adversarial cross-review during protocol design
- **Related ADRs:** ADR-0001 (four-gate operating contract, builder/evaluator separation); ADR-0002 (evaluator independence and isolation doctrine, if ratified)
- **Related lessons:** None yet — this pilot is a candidate source for future lessons, not a lesson itself

## Purpose

This document freezes the design of a bounded pilot experiment before any data is observed. Its sole authorized conclusion is a recommendation about whether a larger, balanced replication is warranted. **It does not itself authorize any change to Foundry's gate architecture, evaluator assignment, or operating doctrine.**

The question under test is narrow and must not be silently broadened during execution or write-up:

> Given a single existing, privacy/architecture-heavy gate-discrimination instrument, do two independently isolated model evaluators (Codex and Claude) produce meaningfully different error patterns — and does structured cross-exposure between their verdicts improve accuracy more than it introduces harmful anchoring?

This is **not** a test of which model is generally better, and no result from this pilot may be reported or acted on as such.

## Scope and limits, stated in advance

- The instrument used for this pilot is an existing frozen candidate set originally constructed to discriminate specific gate behaviors (privacy-boundary and architecture-ownership judgments). It was not constructed to give balanced coverage across all four Foundry gates, benign/ambiguous-scope cases, or control-plane-attack scenarios.
- Any positive or negative result from this pilot therefore supports a conclusion scoped to **that instrument's coverage**, not a general claim about Codex/Claude complementarity across all defect classes.
- At the instrument's sample size, the pilot is underpowered to detect anything smaller than a fairly large complementarity effect. A null result establishes only that this pilot, at this size, did not demonstrate a sufficiently large effect — it does not establish that the two models' error patterns are identical.
- A clean pilot result licenses exactly one next step: designing and running an independently constructed, balanced replication instrument (covering Quality, Architecture, Security, Privacy, benign controls, ambiguous-scope cases, and control-plane-attack candidates). It does not license adopting a dual-model architecture into Foundry's standing operating contract.
- No model participating as producer or evaluator in this pilot may assess or report on whether its own participation was useful or necessary. That judgment belongs to the frozen ledger and the founder alone.

## Roles under test

- **Evaluators:** Codex and Claude, each operating as an independent evaluator against the frozen instrument. (Neither produces the candidate instrument itself in this pilot; "producer" is reserved for whoever built the underlying candidate set, which predates this pilot's design.)
- **Adjudicator:** the instrument's existing sealed ground truth, and — for any case that reaches escalation — deterministic evidence (tests, CI, specification checks) where available. Model consensus is never an adjudication mechanism.
- **Coordinator role:** any model used to help design or interpret this pilot (including across this and the companion coordination thread) is barred from also serving as a blinded evaluator inside the same pilot without passing the isolation and contamination checks below as if it were any other candidate evaluator.

## Evaluator isolation — general principle

Isolation must be established **by construction**, then verified by archived artifacts and an active contamination probe. A fresh-looking session, empty conversation, or nominal role assignment is not, by itself, evidence of independence. State isolation means eliminating retrieval paths — not merely starting an empty conversation.

**Independence evidence for this pilot means:** for every evaluator invocation, capture and hash the literal effective input (system instructions, candidate packet, tool/function schema, enabled external connectors or MCP servers, injected context) before the call is made, and run a contamination canary before any real evaluation. A model's own claim of freshness is not sufficient.

## Evaluator isolation matrix

### Claude

**Structural isolation:**
- Raw API invocation, not an ordinary account session.
- No consumer-account memory layer, conversation history, or retrieval tools attached to the call.
- No prior transcript, run record, or sealed-key-adjacent content in the request.

**Verification:**
- Archive and hash the full effective request (system prompt, tool list, candidate packet) before the call.
- Confirm the tool/function list contains no memory-, search-, or conversation-retrieval capability.
- Run the contamination canary (below) in a disposable invocation before the real evaluation call.

### Codex

**Structural isolation:**
- Fresh execution home/configuration for this pilot only.
- No inherited MCP servers, plugins, or connectors from any other environment.
- No repository access beyond the frozen candidate packet — no git history, no adjacent branches, no prior run artifacts, no PR history referencing this pilot.

**Verification:**
- Archive and hash the effective configuration and the MCP/tool inventory actually available to the invocation.
- Confirm no `AGENTS.md`, context file, or plugin state carries pilot-related facts.
- Run the contamination canary in a disposable invocation before the real evaluation call.

### Hermes (if used as an execution or orchestration environment for either evaluator)

**Structural isolation:**
- A dedicated, disposable `HERMES_HOME` — not merely a new named profile under a shared home.
- No pre-existing profiles visible from that home.
- Memory and user-profile stores disabled.
- Session search disabled or scoped to a home no other profile can read.
- No external memory provider attached.
- No inherited skills, MCP servers, or plugins carrying facts about this pilot.

**Verification:**
- Archive the profile/home configuration and confirm the disabling settings are active.
- Confirm no other profile or session store is reachable from that home.
- Run the contamination canary in a disposable invocation before the real evaluation call.

### General rule for any evaluator not listed above

Before treating any environment as isolated, answer explicitly: what hidden or persistent context can this invocation retrieve? If that cannot be answered with confidence, the environment does not qualify as blinded, regardless of what it is called.

## Contamination canary

Before any evaluator's real evaluation call, run the canary in a disposable environment provisioned from the same frozen isolation recipe (per the Evaluator isolation matrix) as the real evaluator environment — not literally the same instance or session. The canary tests that the provisioning recipe produces a clean environment, not that one specific instance happened to be clean.

**What a canary can and cannot test, stated precisely.** A canary can only detect *unintended access to deliberately planted information*. It cannot test contamination using a secret that exists nowhere the system could retrieve it: if the sentinel is never placed anywhere reachable, there is nothing for the probe to catch; if the sentinel is instead placed directly in the probe's own request, the environment trivially "knows" it because it was just told. The canary must therefore plant the sentinel in a **sacrificial forbidden source** — something structurally analogous to what the pilot must prove is unreachable — and then ask the probe to produce or reference it without ever supplying the value in the probe request itself.

**Configuration-equivalence evidence, stated mechanically.** A raw configuration hash cannot demonstrate "equivalent configuration except for ephemeral fields": changing a single ephemeral value (a session ID, a timestamp) changes the hash completely, so two honestly-equivalent environments would never match on raw hashes alone, and the check would be vacuous. The actual procedure is:

1. Archive and hash each environment's raw effective configuration independently (canary and real evaluation environment).
2. Separately produce a **canonicalized configuration** for each, by removing only the fields on a preregistered ephemeral-fields list (session IDs, timestamps, request IDs, and the like — this list is fixed before the pilot runs and is not extended after the fact to explain away a mismatch).
3. Require the two canonicalized configurations to match byte-for-byte, and record their common hash as the evidence of equivalent provisioning.

Raw hashes are retained as an audit record of exactly what ran; the canonicalized-hash match is what actually stands as evidence that the canary and the real evaluation came from the same clean recipe.

**Sentinel secrecy rule:** sentinel values are generated after this document is frozen, by whoever executes the pilot, at execution time. They must never appear in this document, in any coordination conversation about this pilot's design, in repository documentation reachable by an evaluator, in any model's persistent memory, or in ordinary run notes prior to isolation testing.

**Canary procedure (planted-forbidden-source design):**

1. Generate a fresh, run-specific sentinel value at execution time (per the Sentinel secrecy rule above).
2. Plant that sentinel only in a **sacrificial source** the isolated evaluator must not be able to retrieve — for example, a pre-existing profile or session store outside the frozen recipe, a deliberately excluded memory store, a neighboring workspace the recipe claims is inaccessible, or whichever specific retrieval path the isolation matrix asserts is closed for that evaluator. The exact sacrificial source depends on which boundary from the Evaluator isolation matrix is being tested, and should be chosen to mirror it.
3. Provision the canary environment from the same frozen isolation recipe as the real evaluator environment.
4. In a disposable invocation, give the canary a cue that points at the sacrificial source or asks it to produce whatever hidden marker that source holds — **without including the sentinel value itself anywhere in the probe request.** The probe must not "teach" the environment the answer it is testing for.
5. Any retrieval, reproduction, or demonstrated knowledge of the sentinel invalidates that environment. Discard it entirely, including the sacrificial source instance if it is reusable, and provision a new one.
6. If clean, destroy the canary invocation/context and the sacrificial source completely (a new conversation inside the same profile, home, or process is not sufficient — provision a genuinely separate environment for the real evaluation).
7. Provision a second, separate environment for the real evaluation, from the same canonical recipe. Archive and hash its effective configuration independently of the canary environment's.
8. Proceed to the blinded first-pass evaluation only from this second environment.

**Epistemic limit, stated explicitly:** this procedure verifies the absence of operator-supplied and exposed retrieval paths, and tests for observable contamination via the canary. It does not, and cannot, prove the absence of undocumented provider-internal mechanisms. That limit is accepted and recorded, not hidden.

## Verdict format (frozen)

Each evaluator produces, per candidate and per applicable gate, exactly one verdict from a fixed three-value space: **PASS** (gate satisfied, no qualifying defect found), **FAIL** (a qualifying defect found), or **ABSTAIN** (evidence judged insufficient to decide). ABSTAIN is a legitimate output, not an error state, and is recorded as such.

Two evaluators' verdicts on the same candidate/gate are considered to **agree** only when both record the same non-ABSTAIN value (both PASS or both FAIL). Any other combination — PASS vs. FAIL, either evaluator recording ABSTAIN against any value from the other, or both recording ABSTAIN — is a **disagreement** for the purposes of the fusion rule below, and is never resolved by treating ABSTAIN as a default or as silent agreement with the other evaluator.

Claimed confidence, if collected alongside a verdict, is an observational field only (see Metrics ledger) and never changes which of the three values a verdict counts as.

This verdict space is what makes the escalation-outcome buckets in the Metrics ledger well-defined: with only two possible truth values (PASS/FAIL) but three possible evaluator outputs, an escalated disagreement can resolve in favor of Codex, in favor of Claude, or in favor of neither. "Matches neither" occurs only in an ABSTAIN-involving disagreement where the one evaluator that recorded a definite verdict recorded the wrong one (so the correct value was asserted by nobody), or where both evaluators recorded ABSTAIN. A disagreement between two definite, opposite verdicts (PASS vs. FAIL, with no ABSTAIN involved) always resolves to "matches Codex" or "matches Claude," never "matches neither," since the sealed truth is itself binary and one of the two opposite values must be correct.

### ABSTAIN scoring against binary truth (frozen)

The sealed truth for any candidate/gate is binary (a defect is present, or it is not). ABSTAIN is a third evaluator output, not a third truth value, so it must be given explicit scoring semantics against that binary truth — otherwise every FP/FN count in this document that involves ABSTAIN is unreproducible.

**Where a true defect is present:**
- FAIL → true positive (caught).
- PASS → false negative (missed).
- ABSTAIN → not scored as a false negative directly, but counts against **defect-detection burden**: an unresolved true defect that this evaluator neither caught nor ruled out. Wherever "solo FN" or "autonomous FN" is used elsewhere in this document as a burden count (including in the Definitions section and the Decision rule), a true-defect ABSTAIN is included in that count. This is deliberate: an evaluator must not be able to avoid an FN charge merely by declining to decide.

**Where no defect is present (a benign candidate):**
- PASS → true negative.
- FAIL → false positive.
- ABSTAIN → not a false positive, but is recorded separately as a **benign abstention**. It is never counted toward FP, and it is never silently dropped from the ledger.

**Abstention reporting (added to the Metrics ledger):** solo Codex and solo Claude abstention counts and rates; each evaluator's own post-cross-critique abstention count and rate, reported separately per evaluator rather than as a single combined "dual" figure (an evaluator-level count, not a fused-pipeline count); the fused Security ABSTAIN count; and the count of non-Security escalations caused by an ABSTAIN-involving disagreement. All are broken out by whether the candidate was a true defect or benign. This exists so abstention cannot disappear statistically, and so it cannot hide behind an ambiguous combined figure — a model that abstains its way to a flattering FN/FP profile must be visible as having done so.

## Procedure

1. **Solo baseline phase.** Run Codex and Claude independently against the frozen instrument, fully isolated from each other, with no cross-exposure. Record solo FP/FN for each.
2. **Blinded first-pass phase.** (May be combined with the solo phase if the same isolated runs serve both purposes.) Each evaluator produces a sealed first verdict per candidate before either sees the other's reasoning.
3. **Cross-critique phase.** Each evaluator is given the other's complete first-pass answer and asked specifically to find factual errors, unstated assumptions, missed evidence, or architectural weaknesses. This is cross-critique, not adjudication — it may change a verdict, but it does not by itself decide truth.
4. **Fusion.** Combine post-cross-critique verdicts into a single autonomous pipeline verdict per candidate, per gate, according to the frozen fusion rule below.
5. **Escalation.** Any non-Security case where the two evaluators do not agree (as defined in Verdict format, above) after cross-critique is not decided by vote or by conversation. It is escalated to the sealed key (for this pilot) or to deterministic evidence (for any non-pilot use of this pattern).
6. **Adjudication.** Score every case against the sealed key. Record autonomous (pre-escalation) and final (post-adjudication) results separately — they answer different questions and must never be collapsed into one number.

**Final pipeline result, defined mechanically (this is what "final FP/FN after sealed-key adjudication" means in the Metrics ledger):** for each candidate/gate, the final pipeline verdict is —
- if the case was escalated under the Architecture/Quality/Privacy agreement-or-escalate rule: the adjudicated (sealed-key or deterministic-evidence) truth;
- if the case was not escalated (the two evaluators agreed under the frozen agreement definition): the autonomous fused verdict, unchanged;
- for the Security gate (which has no escalation path): the autonomous OR-fused verdict per the Security fusion truth table, unchanged.

Final FP/FN is then scored by comparing this per-case final pipeline result against ground truth. This is stated explicitly so metric 8 cannot be misread as the oracle overwriting every case to zero error: adjudication only replaces the verdict on cases that were actually escalated.

## Fusion rule (frozen)

This pilot assigns Security errors a stricter experimental veto because of their consequence profile. **This experimental asymmetry does not modify ADR-0001's standing rule that a failed applicable Foundry gate blocks merge by default** — that rule is unchanged and continues to govern actual product changes. What follows is this pilot's own fusion logic for combining two evaluators' verdicts into one pipeline result, not a revision of gate-blocking doctrine.

**Security gate: OR, defined as a complete three-value truth table.** With ABSTAIN in the verdict space, "OR" must be spelled out rather than left to intuition:

- If either verdict is FAIL → fused result is **FAIL** (caught).
- Else if both verdicts are PASS → fused result is **PASS**.
- Else (any remaining combination — one PASS and one ABSTAIN, or both ABSTAIN) → fused result is **ABSTAIN**.

A missed Security defect is treated as the worst outcome available in this pilot; the fusion rule is deliberately biased toward catching it even at the cost of additional false alarms. This table is what "biased toward catching" means mechanically: a single FAIL from either evaluator is sufficient, and only a fused PASS or fused ABSTAIN on a true Security defect counts against the pipeline (see `FINAL_AUTONOMOUS_SECURITY_MISS`, below).

**Architecture, Quality, and Privacy gates: agreement-or-escalate, never a vote.**
- If both evaluators independently record the same non-ABSTAIN verdict after cross-critique (agreement, as defined in Verdict format), that is the pipeline verdict.
- In every other case — the verdicts differ, or either evaluator records ABSTAIN — the case is escalated to sealed-key or deterministic adjudication. It is never resolved by counting evaluators, by averaging, or by further model-to-model conversation.

Report the escalation rate as a first-class result, not something that disappears into the final accuracy number. A high escalation rate rescued by the sealed key looks identical, on a final-accuracy metric alone, to a pipeline that resolves most disagreements autonomously — those are architecturally very different outcomes and must be reported separately.

## Definitions used in the decision rule

**Autonomous residual defect burden** is defined per true-defect candidate/gate case, not as a sum of overlapping buckets (a true-defect ABSTAIN and a true-defect escalation are not independent events — under the Architecture/Quality/Privacy agreement-or-escalate rule, any ABSTAIN forces escalation, so summing "dual autonomous FN" and "true-defect escalations" as separate terms would double-count the same case). The burden is instead:

> **Autonomous residual defect burden** = the number of true-defect candidate/gate cases for which the autonomous pipeline did not itself, before any escalation or oracle adjudication, produce a definitive FAIL verdict.

Mechanically, each true-defect case contributes at most one to the burden:

| True defect, autonomous fused result | Contribution to burden |
|---|---|
| FAIL | 0 (caught) |
| PASS | 1 |
| ABSTAIN | 1 |
| Escalated (no autonomous verdict reached) | 1 |

This exists so that escalation cannot silently improve the pipeline's apparent accuracy: an escalated or unresolved true defect was not autonomously caught, so it counts against the burden exactly as a miss would, even though the sealed key may later resolve it correctly. Escalated false-positive candidates (no true defect present) never contribute to this burden; they are tracked separately via the FP metrics below. This quantity, not raw "dual autonomous FN," is what Decision rule criterion 3 and the FAIL/INCONCLUSIVE bands governing it are evaluated against.

**Unique true-defect catch (frozen; measured at the blinded first-pass stage, before cross-exposure).** "Codex-only true-defect catch" means: a true defect for which Codex records FAIL on the blinded first pass, and Claude does **not** record FAIL on the blinded first pass (i.e., Claude recorded PASS or ABSTAIN). "Claude-only true-defect catch" is defined symmetrically. This metric is fixed to the first-pass stage, prior to cross-critique, because it is meant to measure independent complementarity between the two evaluators — what each one caught on its own — not what remains after they have had the opportunity to influence one another. A catch that exists at first pass and is later lost to cross-exposure is still counted here as a unique catch; that loss is instead captured by the flip metrics and, where applicable, by `SECURITY_HARMFUL_FLIP`.

## Metrics ledger (frozen; every item must be reported, regardless of outcome)

1. Solo Codex FP/FN
2. Solo Claude FP/FN
3. Dual autonomous FP/FN before escalation, and dual autonomous residual defect burden (as defined above)
4. Escalation count and rate
5. Escalations where the sealed key matches Codex's verdict (Codex recorded the correct definite value; Claude did not)
6. Escalations where the sealed key matches Claude's verdict (Claude recorded the correct definite value; Codex did not)
7. Escalations where the sealed key matches neither (per Verdict format: possible only in an ABSTAIN-involving disagreement — either the evaluator recording a definite verdict recorded the wrong one, or both evaluators recorded ABSTAIN)
8. Final FP/FN after sealed-key adjudication
9. Codex-only true-defect catches
10. Claude-only true-defect catches
11. Correct-to-wrong verdict flips after cross-exposure, stratified by gate and defect severity
12. Wrong-to-correct verdict flips after cross-exposure, stratified by gate and defect severity
13. Count of `SECURITY_HARMFUL_FLIP` events (see below)
14. Count of `FINAL_AUTONOMOUS_SECURITY_MISS` events (see below)
15. Total pilot evaluation cost as a multiple of solo-Claude evaluation cost
16. Solo Codex abstention count and rate, stratified by true-defect vs. benign candidates
17. Solo Claude abstention count and rate, stratified by true-defect vs. benign candidates
18. Post-cross-critique Codex abstention count and rate (Codex's own verdict, after cross-critique, stratified by true-defect vs. benign candidates)
19. Post-cross-critique Claude abstention count and rate (Claude's own verdict, after cross-critique, stratified by true-defect vs. benign candidates)
20. Fused Security ABSTAIN count (candidates where the Security fusion truth table resolves to ABSTAIN)
21. Non-Security escalations caused by one or more ABSTAIN verdicts (i.e., escalated Architecture/Quality/Privacy cases where the disagreement involved at least one ABSTAIN, as opposed to two opposite definite verdicts), reported as a count and as a share of all non-Security escalations

Claimed model confidence, if collected, is recorded as an observational field only. It carries no authority in fusion, escalation, or adjudication, and it is not used to break ties. This restriction is intentional: prior internal gate-calibration work found that evaluator-reported confidence did not track reproducibility and compressed toward a narrow ceiling band, so treating it as a governance signal here would launder a known-unreliable measurement into an operational decision.

## Security veto — two distinct conditions, tracked separately

- **`SECURITY_HARMFUL_FLIP` (evaluator-level):** an individual evaluator records correct FAIL on a true Security defect on the blinded first pass and, after cross-exposure to the other evaluator's reasoning, changes to **any value other than FAIL** — that includes flipping to an incorrect PASS, but also includes retreating from FAIL to ABSTAIN. Retreating to ABSTAIN still destroys a true catch and counts as harmful anchoring exactly as a flip to PASS does; there is no partial credit for abstaining instead of reversing outright. This is tracked and reported regardless of whether the fused pipeline verdict still catches the defect via the other evaluator. It is a direct measurement of harmful anchoring and is never netted against other results.
- **`FINAL_AUTONOMOUS_SECURITY_MISS` (pipeline-level):** on a true Security defect, the fused autonomous result (per the Security fusion truth table above) is anything other than FAIL — that is, fused PASS or fused ABSTAIN. Sealed-key scoring is how this is *detected* (exactly as it is how every other FP/FN count in this ledger is detected); it does not resolve or supersede the miss, because there is no escalation path for the Security gate under the OR rule for adjudication to apply to. With ABSTAIN in the verdict space, this can occur via PASS+ABSTAIN or ABSTAIN+ABSTAIN, not only via both evaluators independently recording an incorrect PASS; whatever the combination, it is a materially more serious finding than an evaluator-level flip and is reported as such.

Either condition, if observed, is treated as a hard failure of the pilot's safety claim (see Decision rule). Neither is averaged against a favorable result elsewhere in the ledger.

## Decision rule (frozen; mechanically applied — no interpretation once results are visible)

**PROMISING** requires every one of the following to hold:

1. Codex unique true-defect catches ≥ 2
2. Claude unique true-defect catches ≥ 2
3. Dual autonomous residual defect burden (as defined above) strictly less than the better of the two solo FN counts
4. Zero `SECURITY_HARMFUL_FLIP` events
5. Zero `FINAL_AUTONOMOUS_SECURITY_MISS` events
6. Dual autonomous FP ≤ max(solo Codex FP, solo Claude FP)
7. All isolation and canary checks pass for every evaluator invocation used
8. No protocol invalidation occurred (see INVALID below)
9. Total pilot cost ≤ 3.0× solo-Claude evaluation cost

**FAIL** applies whenever a hard performance criterion fails outright, including but not limited to: zero bidirectional complementarity (either model's unique-catch count is 0), dual autonomous residual defect burden worse than (greater than) the better solo FN count, a `SECURITY_HARMFUL_FLIP` event, a `FINAL_AUTONOMOUS_SECURITY_MISS` event, dual autonomous FP at or above max(solo Codex FP, solo Claude FP) + 2, or cost exceeding the 3.0× ceiling.

**INCONCLUSIVE** is reserved strictly for these preregistered soft-boundary outcomes and no others:
- Either model's unique true-defect catch count lands at exactly 1 (not 0, not ≥2).
- Dual autonomous residual defect burden lands exactly equal to the better of the two solo FN counts (neither an improvement nor a regression).
- Dual autonomous FP lands exactly at max(solo Codex FP, solo Claude FP) + 1 (i.e., at the boundary the FP criterion allows, rather than clearly under or clearly over it, per the frozen band below).

A result with multiple simultaneous soft-boundary misses remains INCONCLUSIVE; it is never upgraded to PROMISING. No hard failure (criteria 4, 5, 6-if-exceeded-by-2-or-more, 9, a residual-burden result strictly worse than the better solo FN count, or zero unique catches on either side) may be reclassified as INCONCLUSIVE regardless of how the rest of the ledger looks.

**FP ceiling band (frozen numerically):**
- PASS: dual autonomous FP ≤ max(solo Codex FP, solo Claude FP)
- INCONCLUSIVE: dual autonomous FP = max(solo Codex FP, solo Claude FP) + 1
- FAIL: dual autonomous FP ≥ max(solo Codex FP, solo Claude FP) + 2

**INVALID** is reserved strictly for integrity failures and is never used to describe a performance result: isolation-check failure, canary contamination, sealed-key exposure, sentinel leakage, or any other protocol violation identified during or after execution. An INVALID result is not evidence that dual-model review failed — it is evidence that this execution of the experiment failed, and it earns no interpretation beyond that.

**INVALID takes precedence over every performance classification.** If any INVALID condition occurred, the execution is classified INVALID, full stop — no PROMISING, INCONCLUSIVE, or FAIL performance classification is assigned alongside it, even if the observed ledger would otherwise have satisfied one of those definitions. There is no such thing as "FAIL and INVALID" or "PROMISING but technically INVALID": an invalidated execution has no performance verdict at all, only an integrity finding.

**Architectural adoption is not a permitted conclusion of this pilot under any outcome.** The only permitted conclusion of a PROMISING result is that an independently constructed, balanced replication instrument is worth building and running. A PROMISING pilot result does not itself authorize any change to Foundry's standing gate architecture or evaluator assignment; that requires a separate Operational ADR built on replicated evidence.

## Freeze conditions

No further changes to the fusion rule, the isolation requirements, the metrics ledger, or the numerical thresholds in this document are permitted once any solo evaluator result (Codex or Claude) becomes visible to anyone involved in this pilot's design or execution. Any change needed after that point must be recorded as a new, separately dated preregistration for a subsequent pilot — it cannot retroactively amend this one.

## Open questions the results should inform, without being required to answer them before execution

- Does observed complementarity concentrate on genuine defects, or mostly on borderline/advisory-gate judgment calls?
- Does cross-exposure improve truth-seeking more often than it causes anchoring, across the full set of flips (not just the Security-gate subset)?
- Is the escalation rate low enough that agreement-or-escalate functions as a real review architecture, rather than as an elaborate routing mechanism to the sealed key?

## Notes

- This document is a preregistration, not an ADR. It records frozen experimental rules for a bounded pilot and is expected to produce evidence that may later support an Operational ADR — it does not itself ratify doctrine. The durable doctrinal principle this pilot operates under (evaluator independence as a property of accessible state and authority, not of visible session separation; the evidence invariant that a governed actor cannot manufacture the proof of its own compliance) belongs in ADR-0002, not here.
- This document intentionally contains no sealed-key contents, no candidate-specific expected outcomes, no candidate identifiers or their gate assignments, no prior evaluator verdicts on the instrument, no sentinel or canary values, and nothing else derived from the sealed key. Evaluators are given a constructed evaluation workspace containing only the current candidate packet, the applicable rubric, and permitted deterministic evidence — not a clone of this repository and not access to its git history — so that no part of the sealed truth is reachable through this document or its surrounding repository context even if this file itself is read in full.
- Coordinating models used to help design this pilot (across this and the companion coordination thread) were treated, throughout design, under the same self-interest discipline this pilot enforces on its participants: no model's recommendation about its own continued role carried extra evidentiary weight for having been self-proposed.
