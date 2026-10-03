# Dual-Model Pilot Protocol-to-Enforcement Matrix

## Status

Draft audit artifact. No replication is authorized by this document.

## Purpose

Map every binding requirement of the frozen dual-model pilot and governing
evaluator-independence doctrine to an explicit enforcement mechanism,
deterministic human checkpoint, or explicitly accepted unenforceable assumption.

A requirement with no mapped control is a protocol defect.

## Authoritative sources

- `experiments/dual-model-pilot-preregistration.md`
- `adrs/ADR-0002-evaluator-independence-and-isolation.md`
- `VERSION.md`
- `experiments/run009-integrity-record.md`

## Classification

Each requirement must be classified as exactly one of:

- `AUTOMATED` — mechanically checked and fail-closed.
- `HUMAN` — deterministic human authorization/checkpoint with recorded evidence.
- `ASSUMPTION` — cannot presently be mechanically guaranteed; limitation must be explicit.
- `GAP` — required but not yet enforced. Replication blocked.

## Rule

Any unresolved `GAP` blocks replication.

## Freeze boundary and sealed-truth custody

| Requirement | Source | Control type | Required enforcement | Evidence artifact | Current status |
|---|---|---|---|---|---|
| Frozen protocol must not change after any solo evaluator result becomes visible. | dual-model pilot preregistration: Freeze conditions | AUTOMATED + HUMAN | Record a protocol hash before execution. Preflight stores the hash. Every scored phase re-checks it. Any mismatch aborts. Any proposed post-freeze change requires a new separately dated preregistration and founder authorization. | `protocol-manifest.txt`, preregistration SHA-256, founder checkpoint record | UNIMPLEMENTED |
| Evaluator identities are part of the frozen pilot definition and may not be silently substituted. | dual-model pilot preregistration: Roles under test; Freeze conditions | AUTOMATED + HUMAN | Preflight records exact evaluator identities/model IDs. Scored runner refuses an evaluator not listed in the frozen manifest. Substitution requires a new preregistration. | evaluator manifest + runtime manifest | UNIMPLEMENTED |
| The sealed truth must exist before scored evaluation begins. | dual-model pilot preregistration: Adjudicator / Procedure; Run-009 integrity record | AUTOMATED | Preflight requires an authoritative sealed-truth artifact and fails closed if absent. | sealed-truth path + hash in preflight manifest | UNIMPLEMENTED |
| The sealed truth must have one authoritative immutable identifier and hash. | ADR-0002 Decision 2; Run-009 integrity record | AUTOMATED | Record exact canonical path, immutable artifact ID where available, byte length, and SHA-256 before evaluator execution. | sealed-truth manifest | UNIMPLEMENTED |
| The sealed truth must have at least one independent recovery copy. | Run-009 integrity record | AUTOMATED + HUMAN | Create recovery copy in a separate storage location before execution. Record path/location and hash. Founder confirms custody separation. | primary + recovery manifests | UNIMPLEMENTED |
| Recovery must be tested before any scored evaluator runs. | Run-009 integrity record | AUTOMATED | Restore/copy the recovery artifact into a temporary location, hash it, and require byte-identical match with the authoritative sealed truth. Failure aborts. | recovery-test log + hashes | UNIMPLEMENTED |
| Chain-of-custody must identify who can read, write, replace, suppress, or delete the sealed truth after freeze. | ADR-0002 Decision 2; Run-009 integrity record | HUMAN + AUTOMATED | Record filesystem/account permissions and responsible actors at freeze time. Scored evaluators receive no write path and no retrieval path to the sealed truth. | custody record + permission snapshot | UNIMPLEMENTED |
| An evaluator being scored must not retain authority to modify, replace, select, or suppress the sealed truth or authoritative evidence after freeze. | ADR-0002 Decision 2 | AUTOMATED + HUMAN | Structural separation of truth store from evaluator workspaces. Permission check must show evaluator identity has no write access. Founder verifies evidence authority. | access-control snapshot + human checkpoint | UNIMPLEMENTED |
| Sealed truth must not be reachable from evaluator packets, repository history, tools, memory, connectors, or adjacent workspaces. | ADR-0002 Decisions 1, 3, 5; preregistration isolation rules | AUTOMATED | Preflight enumerates permitted inputs/tools and verifies no sealed-truth path, file, connector, memory provider, git history, or adjacent workspace is exposed. Canary tests the claimed boundary. | effective-input archive + tool inventory + canary record | UNIMPLEMENTED |
| Truth-dependent scoring must use the recovered artifact whose hash matches the frozen expected hash. | Run-009 integrity record | AUTOMATED | Scoring program accepts truth only when SHA-256 equals frozen expected hash; otherwise scoring aborts. | scorer verification log | UNIMPLEMENTED |
| Existing invalid Run-009 outputs remain quarantined and cannot be used as confirmatory evidence in the replication. | Run-009 integrity record | HUMAN + AUTOMATED | New replication uses a separate evidence root and preregistration. Preflight rejects Run-009 result directories as truth, baseline labels, or confirmatory inputs. | replication manifest + founder checkpoint | UNIMPLEMENTED |

