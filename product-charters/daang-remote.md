# Product Charter: Daang Remote

- **Status:** Draft
- **Date:** 2026-07-12
- **Author(s):** Bulldog-Master (founder)

## Why this product exists

The founder needs to interact with his own computing devices — desktops, laptops, and other personal machines — securely, privately, and reliably from wherever he happens to be, across operating systems and networks he does not always control. In 2026, that need is served almost exclusively by a small number of commercial remote-access products that are expensive, closed, metadata-heavy, and increasingly awkward for people who care about privacy or who work across many devices and platforms. The founder uses remote desktop tooling daily and has repeatedly encountered the same failure modes: recurring per-seat pricing that scales badly for a single power user with many machines; opaque relay infrastructure that observes far more metadata than the session itself requires; weak or absent posture toward post-quantum threats; lock-in to specific operating systems, app stores, or account systems; and user experience that has been optimized for enterprise procurement rather than for the person actually sitting at the keyboard.

Daang Remote exists because the founder needs a way to interact with his own computing environment — treated as a first-class concern of privacy, longevity, and control — regardless of location, and because no existing product credibly serves that need today. Remote desktop is the first expression of that need, not its permanent definition.

## Mission

Daang Remote enables secure, privacy-respecting interaction with the founder's own computing devices regardless of location — minimizing unnecessary metadata, maximizing user control, and providing cryptographic agility with a present-day post-quantum posture — delivered with a user experience good enough that the founder actively prefers it to any commercial alternative. Once that bar is met, the same properties extend to other individuals and eventually to organizations. Remote desktop is the first expression of this mission; the mission itself is broader than any single access modality.

## Users

- **Primary (now):** The founder. Daang Remote must be excellent for one real person doing real daily work before it is offered to anyone else. This is a deliberate sequencing choice, not an aspiration.
- **Secondary (later):** Individuals with similar concerns — privacy-conscious professionals, developers, researchers, and technically capable users who currently tolerate commercial remote-desktop tools rather than endorse them.
- **Tertiary (much later):** Small teams and eventually organizations that need the same properties at greater scale, with administrative controls added without compromising the privacy posture.

The size, shape, and willingness-to-pay of the secondary and tertiary populations are not currently known. See Evidence and assumptions.

## In scope

- Remote access to the founder's own computers across platforms, as the first expression of the broader mission.
- Engineering discipline that minimizes unnecessary metadata and maximizes user control: metadata collected, stored, or observable by any operator (including the Daang project itself) is bounded to what the session functionally requires and is documented.
- Cryptographic agility as a design requirement: the architecture must allow cryptographic primitives to evolve without fundamental redesign. During Foundry 0, Daang Remote is designed with a post-quantum security posture wherever practical and justified by evidence, rather than assuming today's asymmetric algorithms are permanent.
- AI assistance where it genuinely improves the experience, subject to the Constitution's rules on AI authority and human review.
- A user experience that the founder prefers over existing commercial remote-desktop products.
- Platform independence: no permanent dependency on a single operating system, app store, cloud provider, or account system.
- Establishing patterns (identity, transport, update, telemetry posture) that later Daang products can reuse.

## Out of scope

- General-purpose screen sharing for meetings, presentations, or collaboration.
- Unattended remote support of third parties' computers as a helpdesk product.
- File-sync, backup, password management, VPN, or browser features — these may become sibling Daang products, but Daang Remote will not absorb them.
- Ad-supported or data-monetized tiers of any kind.
- Features whose only purpose is to match a competitor's checklist.
- Enterprise administrative surface area before the individual product is genuinely excellent.
- Any capability designed to enable one person to monitor or control another person's computer without that person's informed consent.

## Does not optimize for

- Market scale, user counts, or growth curves before personal-use excellence is achieved.
- Feature parity with commercial remote-desktop suites.
- Enterprise procurement checklists, RFPs, or compliance certifications ahead of genuine need.
- Time-to-market at the cost of privacy, cryptographic posture, or platform independence.
- Short-term convenience that would compromise long-term trust.
- Investor-legibility, valuation narratives, or venture-scale trajectories.

