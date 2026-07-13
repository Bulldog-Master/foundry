# Product Charter: Daang Remote

- **Status:** Ratified
- **Ratified:** 2026-07-12
- **Ratifying authority:** Bulldog-Master, Founder
- **Last amended:** 2026-07-13 (record: PR #3)
- **Author(s):** Bulldog-Master (founder)

## Why this product exists

The founder needs to interact with his own computing devices — desktops, laptops, and other personal machines — securely, privately, and reliably from wherever he happens to be, across operating systems and networks he does not always control. In 2026, that need is served almost exclusively by a small number of commercial remote-access products that are expensive, closed, metadata-heavy, and increasingly awkward for people who care about privacy or who work across many devices and platforms. The founder uses remote desktop tooling daily and has repeatedly encountered the same failure modes: recurring per-seat pricing that scales badly for a single power user with many machines; opaque relay infrastructure that observes far more metadata than the session itself requires — including metadata that enables correlation of sessions, devices, and identities that a well-designed system would keep unlinkable; weak or absent posture toward post-quantum threats; lock-in to specific operating systems, app stores, or account systems; and user experience that has been optimized for enterprise procurement rather than for the person actually sitting at the keyboard.

Daang Remote exists because the founder needs a way to interact with his own computing environment — treated as a first-class concern of privacy, longevity, and control — regardless of location, and because no existing product credibly serves that need today. Remote desktop is the first expression of that need, not its permanent definition.

## Mission

Daang Remote enables secure, privacy-respecting interaction with the founder's own computing devices regardless of location, with a privacy posture built on **metadata minimization, metadata resistance, prevention of avoidable correlation, and unlinkability wherever the workflow permits and the product remains usable** — providing cryptographic agility with a present-day post-quantum posture, and delivered with a user experience good enough that the founder actively prefers it to any commercial alternative. Unavoidable linkabilities are documented and justified rather than hidden. Once that bar is met, the same properties extend to other individuals and eventually to organizations. Remote desktop is the first expression of this mission; the mission itself is broader than any single access modality.

## Users

- **Primary (now):** The founder. Daang Remote must be excellent for one real person doing real daily work before it is offered to anyone else. This is a deliberate sequencing choice, not an aspiration.
- **Secondary (later):** Individuals with similar concerns — privacy-conscious professionals, developers, researchers, and technically capable users who currently tolerate commercial remote-desktop tools rather than endorse them.
- **Tertiary (much later):** Small teams and eventually organizations that need the same properties at greater scale, with administrative controls added without compromising the privacy posture.

The size, shape, and willingness-to-pay of the secondary and tertiary populations are not currently known. See Evidence and assumptions.

## In scope

- Remote access to the founder's own computers across platforms, as the first expression of the broader mission.
- Engineering discipline that enforces the full privacy posture: **metadata minimization, metadata resistance, prevention of avoidable correlation, and unlinkability where the workflow permits and the product remains usable.** Metadata collected, stored, or observable by any operator (including the Daang project itself) is bounded to what the session functionally requires and is documented. Any unavoidable linkability is explicitly documented and justified.
- Cryptographic agility as a design requirement: the architecture must allow cryptographic primitives to evolve without fundamental redesign. During the current phase, Daang Remote is designed with a post-quantum security posture wherever practical and justified by evidence, rather than assuming today's asymmetric algorithms are permanent.
- AI assistance where it genuinely improves the experience, subject to the Constitution's rules on AI authority and human review.
- A user experience that the founder prefers over existing commercial remote-desktop products.
- Platform independence: no permanent dependency on a single operating system, app store, cloud provider, or account system.
- Establishing patterns (identity, transport, update, telemetry posture) that later Daang products can reuse, with the engineering-identity / product-identity seam explicitly maintained.

## Out of scope

- General-purpose screen sharing for meetings, presentations, or collaboration.
- Unattended remote support of third parties' computers as a helpdesk product.
- File-sync, backup, password management, VPN, or browser features — these may become sibling Daang products, but Daang Remote will not absorb them.
- Ad-supported or data-monetized tiers of any kind.
- Features whose only purpose is to match a competitor's checklist.
- Enterprise administrative surface area before the individual product is genuinely excellent.
- Any capability designed to enable one person to monitor or control another person's computer without that person's informed consent.
- Product-doctrine commitments to any specific transport, mixnet, or messaging mechanism. Selection of transport and control/data-plane mechanisms is a downstream engineering decision (see **Mechanism boundary** below), not a charter commitment.

## Does not optimize for

- Market scale, user counts, or growth curves before personal-use excellence is achieved.
- Feature parity with commercial remote-desktop suites.
- Enterprise procurement checklists, RFPs, or compliance certifications ahead of genuine need.
- Time-to-market at the cost of privacy, cryptographic posture, or platform independence.
- Short-term convenience that would compromise long-term trust.
- Investor-legibility, valuation narratives, or venture-scale trajectories.

## Non-negotiables

- **Metadata minimization** is a hard constraint, not a marketing posture.
- **Metadata resistance** — the product's operator, its infrastructure, and any intermediary must not be positioned to observe more than the session functionally requires, even opportunistically.
- **Prevention of avoidable correlation** — sessions, devices, accounts, and identifiers must not be linkable to each other, to the founder, or to future users beyond what the workflow strictly requires.
- **Unlinkability where the workflow permits and the product remains usable** — where a design choice can preserve unlinkability without breaking the product, it must; where it cannot, the linkability is documented and justified rather than accepted silently.
- Cryptographic agility is a design requirement, and the present-day engineering posture is post-quantum where practical and evidence-supported.
- No data monetization, ad-supported tier, or third-party analytics that observe session or user behavior.
- No permanent dependency on a single operating system, app store, cloud provider, or third-party identity system.
- The product must not be shaped into a tool whose easiest use is covert surveillance of another person.
- Founder-first sequencing: personal-use excellence precedes any external release.

## Design philosophy

- Build for enduring usefulness before market scale.
- Prefer simple systems over clever systems.
- Minimize metadata by design rather than by policy, and prefer designs that make correlation structurally difficult over designs that rely on operator restraint.
- Preserve replaceability of infrastructure whenever practical.
- Choose long-term trust over short-term convenience.

## Mechanism boundary

Daang Remote's charter commits to **properties** — metadata minimization, metadata resistance, prevention of avoidable correlation, unlinkability where the workflow permits, cryptographic agility, and a present-day post-quantum posture. It does **not** commit to any specific transport, mixnet, messaging fabric, or identity mechanism as product doctrine.

Mechanisms currently under consideration — including **cMixx** and **xxDK** — are **candidate mechanisms**, not product commitments. They are named here so that later readers understand what was being evaluated at ratification, not to enshrine them.

**Selection of transport and of the control-plane and data-plane mechanisms is deferred to a later Architecture ADR** under the Foundry 1 gate contract. That ADR is expected to:

- state which candidates were evaluated and against which properties;
- name the selected mechanism(s) and the fallback posture;
- record the evidence supporting the selection at that time;
- state the review trigger or expiry after which the selection is re-examined.

Until that ADR exists, no code, documentation, or product surface may treat any specific mechanism as fixed by this charter.

## Evidence and assumptions

- **Known:**
  - The founder personally experiences the problem daily and pays for commercial remote-desktop software today.
  - Commercial remote-desktop products exist, are widely used, and have well-documented pricing, privacy, metadata, and correlation characteristics that the founder considers inadequate.
  - Post-quantum cryptographic primitives suitable for transport security exist and are being standardized; a post-quantum posture is technically achievable today, not speculative.
  - Cross-platform remote access is technically feasible; multiple open-source and commercial implementations demonstrate the underlying problem is solvable.
  - Metadata-resistant and unlinkability-preserving transports exist as candidate mechanisms; whether any of them meets Daang Remote's combined property, latency, and usability requirements is an open engineering question to be answered under the Architecture ADR referenced above.
- **Assumed:**
  - Other individuals share the founder's concerns strongly enough to adopt an alternative once it exists. This is not yet validated by any external user, waitlist, survey, or purchase.
  - A privacy posture combining metadata minimization, metadata resistance, prevention of avoidable correlation, and unlinkability where the workflow permits can be delivered with cryptographic agility and without unacceptable losses in latency, reliability, or user experience.
  - The founder's own use is a sufficiently representative starting point that a product excellent for him will be a credible starting point for others. This may prove false and would then require re-scoping.
  - There is an eventual willingness to pay — from individuals, and later from organizations — sufficient to sustain the product without resorting to data monetization. The size and shape of that willingness is unknown.
  - The Daang project can maintain the discipline, over years, to keep the product's privacy and independence properties intact under commercial pressure.

## Success criteria

Daang Remote is working when:

- The founder has completely replaced his commercial remote-access software with Daang Remote for normal daily work, by preference and not by obligation, and has stopped paying for the commercial alternative it replaces.
- Every personal machine intended for remote access is managed through Daang Remote.
- Weekly usage is measured and reviewed as an ongoing indicator, without a pre-committed numeric threshold at this stage.
- Session reliability, responsiveness, and usability are evaluated qualitatively and comparatively against the commercial alternative, and Daang Remote is at least as usable for the kinds of work the founder actually does.
- The system's metadata exposure is small enough, and its resistance to observation and correlation is strong enough, that a technically literate skeptic examining it would agree it materially improves on commercial alternatives on all four dimensions — minimization, resistance, correlation avoidance, and unlinkability — and that any residual linkability is explicitly documented and justified.
- The cryptographic posture demonstrates cryptographic agility and a credible present-day post-quantum direction, and can be reviewed by someone qualified to assess that claim.
- External success metrics (adoption, retention, willingness-to-pay signals from individuals outside the founder) will be defined before the first public release, not invented now.

The founder should reconsider or discontinue Daang Remote if, after honest effort:

- He does not, in practice, prefer it to the commercial alternative for his own work.
- The metadata-minimization, metadata-resistance, correlation-avoidance, unlinkability, or cryptographic-agility properties cannot be maintained without making the product unusable.
- No individual outside the founder shows durable interest once the product is offered.
- Sustaining it would require compromises (data monetization, mandatory accounts on third-party identity providers, platform lock-in) that violate this charter or the Constitution.

## Constraints

- **Constitutional:** All work is bound by the Foundry Constitution, including the rules on AI authority, human review, doctrine change, the four-gate operating contract, and responsible use.
- **Privacy:** Metadata minimization, metadata resistance, prevention of avoidable correlation, and unlinkability where the workflow permits are hard constraints, not marketing posture. Features that would collect more metadata than the session needs, that would enable a new observation position for any operator, or that would introduce avoidable correlation or new linkabilities, must be justified in writing and reviewed under the Privacy and Metadata Gate. Unavoidable linkabilities are documented and justified explicitly.
- **Security:** Cryptographic agility is a hard architectural constraint on transport and identity primitives; the current engineering posture is post-quantum wherever practical and evidence-supported.
- **Platform independence:** No design decision may create a permanent dependency on a single operating system, app store, cloud provider, or third-party identity system.
- **Mechanism neutrality:** No charter-level commitment to a specific transport, mixnet, messaging fabric, or identity mechanism. Selection is made under a later Architecture ADR.
- **Financial:** The product must be buildable and maintainable at the scale of a founder-led project before it is offered more widely; it must not require venture-scale spending to reach personal-use viability.
- **Ethical:** Daang Remote must not be designed, marketed, or documented in ways that make covert surveillance of another person easier than legitimate remote access to one's own machines.
- **Time:** The founder's own use is the first milestone. Broader release is explicitly deferred until that milestone is met.

## Risks

- **Founder-only fit:** The product may end up excellent for exactly one person and uninteresting to anyone else. Mitigation: name this risk now, treat single-user excellence as necessary but not sufficient, and test external interest before investing in scale.
- **Commercial success creates pressure to compromise the charter:** If Daang Remote gains traction, revenue, or user growth, that success itself will generate ongoing pressure to add analytics, mandatory accounts, growth-oriented features, platform-specific integrations, or data-monetized tiers that violate this charter. Mitigation: treat this pressure as a predictable and permanent condition rather than a surprise; any such change requires explicit doctrine-level review under the Constitution, not a routine product decision, and the charter is re-read whenever a commercially attractive shortcut is proposed.
- **Privacy erosion under pressure:** Commercial or operational pressure may push toward collecting more metadata, adding accounts, tolerating new correlation, or integrating third-party analytics. Mitigation: the Constitution and this charter treat metadata minimization, metadata resistance, correlation avoidance, and unlinkability-where-possible as hard constraints; any change requires explicit doctrine-level review under the Privacy and Metadata Gate.
- **Correlation and linkability drift:** Small, individually reasonable choices can accumulate into a system that is much more correlatable than any single decision suggested. Mitigation: linkability is evaluated at the seam by the Privacy and Metadata Gate on every substantive change, not only at feature-launch time.
- **Cryptographic misjudgment:** Getting post-quantum choices wrong, or mistaking agility for security, could produce a false sense of protection. Mitigation: treat cryptographic decisions as reviewable by qualified outsiders; do not present claims that have not been reviewed.
- **Mechanism lock-in by accident:** Building against a specific candidate mechanism (for example cMixx or xxDK) can create hidden coupling that later hardens into de-facto product doctrine. Mitigation: the Architecture ADR that selects mechanisms must name the fallback and the exit cost, and product code must not treat any mechanism-specific behaviour as promised in the charter.
- **AI over-reach:** AI assistance could quietly expand into decisions that should remain human, or into features that require exfiltrating session content. Mitigation: AI usage is bound by the Constitution's authority rules and by this charter's privacy constraints.
- **Dual-use / misuse:** Any remote-access tool can, in principle, be used to spy on or control another person's computer. Mitigation: Daang Remote is scoped to access of one's own machines; features, documentation, and defaults must not make covert third-party surveillance easier than legitimate use.
- **Platform capture:** An operating system vendor, app store, or identity provider may attempt to force changes incompatible with this charter. Mitigation: platform independence is a design constraint from day one, not a later refactor.
- **Founder attention:** Daang Remote is one of several intended Daang products. Mitigation: it is explicitly first, and no other product is authorized to compete for attention until this one meets its personal-use success criteria.

## Constitutional principles this product depends on

- **Replaceable intelligence and platform independence:** Daang Remote must survive changes in AI models, frameworks, cloud providers, and operating systems. Replaceable does not mean equivalent; model-specific artifacts are expected to be re-tuned on swap.
- **Privacy and metadata minimization (and its extensions):** The product is a direct expression of metadata minimization, metadata resistance, prevention of avoidable correlation, and unlinkability where the workflow permits.
- **AI authority limits and human review:** AI assistance inside the product, and AI-generated changes to the product, are bound by the Constitution.
- **Doctrine vs policy:** The privacy posture (all four properties), cryptographic agility with a present-day post-quantum posture, mechanism neutrality, and platform independence are treated as doctrine here; changing them requires explicit founder approval, not a routine PR.
- **Builder / evaluator separation and the four-gate operating contract:** Every substantive change to Daang Remote is evaluated under Architecture, Security and Cryptography, Privacy and Metadata (owner of the engineering-identity / product-identity seam), and Quality and Verification gates.
- **Responsible use:** The product must not be shaped into a tool whose easiest use is to harm others.
- **Founder-first sequencing:** Personal-use excellence precedes external release; this charter formalizes that sequencing for Daang Remote specifically.

**Principles at unusual risk of drift for this product:**

- **The full privacy posture** — under any future pressure to add analytics, accounts, third-party integrations, or shared identifiers that would introduce new correlation or linkability.
- **Platform independence** — under pressure to adopt platform-specific identity, distribution, or payment systems that would be easier in the short term.
- **Mechanism neutrality** — under pressure to bake a specific transport or mixnet into the product's public identity before an Architecture ADR has ratified the choice.
- **Scope discipline** — the temptation to absorb adjacent problems (sync, backup, VPN, password management) into Daang Remote instead of keeping them as separate future products.
- **Charter integrity under commercial success** — the temptation, once the product works, to trade small charter compromises for growth, revenue, or convenience.