## Runtime, output schema, and retry integrity

| Requirement | Source | Control type | Required enforcement | Evidence artifact | Current status |
|---|---|---|---|---|---|
| Scored execution must use one frozen runtime configuration. | dual-model pilot preregistration: configuration-equivalence procedure; Run-009 integrity record | AUTOMATED | Before scoring, record model ID, model artifact/blob hash where applicable, inference runtime version, driver version, CUDA version, context length, temperature, top-p, effective environment variables, runner hash, and effective tool configuration. Every scored invocation re-checks the frozen manifest before launch. Any non-preregistered change aborts the execution. | runtime manifest + per-invocation verification log | UNIMPLEMENTED |
| Raw effective configuration must be archived for each evaluator invocation. | dual-model pilot preregistration: independence evidence / configuration-equivalence | AUTOMATED | Serialize and hash the literal effective configuration and permitted tool inventory before every scored call. | raw-config archive + SHA-256 manifest | UNIMPLEMENTED |
| Canonicalization may remove only preregistered ephemeral fields. | dual-model pilot preregistration: configuration-equivalence evidence | AUTOMATED | Maintain a frozen explicit list of removable ephemeral fields. Canonicalizer refuses unknown exclusions. Canary and real evaluator canonical configurations must match byte-for-byte. | canonicalization specification + common canonical hash | UNIMPLEMENTED |
| A runtime change during scored execution automatically invalidates the execution unless the preregistration already defines that change as equivalent. | Freeze conditions; Run-009 integrity record | AUTOMATED | Runner checks the frozen runtime manifest before and after each invocation. Any mismatch sets execution status to INVALID and prevents additional scored work. | invalidation record + runtime diff | UNIMPLEMENTED |
| Evaluator output must contain exactly one verdict for each required gate from PASS, FAIL, or ABSTAIN. | dual-model pilot preregistration: Verdict format | AUTOMATED | Evaluator response must satisfy a strict machine-readable schema. Missing, duplicate, unknown, or malformed gate verdicts fail validation immediately. | JSON/schema validator log + frozen response | UNIMPLEMENTED |
| Free-form prose must never be used to infer a missing authoritative verdict. | dual-model pilot preregistration: Verdict format; Run-009 integrity record | AUTOMATED | Scorer reads only schema-validated verdict fields. Prose/reasoning is archived but cannot supply or repair a verdict. | parser/scorer implementation hash + validation log | UNIMPLEMENTED |
| Zero-verdict and malformed-output behavior must be preregistered before execution. | frozen retry semantics / Run-009 integrity record | HUMAN + AUTOMATED | New preregistration must define whether zero-verdict or malformed responses may be retried, how many times, and under what freshness conditions. Runner implements only that frozen rule; no retrospective exception is permitted. | retry-policy section + runner tests | UNIMPLEMENTED |
| Any attempt producing an authoritative gate verdict cannot be silently discarded or rerun unless the frozen protocol explicitly permits it. | preregistered retry/freeze principles | AUTOMATED | Runner detects whether any valid gate verdict was emitted and records the attempt as authoritative according to the frozen retry policy. | attempt ledger + validator result | UNIMPLEMENTED |
| Failed attempts must be preserved rather than overwritten. | evidence invariant; Run-009 operational lessons | AUTOMATED | Every invocation receives a unique immutable attempt directory containing raw request, raw response, stderr/logs where available, config hash, timestamps, and failure status. | attempt manifest + file hashes | UNIMPLEMENTED |
| Resume after crash/reboot must not change the frozen execution state. | Freeze conditions; Run-009 runtime failures | AUTOMATED | Resume logic reads the frozen execution manifest, verifies all prior artifacts and hashes, verifies runtime identity, and continues only from the first legally incomplete unit. Otherwise it aborts. | resume verification log | UNIMPLEMENTED |
| Completed scored candidates must never be rerun merely because later infrastructure fails. | evidence invariant / retry integrity | AUTOMATED | Completion ledger is append-only and hash-checked. Resume skips valid completed units and refuses overwrite. | completion ledger + manifest hash | UNIMPLEMENTED |
| Scoring code must fail closed on missing candidate, gate, verdict, truth row, manifest entry, or hash mismatch. | reproducibility requirements; Run-009 integrity record | AUTOMATED | Scorer validates cardinality and identifiers before computing any metric. Any missing or extra item aborts scoring. | scorer preflight report | UNIMPLEMENTED |
| Truth reveal and scoring occur only after both evaluator ledgers are frozen. | dual-model pilot procedure: blinded first pass, cross-critique, fusion, adjudication | AUTOMATED + HUMAN | Pre-scoring checkpoint requires frozen hashes for both evaluator ledgers and all post-cross-critique outputs before sealed truth is opened to the scoring process. | ledger manifest + founder checkpoint | UNIMPLEMENTED |
| Synthetic non-scored end-to-end tests must pass before real candidates are authorized. | Run-009 integrity record | AUTOMATED + HUMAN | Run the complete harness using synthetic candidates, synthetic truth, forced malformed output, forced crash, forced runtime mismatch, and restore tests. Real-run authorization is blocked unless all expected pass/fail behaviors are observed. | synthetic preflight report + founder authorization | UNIMPLEMENTED |