## Non-negotiables

- Metadata minimization is a hard constraint, not a marketing posture.
- Cryptographic agility is a design requirement, and the present-day engineering posture is post-quantum where practical and evidence-supported.
- No data monetization, ad-supported tier, or third-party analytics that observe session or user behavior.
- No permanent dependency on a single operating system, app store, cloud provider, or third-party identity system.
- The product must not be shaped into a tool whose easiest use is covert surveillance of another person.
- Founder-first sequencing: personal-use excellence precedes any external release.

## Design philosophy

- Build for enduring usefulness before market scale.
- Prefer simple systems over clever systems.
- Minimize metadata by design rather than by policy.
- Preserve replaceability of infrastructure whenever practical.
- Choose long-term trust over short-term convenience.

## Evidence and assumptions

- **Known:**
  - The founder personally experiences the problem daily and pays for commercial remote-desktop software today.
  - Commercial remote-desktop products exist, are widely used, and have well-documented pricing, privacy, and metadata characteristics that the founder considers inadequate.
  - Post-quantum cryptographic primitives suitable for transport security exist and are being standardized; a post-quantum posture is technically achievable today, not speculative.
  - Cross-platform remote access is technically feasible; multiple open-source and commercial implementations demonstrate the underlying problem is solvable.
- **Assumed:**
  - Other individuals share the founder's concerns strongly enough to adopt an alternative once it exists. This is not yet validated by any external user, waitlist, survey, or purchase.
  - A metadata-minimizing architecture with cryptographic agility can be delivered without unacceptable losses in latency, reliability, or user experience.
  - The founder's own use is a sufficiently representative starting point that a product excellent for him will be a credible starting point for others. This may prove false and would then require re-scoping.
  - There is an eventual willingness to pay — from individuals, and later from organizations — sufficient to sustain the product without resorting to data monetization. The size and shape of that willingness is unknown.
  - The Daang project can maintain the discipline, over years, to keep the product's privacy and independence properties intact under commercial pressure.

## Success criteria

Daang Remote is working when:

- The founder has completely replaced his commercial remote-access software with Daang Remote for normal daily work, by preference and not by obligation, and has stopped paying for the commercial alternative it replaces.
- Every personal machine intended for remote access is managed through Daang Remote.
- Weekly usage is measured and reviewed as an ongoing indicator, without a pre-committed numeric threshold at this stage.
- Session reliability, responsiveness, and usability are evaluated qualitatively and comparatively against the commercial alternative, and Daang Remote is at least as usable for the kinds of work the founder actually does.
- The system's metadata exposure is small enough, and documented clearly enough, that a technically literate skeptic examining it would agree it materially improves on commercial alternatives.
- The cryptographic posture demonstrates cryptographic agility and a credible present-day post-quantum direction, and can be reviewed by someone qualified to assess that claim.
- External success metrics (adoption, retention, willingness-to-pay signals from individuals outside the founder) will be defined before the first public release, not invented now.

The founder should reconsider or discontinue Daang Remote if, after honest effort:

- He does not, in practice, prefer it to the commercial alternative for his own work.
- The metadata-minimization or cryptographic-agility properties cannot be maintained without making the product unusable.
- No individual outside the founder shows durable interest once the product is offered.
- Sustaining it would require compromises (data monetization, mandatory accounts on third-party identity providers, platform lock-in) that violate this charter or the Constitution.

## Constraints