## Evaluator isolation, contamination, and authority

| Requirement | Source | Control type | Required enforcement | Evidence artifact | Current status |
|---|---|---|---|---|---|
| Evaluator independence is determined by accessible state and authority, not by a fresh-looking session or role label. | ADR-0002 Decision 1 | HUMAN + AUTOMATED | For each evaluator, document all reachable persistent state, tools, connectors, filesystems, repositories, memories, session stores, and external retrieval paths. Preflight rejects any unexplained retrieval path. | evaluator-access map + preflight report | UNIMPLEMENTED |
| The governed evaluator must not control the authoritative evidence used to establish its own compliance. | ADR-0002 Decision 2 | HUMAN + AUTOMATED | Evidence directories, manifests, sealed truth, and frozen packets must be outside evaluator write authority. Evaluator may write only its designated output/attempt area. | permission snapshot + custody record | UNIMPLEMENTED |
| Independence claims must be supported by recorded, checkable evidence. | ADR-0002 Decision 3 | AUTOMATED | Archive effective configuration, environment, permitted tools/connectors, packet hash, isolation settings, and contamination-probe result for every evaluator arrangement. Missing evidence blocks authorization. | evaluator-independence record | UNIMPLEMENTED |
| Prior exposure to deliberately withheld information permanently disqualifies an actor from blinded evaluation for that execution. | ADR-0002 Decision 4; dual-model pilot coordinator rule | HUMAN | Before assigning an evaluator, record known exposure to sealed truth, candidate-specific withheld facts, prior judgments, and other excluded material. Any such exposure disqualifies that actor for the same execution. | exposure declaration + founder eligibility decision | UNIMPLEMENTED |
| Generic protocol-design participation alone does not disqualify an evaluator. | ADR-0002 Decision 4 | HUMAN | Eligibility record distinguishes generic protocol exposure from candidate/truth exposure rather than treating role title alone as disqualifying. | exposure declaration | UNIMPLEMENTED |
| Evaluator context must be bounded to what is reasonably necessary for the gate. | ADR-0002 Decision 5 | HUMAN + AUTOMATED | Frozen packet manifest lists all authorized inputs. Any broader access must be justified before execution. Runtime/tooling prevents access beyond that boundary. | packet manifest + access justification | UNIMPLEMENTED |
| Codex must run without inherited MCP servers, plugins, connectors, repository history, prior run records, or adjacent candidate branches unless explicitly authorized. | dual-model pilot preregistration: Codex isolation matrix | AUTOMATED | Provision fresh execution home/configuration. Enumerate tools and mounted paths. Candidate packet is the only candidate source. Preflight rejects inherited state or unauthorized repo access. | Codex effective-config archive + tool/path inventory | UNIMPLEMENTED |
| A Claude evaluator, if used, must use the frozen isolated invocation method rather than an ordinary consumer account session. | dual-model pilot preregistration: Claude isolation matrix | AUTOMATED + HUMAN | New preregistration must identify the exact supported invocation method. Preflight verifies no account memory, prior transcript, retrieval tools, or unauthorized connectors are attached. | Claude effective-request archive + tool inventory | UNIMPLEMENTED |
| Hermes, if used for orchestration/evaluation, must use a dedicated disposable HERMES_HOME rather than a profile under a shared home. | dual-model pilot preregistration: Hermes isolation matrix | AUTOMATED | Runner creates a new disposable HERMES_HOME and verifies no pre-existing profiles, session stores, memories, MCP state, or inherited plugins are reachable. | HERMES_HOME manifest + directory/config inventory | UNIMPLEMENTED |
| Hermes memory, user-profile state, and session search must be disabled or structurally isolated from all other evaluator/coordinator state. | dual-model pilot preregistration: Hermes isolation matrix | AUTOMATED | Preflight tests effective settings and filesystem reachability, not merely configuration declarations. | Hermes isolation verification log | UNIMPLEMENTED |
| A contamination canary must run before real evaluation. | dual-model pilot preregistration: Contamination canary | AUTOMATED | Real evaluator authorization requires a completed clean canary result generated under the same frozen provisioning recipe. | canary result + hashes | UNIMPLEMENTED |
| Canary sentinel must be generated only at execution time and never appear in protocol docs, coordination records, evaluator packets, persistent memory, or ordinary run notes before the probe. | dual-model pilot preregistration: Sentinel secrecy rule | AUTOMATED + HUMAN | Generate sentinel inside controlled execution tooling after protocol freeze. Store only in designated sacrificial forbidden source and restricted evidence record. Preflight scans authorized packet/config artifacts for accidental sentinel inclusion. | sentinel generation record + leak scan | UNIMPLEMENTED |
| Canary must plant the sentinel in a sacrificial source structurally analogous to the retrieval path being tested. | dual-model pilot preregistration: Canary procedure | HUMAN + AUTOMATED | Canary manifest identifies the exact forbidden source and claimed boundary. Probe request must not contain the sentinel itself. | canary manifest + archived probe request | UNIMPLEMENTED |
| Canary and real evaluator must be separate environments created from the same canonical recipe. | dual-model pilot preregistration: Canary procedure / configuration equivalence | AUTOMATED | Destroy canary invocation/context and provision a distinct real environment. Compare canonicalized configs byte-for-byte before real execution. | canary config hash + real config hash + equivalence result | UNIMPLEMENTED |
| Sentinel reproduction or demonstrated knowledge invalidates that evaluator environment. | dual-model pilot preregistration: Canary procedure | AUTOMATED | Canary parser checks for sentinel reproduction/knowledge. Positive contamination result blocks real evaluator provisioning and records INVALID isolation attempt. | contamination result + attempt archive | UNIMPLEMENTED |
| Canary success does not prove absence of undocumented provider-internal mechanisms. | dual-model pilot preregistration: Epistemic limit | ASSUMPTION | Record this limitation explicitly in the preregistration and final report. Do not describe canary success as proof of absolute independence. | accepted limitation statement | UNIMPLEMENTED |
| No evaluator may assess or certify whether its own participation was useful or necessary. | dual-model pilot preregistration: Scope and limits | HUMAN | Architecture/performance conclusions come only from frozen scoring/adjudication and founder authority, not evaluator self-assessment. | final decision record | UNIMPLEMENTED |
| Independent review of this enforcement matrix must occur before it becomes an authorization gate. | Run-009 integrity record; ADR-0002 evidence invariant | HUMAN | A reviewer who did not author this matrix examines it before adoption. Reviewer must not receive sealed truth. Review outcome is preserved. | independent review artifact + founder disposition | UNIMPLEMENTED |

## Fusion, scoring, metrics, and classification

| Requirement | Source | Control type | Required enforcement | Evidence artifact | Current status |
|---|---|---|---|---|---|
| Security fusion uses the frozen three-value OR rule exactly as preregistered. | dual-model pilot preregistration: Fusion rule | AUTOMATED | Implement a complete truth table for PASS/FAIL/ABSTAIN pairs. Unit tests cover every combination. No heuristic interpretation permitted. | fusion implementation hash + truth-table tests | UNIMPLEMENTED |
| Architecture, Quality, and Privacy use agreement-or-escalate, never vote. | dual-model pilot preregistration: Fusion rule | AUTOMATED | Same non-ABSTAIN verdict produces autonomous verdict; every other combination escalates. Unit tests cover PASS/PASS, FAIL/FAIL, PASS/FAIL, PASS/ABSTAIN, FAIL/ABSTAIN, ABSTAIN/ABSTAIN. | fusion implementation hash + tests | UNIMPLEMENTED |
| Cross-critique may change evaluator verdicts but cannot itself adjudicate truth. | dual-model pilot preregistration: Procedure | AUTOMATED + HUMAN | Post-cross verdicts are recorded separately from adjudication. Scoring pipeline prohibits model consensus from writing truth labels. | post-cross ledgers + scorer separation test | UNIMPLEMENTED |
| Escalation outcome buckets must be computed mechanically against sealed truth. | dual-model pilot preregistration: Metrics ledger | AUTOMATED | For each escalated case, scorer records matches Codex / matches second evaluator / matches neither using the frozen binary-truth semantics. | escalation ledger + scorer tests | UNIMPLEMENTED |
| ABSTAIN semantics must follow the frozen scoring rules. | dual-model pilot preregistration: ABSTAIN scoring | AUTOMATED | True-defect ABSTAIN counts against detection burden but not direct FN; benign ABSTAIN is recorded separately and not FP. Unit tests cover all truth/verdict combinations. | scorer truth-table tests | UNIMPLEMENTED |
| Solo FP/FN and abstention metrics must be computed per evaluator from blinded first-pass outputs only. | dual-model pilot preregistration: Metrics ledger | AUTOMATED | Scorer reads frozen first-pass ledgers only. Post-cross or adjudicated outputs cannot overwrite solo metrics. | solo-metrics report + input manifest | UNIMPLEMENTED |
| Unique true-defect catches are measured from blinded first-pass outputs before cross-exposure. | dual-model pilot preregistration: Decision rule | AUTOMATED | Scorer computes unique catches only from first-pass frozen ledgers and sealed truth. | unique-catch report | UNIMPLEMENTED |
| Security harmful-flip metric is computed exactly from first-pass and post-cross Security verdicts on true defects. | dual-model pilot preregistration: SECURITY_HARMFUL_FLIP | AUTOMATED | For each true Security defect, any correct first-pass FAIL changing after cross-exposure to anything other than FAIL is counted. | security-flip report + tests | UNIMPLEMENTED |
| Final autonomous Security miss is computed from fused post-cross Security verdict before any oracle intervention. | dual-model pilot preregistration: FINAL_AUTONOMOUS_SECURITY_MISS | AUTOMATED | Any true Security defect with fused PASS or ABSTAIN counts as a miss. | autonomous-security-miss report | UNIMPLEMENTED |
| Autonomous residual defect burden counts each true-defect candidate/gate case at most once. | dual-model pilot preregistration: residual burden definition | AUTOMATED | Scorer deduplicates by candidate/gate key and applies frozen burden semantics. | residual-burden report + tests | UNIMPLEMENTED |
| False-positive band must use the frozen comparison against the better/worse solo baseline exactly as preregistered. | dual-model pilot preregistration: FP band | AUTOMATED | Threshold implementation is encoded directly from preregistered formula and covered by boundary tests. | FP-band report + tests | UNIMPLEMENTED |
| Residual-burden classification must use the frozen comparison to the better solo baseline exactly as preregistered. | dual-model pilot preregistration: Decision rule | AUTOMATED | `<`, `=`, and `>` cases map only to the preregistered outcome conditions. | residual threshold tests | UNIMPLEMENTED |
| Unique-catch thresholds must use the frozen values without reinterpretation. | dual-model pilot preregistration: Decision rule | AUTOMATED | ≥2 true unique catches by each evaluator satisfies promising criterion; exactly 1 on either side is inconclusive; 0 on either side is fail, subject to INVALID precedence and all other criteria. | threshold tests | UNIMPLEMENTED |
| Any SECURITY_HARMFUL_FLIP is a hard performance failure if the execution is otherwise valid. | dual-model pilot preregistration: Decision rule | AUTOMATED | Classification engine checks this hard condition before soft thresholds. | classification trace | UNIMPLEMENTED |
| Any FINAL_AUTONOMOUS_SECURITY_MISS is a hard performance failure if the execution is otherwise valid. | dual-model pilot preregistration: Decision rule | AUTOMATED | Classification engine checks this hard condition before soft thresholds. | classification trace | UNIMPLEMENTED |
| INVALID has absolute precedence over PROMISING, INCONCLUSIVE, or FAIL. | dual-model pilot preregistration: INVALID rule | AUTOMATED | Classification engine first checks protocol-integrity state. If INVALID, no performance classification is computed or emitted as authoritative. | classification trace + invalidation record | UNIMPLEMENTED |
| Performance and integrity classifications must never coexist as authoritative final statuses. | dual-model pilot preregistration: INVALID precedence | AUTOMATED | Final report generator accepts exactly one authoritative terminal state. Exploratory metrics, if allowed, must be labeled non-authoritative. | report-schema validation | UNIMPLEMENTED |
| The pilot's sole authorized conclusion is whether a larger balanced replication is warranted; it cannot authorize standing architecture changes. | dual-model pilot preregistration: Purpose / scope | HUMAN | Final decision template restricts conclusions to the preregistered scope. Any standing architecture change requires a separate ADR and independent evidence. | founder decision record | UNIMPLEMENTED |
| No result may be generalized beyond the frozen instrument's coverage. | dual-model pilot preregistration: Scope and limits | HUMAN | Final report must state instrument limitations and prohibit general claims about evaluator quality or all defect classes. | final-report checklist | UNIMPLEMENTED |
| No evaluator-superiority conclusion may be drawn from this pilot. | dual-model pilot preregistration: Purpose / scope | HUMAN | Report template bans ranking/general “better model” conclusions. Metrics remain scoped to the instrument. | final-report checklist | UNIMPLEMENTED |
| Cost criterion must be mechanically measurable for the exact named evaluator design before execution. | dual-model pilot preregistration: Decision rule; Run-009 integrity record | HUMAN + AUTOMATED | New preregistration must define exact cost denominator and measurement source for the actual evaluators used. Preflight rejects undefined, unavailable, or substituted denominators. | cost-metric specification + preflight check | UNIMPLEMENTED |
| Every metric required for classification must be computable before the run is authorized. | reproducibility requirement; Run-009 integrity record | AUTOMATED | Preflight runs scorer on synthetic complete data and verifies every required metric field can be produced. Missing metric implementation blocks real execution. | synthetic scoring report | UNIMPLEMENTED |
| Final report must distinguish autonomous results from post-adjudication results. | dual-model pilot preregistration: Procedure / final pipeline definition | AUTOMATED + HUMAN | Report generator emits separate sections/fields and prohibits collapsing them into one aggregate. | final report schema + review checklist | UNIMPLEMENTED |