- **Constitutional:** All work is bound by the Foundry Constitution, including the rules on AI authority, human review, doctrine change, and responsible use.
- **Privacy:** Metadata minimization is a hard constraint, not a marketing posture. Features that require collecting more metadata than the session itself needs must be justified explicitly or rejected.
- **Security:** Cryptographic agility is a hard architectural constraint on transport and identity primitives; the current engineering posture is post-quantum wherever practical and evidence-supported.
- **Platform independence:** No design decision may create a permanent dependency on a single operating system, app store, cloud provider, or third-party identity system.
- **Financial:** The product must be buildable and maintainable at the scale of a founder-led project before it is offered more widely; it must not require venture-scale spending to reach personal-use viability.
- **Ethical:** Daang Remote must not be designed, marketed, or documented in ways that make covert surveillance of another person easier than legitimate remote access to one's own machines.
- **Time:** The founder's own use is the first milestone. Broader release is explicitly deferred until that milestone is met.

## Risks

- **Founder-only fit:** The product may end up excellent for exactly one person and uninteresting to anyone else. Mitigation: name this risk now, treat single-user excellence as necessary but not sufficient, and test external interest before investing in scale.
- **Commercial success creates pressure to compromise the charter:** If Daang Remote gains traction, revenue, or user growth, that success itself will generate ongoing pressure to add analytics, mandatory accounts, growth-oriented features, platform-specific integrations, or data-monetized tiers that violate this charter. Mitigation: treat this pressure as a predictable and permanent condition rather than a surprise; any such change requires explicit doctrine-level review under the Constitution, not a routine product decision, and the charter is re-read whenever a commercially attractive shortcut is proposed.
- **Privacy erosion under pressure:** Commercial or operational pressure may push toward collecting more metadata, adding accounts, or integrating third-party analytics. Mitigation: the Constitution and this charter treat privacy as a hard constraint; any change requires explicit doctrine-level review.
- **Cryptographic misjudgment:** Getting post-quantum choices wrong, or mistaking agility for security, could produce a false sense of protection. Mitigation: treat cryptographic decisions as reviewable by qualified outsiders; do not present claims that have not been reviewed.
- **AI over-reach:** AI assistance could quietly expand into decisions that should remain human, or into features that require exfiltrating session content. Mitigation: AI usage is bound by the Constitution's authority rules and by this charter's privacy constraints.
- **Dual-use / misuse:** Any remote-access tool can, in principle, be used to spy on or control another person's computer. Mitigation: Daang Remote is scoped to access of one's own machines; features, documentation, and defaults must not make covert third-party surveillance easier than legitimate use.
- **Platform capture:** An operating system vendor, app store, or identity provider may attempt to force changes incompatible with this charter. Mitigation: platform independence is a design constraint from day one, not a later refactor.
- **Founder attention:** Daang Remote is one of several intended Daang products. Mitigation: it is explicitly first, and no other product is authorized to compete for attention until this one meets its personal-use success criteria.

## Constitutional principles this product depends on

- **Replaceable intelligence and platform independence:** Daang Remote must survive changes in AI models, frameworks, cloud providers, and operating systems.
- **Privacy and metadata minimization:** The product is a direct expression of this principle.
- **AI authority limits and human review:** AI assistance inside the product, and AI-generated changes to the product, are bound by the Constitution.
- **Doctrine vs policy:** Privacy, cryptographic agility with a present-day post-quantum posture, and platform independence are treated as doctrine here; changing them requires explicit founder approval, not a routine PR.
- **Responsible use:** The product must not be shaped into a tool whose easiest use is to harm others.
- **Founder-first sequencing (Foundry 0):** Personal-use excellence precedes external release; this charter formalizes that sequencing for Daang Remote specifically.

**Principles at unusual risk of drift for this product:**

- **Privacy and metadata minimization** — under any future pressure to add analytics, accounts, or third-party integrations.
- **Platform independence** — under pressure to adopt platform-specific identity, distribution, or payment systems that would be easier in the short term.
- **Scope discipline** — the temptation to absorb adjacent problems (sync, backup, VPN, password management) into Daang Remote instead of keeping them as separate future products.
- **Charter integrity under commercial success** — the temptation, once the product works, to trade small charter compromises for growth, revenue, or convenience.