## Independent-review corrections

### Review exposure and future evaluator eligibility

| Requirement | Source | Control type | Required enforcement | Evidence artifact | Current status |
|---|---|---|---|---|---|
| Participation in protocol or enforcement review must be recorded as part of that actor's exposure history before any later blinded-evaluator eligibility decision. | ADR-0002 Decision 4; independent review C2 | HUMAN + AUTOMATED | Every protocol reviewer receives an exposure record identifying the exact reviewed packet hash and categories of information seen. Preflight refuses evaluator authorization without a complete exposure declaration and founder eligibility decision. | reviewer exposure record + packet hash + eligibility decision | UNIMPLEMENTED |

### Matrix status governance

| Requirement | Source | Control type | Required enforcement | Evidence artifact | Current status |
|---|---|---|---|---|---|
| No matrix row may move from GAP to satisfied based solely on the implementer's own assertion. | ADR-0002 Decisions 2 and 3; independent review M1 | HUMAN + AUTOMATED | Every row closure must name an implementer and a distinct verifier. Status changes require a verification artifact signed/recorded by the verifier and referenced by hash. Preflight treats unverified closures as GAP. | row-verification record + artifact hash + verifier identity | UNIMPLEMENTED |
| A substantive matrix revision after independent review requires another independent review before authorization. | independent review M7 | HUMAN + AUTOMATED | Any change to requirement text, control type, enforcement semantics, or evidence expectations changes the matrix hash and resets review status to unreviewed. Authorization requires a fresh review record for the new hash. | matrix hash history + independent review record | UNIMPLEMENTED |

### Exposure declaration and evaluator eligibility

| Requirement | Source | Control type | Required enforcement | Evidence artifact | Current status |
|---|---|---|---|---|---|
| No evaluator may be authorized without a completed exposure declaration referenced in the frozen preflight manifest. | ADR-0002 Decision 4; independent review M2 | AUTOMATED + HUMAN | Preflight requires a hash-referenced exposure declaration for each evaluator. Missing declaration blocks execution. | exposure declaration + preflight manifest reference | UNIMPLEMENTED |
| Exposure classification must use a preregistered checklist rather than retrospective narrative judgment. | ADR-0002 Decision 4; independent review M3 | HUMAN + AUTOMATED | Eligibility checklist explicitly records whether the actor saw: sealed truth, candidate-specific withheld facts, prior evaluator verdicts, prior judgments on the same candidate, adjudication material, protocol-only material, integrity/runtime records, or other excluded state. Preflight records founder eligibility decision against this checklist before authorization. | exposure checklist + founder eligibility decision | UNIMPLEMENTED |

### Cross-critique handoff integrity

| Requirement | Source | Control type | Required enforcement | Evidence artifact | Current status |
|---|---|---|---|---|---|
| The exact first-pass bytes handed to the other evaluator during cross-critique must be frozen and independently auditable. | dual-model pilot preregistration: Cross-critique phase; independent review M4 | AUTOMATED | Before cross-critique, hash each evaluator's exact first-pass response. Archive the exact handoff payload delivered to the opposite evaluator and verify its embedded response hash matches the frozen first-pass artifact. Any mismatch aborts cross-critique. | first-pass hash + handoff payload + handoff verification log | UNIMPLEMENTED |

### Sealed-truth backup independence

| Requirement | Source | Control type | Required enforcement | Evidence artifact | Current status |
|---|---|---|---|---|---|
| The sealed-truth recovery copy must be logically or physically independent from the primary storage failure domain. | Run-009 integrity record; independent review M5 | HUMAN + AUTOMATED | A second directory on the same filesystem or NVMe is insufficient. The recovery copy must reside on an independently recoverable storage location or service. Primary and recovery hashes are verified at creation and again before scored execution. | recovery-location record + primary/recovery hashes + re-verification log | UNIMPLEMENTED |

### Scorer and classifier independence

| Requirement | Source | Control type | Required enforcement | Evidence artifact | Current status |
|---|---|---|---|---|---|
| The scorer, fusion logic, and classification implementation must receive independent review before being used authoritatively. | ADR-0002 evidence invariant; independent review M6 | HUMAN + AUTOMATED | Scoring code, truth tables, boundary tests, and classification logic are reviewed by someone other than the implementer. The reviewed implementation hash is frozen. Preflight refuses an unreviewed or hash-mismatched scorer. | scorer review record + implementation hash + test results | UNIMPLEMENTED |

### Review-packet and document identity

| Requirement | Source | Control type | Required enforcement | Evidence artifact | Current status |
|---|---|---|---|---|---|
| Every document included in an independent review packet must have an exact raw-file identity that can be independently verified. | independent review process note / F1 | AUTOMATED | Review packet includes a manifest listing each source file's canonical path, byte count, and raw SHA-256 before packet assembly. Reviewers verify the manifest against the supplied source files or explicitly record when embedded serialization prevents byte-identical reconstruction. | review-packet source manifest + raw file hashes | UNIMPLEMENTED |
| Review-packet assembly must not imply that an extracted embedded section can reproduce the original raw-file hash unless that serialization is explicitly defined. | independent review process note / F1 | AUTOMATED + HUMAN | Packet instructions distinguish raw source-file hashes from packet-container hashes. Any canonicalization or extraction rule used for verification must be frozen and documented in advance. | packet-format specification + verification log | UNIMPLEMENTED |

### Final-report safeguards

| Requirement | Source | Control type | Required enforcement | Evidence artifact | Current status |
|---|---|---|---|---|---|
| A null or non-PROMISING result must not be reported as evidence that the evaluators are equivalent. | dual-model pilot preregistration: Scope and limits; independent review N1 | HUMAN | Final-report checklist explicitly states that the pilot is underpowered for small effects and that a null result establishes only that this instrument did not demonstrate the preregistered effect size. | final-report checklist | UNIMPLEMENTED |
| Synthetic preflight must explicitly test corrupted or hash-mismatched sealed truth. | Run-009 integrity record; independent review N2 | AUTOMATED | Synthetic harness deliberately alters the truth artifact and verifies that preflight/scoring aborts before any metric is computed. | synthetic corruption-test log | UNIMPLEMENTED |
| Final authoritative reports must be frozen and hash-protected after generation. | evidence integrity; independent review N3 | AUTOMATED + HUMAN | Final report is hashed immediately after approval. Any later edit creates a new version with a new hash and recorded provenance; prior versions remain preserved. | final-report hash + version history | UNIMPLEMENTED |
| Run-009 quarantine prohibitions must remain explicitly visible in replication documentation. | Run-009 integrity record; independent review N4 | HUMAN + AUTOMATED | Replication preregistration and final-report checklist explicitly reference the Run-009 quarantine and prohibit using Run-009 outputs for confirmatory claims, evaluator assignment, architecture adoption, or production-policy changes. | replication preregistration + report checklist | UNIMPLEMENTED |

### Visibility-sequencing refinement

| Requirement | Source | Control type | Required enforcement | Evidence artifact | Current status |
|---|---|---|---|---|---|
| No solo evaluator result may become visible, directly or indirectly, to the founder, coordinator, protocol designer, or any actor able to alter evaluator assignment or execution design until both evaluator identities are frozen and both solo phases are complete. | Freeze conditions; Run-009 integrity record; independent review C1; closure review MAJOR 1 | AUTOMATED + HUMAN | Before either solo run begins, freeze and hash both evaluator identities and the protocol manifest. Solo execution must run non-interactively with stdout/stderr and result artifacts inaccessible to all actors able to influence design or evaluator assignment. Live terminal/session observation is prohibited. Release is allowed only after both solo completion hashes exist and the release event is recorded. Any premature visibility invalidates the execution. | evaluator manifest + protocol manifest + access-control record + solo completion hashes + release-event record | UNIMPLEMENTED |
| Freeze ordering must be explicitly auditable. | closure review MINOR 1 | AUTOMATED | Record a monotonic and wall-clock freeze event before any scored evaluator process starts. Every scored attempt records its start event and must prove ordering after the freeze event. | freeze-order ledger + timestamps + attempt start records | UNIMPLEMENTED |

### Status vocabulary and exposure cross-reference refinement

`Control type` and `Implementation status` are separate axes.

Permitted control types:
- `AUTOMATED`
- `HUMAN`
- `AUTOMATED + HUMAN`
- `ASSUMPTION`

Permitted implementation statuses:
- `UNIMPLEMENTED`
- `IMPLEMENTED_UNVERIFIED`
- `VERIFIED`
- `BLOCKED`

For this draft matrix, existing rows whose Current status is `GAP` are to be
interpreted as `UNIMPLEMENTED`. Before authorization, status terminology must
be normalized so `GAP` is not used as both a design classification and an
implementation state.

The prior-exposure disqualification requirement and the exposure-checklist
requirement are complementary:
- the disqualification row states the governing eligibility rule;
- the checklist row supplies the operational evidence used to apply that rule.

Neither may be satisfied without the other.
