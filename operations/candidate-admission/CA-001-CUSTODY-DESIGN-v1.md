# CA-001 separate custody design v1

- Status: DRAFT DESIGN ONLY — not approved, installed, commissioned or activated.
- Scope: one non-production CA-001 trial; no standing operation.
- Baseline: source revision `08a7efd46ea0ede5dd067e6eefb64dbcd1ee249f`.
- Final authority: Bulldog; independent review remains with the other chat.

## Decision proposed

Use a separate custodian-controlled Windows host with a dedicated WSL2 worker for CA-001. The custodian owns the capture process, frozen inputs and authoritative evidence. The producer must have no administrative authority over that host, its storage, hypervisor or recovery paths. The worker remains unprivileged and receives only the bound synthetic trial inputs.

Prefer the existing capture script and Python harness unchanged, with their current two-pass, 60-second and 1-MiB combined-output limits. This avoids a new ingestion service, network broker, sealer, signing mechanism or agent framework. It proposes a new isolated custody boundary, not changes to the working Foundry environments. No eligible host or identity is assumed to exist.

This design does not establish custody by itself. Installation, verified commissioning, final freeze, Stage B, admission and integration remain separate acts.

## Boundary and authority

| Role | Allowed | Not allowed |
| --- | --- | --- |
| Producer | Prepare candidate files and explanatory material in existing preparation workspaces | Administer the custody host; alter frozen inputs, capture code or authoritative records; hold custodian credentials; select which attempts are retained |
| Custodian | Verify and import the exact approved tuple; hold capture and evidence; run only separately authorized bounded operations | Produce an independent gate verdict by self-assessment; infer Stage B approval; grant standing authority |
| WSL worker | Run the frozen deterministic code under the approved isolation and bounds | Windows interop, controller storage, sudo, provider/network/credential/signing access or writes outside the disposable worker directory |
| Independent reviewer | Review the authorized bounded inputs under recorded ADR-0002 arrangements | Be assigned or have outcomes pre-completed by this design |

The capture process runs directly on the custodian-owned host. It must not accept a producer-uploaded transcript as the sole authoritative record or route capture through the producer-administered desktop. The custodian controls both invocation and collection, including failed, malformed, partial, timed-out and aborted attempts.

A new account, folder or VM on a host the producer can administer is insufficient. Verify host and hypervisor control, privileged groups/delegations, storage and backup access, recovery authority, ancestor replacement rights and any existing access paths. This is a scoped boundary assessment, not a claim of exhaustive compromise resistance.

## Reuse without changing existing integrations

The proposed host uses its own custodian-owned profile and dedicated `Foundry-Agent` WSL registration. Keeping the expected distribution name, worker identity and disposable work directory permits reuse of the existing capture and harness interfaces. The current desktop's WSL registration is not shared or remotely controlled for this trial.

Prefer unchanged copies of `Capture-CA001StageB.ps1` and `ca001_harness.py` from the baseline. Verify their exact hashes and the target's runtime, launcher and bwrap identity before proposing a final tuple. A matching distribution name is not identity or isolation proof. If unchanged reuse cannot satisfy the target checks, stop and show a separate minimal code diff; do not weaken directory checks or silently introduce a transport.

Do not export or clone the working WSL installation, account profiles, SSH keys, sessions, credentials, database contents or protected Foundry material. Any future worker provisioning is a separately approved, minimal non-production environment containing only approved system components and hash-bound CA-001 files. Availability, configuration, resource/cost bounds and exact provisioning changes remain unresolved.

Caller-1's sealer illustrates existing root-owned custody practice; it is not reused, modified or invoked. Caller-1 and Sandbox-1 remain frozen. Existing Standalone, Hermes, n8n, PostgreSQL, JEV, Valyu, Ollama, Ponytail and OpenCode integrations remain unchanged. The controller/Caller signing trust roots are neither accessed nor relocated.

## Proposed layout

Paths below are relative to a future custodian-owned profile, not an approved machine or concrete path:

- `Foundry-Control/pause-kill/STATE.txt`: local PAUSE guard for this custody environment only.
- `Foundry-Control/candidates/CA-001-v1/sources`: verified frozen sources, capture implementation and finalized prerequisite records.
- `Foundry-Control/candidates/CA-001-v1/evidence`: capture locks, consumed-authorization markers, preflight rejections and all attempt records.
- `/home/foundry-agent/work/candidate-admission/ca001-v1`: disposable worker copy only.

The current desktop's PAUSE state and preparation folders are not modified, superseded or relabeled as authoritative. An isolated custodian's local PAUSE guard does not become a new operational controller or signing trust root.

The custodian must control the directories, file ownership and relevant ancestors. The worker and producer cannot create, append, overwrite, truncate, delete, rename, replace, change ownership/ACLs or retain handles that bypass the freeze. Administrative/recovery access must remain outside producer control. Host-specific identities and permission entries are recorded privately before an exact installation diff is approved; no guessed SID, ACL command or installer is included here.

## Preservation and capture sequence proposed

1. The custodian imports only an explicitly approved inventory and recomputes each hash. Candidate material remains producer-authored input, not independent evidence.
2. Preserve the existing preparation inventory and failures byte-for-byte with original provenance. Importing them does not retrospectively make their producer-authored observations independently verified or frozen.
3. Finalize the revised evaluation packet, named roles, reviewer independence, independent expected-outcome confirmation, custody/environment records, review arrangements and exact commands. The other chat supplies independent inputs; this design does not generate them.
4. Record enforceable preservation of frozen inputs and all subsequent attempts under the custodian's authority. Specify retention and access limits before freeze. No retention duration, automatic deletion job or signing authority is adopted here.
5. Freeze exact source, capture, runtime, isolation, environment, command and prerequisite bindings. Keep final hashes outside the documents they hash. A resolved command containing the manifest hash cannot also be hashed back into that same manifest; bind the unexpanded template and record the resolved command hash externally.
6. Stop. The custodian launches neither candidate nor Stage A tests without separate exact-tuple Stage B approval. Only after that approval may the existing capture invoke exactly two bounded passes, recording raw bytes and every failure locally without producer selection or automatic retry.

A capture summary or successful hash comparison does not authenticate founder approval, prove custody, establish worker cleanup or replace gate review. Capture's existing `custody_verified=false` is not changed into an automatic PASS by this design.

## Exact future binding changes

This design-only patch adds this document and a non-executable binding template. It changes no current packet, source, manifest, controller or installed file.

Before installation or evaluation, a separate proposed revision must show:

| Artifact | Current preparation | Required proposed revision |
| --- | --- | --- |
| Evaluation packet sections 4, 5 and 8 | Existing Foundry-Agent environment; proposed controller custody | Dedicated custodian-controlled non-production host and worker; named operator/custodian; explicit access and verification limits |
| Evaluation packet section 9 and final manifest | Existing source pins with unresolved freeze prerequisites | New packet hash, privately verified host/runtime/capture/isolation bindings, custodian-owned roots and all finalized prerequisite hashes |
| Environment and custody records | Producer observations and pending acceptance | Actual target observations, access-boundary evidence, retention mechanism and separately recorded acceptance |
| Command template | Existing capture interface with unresolved final manifest hash | Exact target-local invocation and final hash, preserving all bounds and comparisons |
| Host provisioning proposal | No eligible host commissioned | Exact host/identity, approved software/runtime inventory, permissions, resource limits and inert verification plan; no effect on existing hosts |

The checker rules, twelve fixture cases, expected outcomes, eight unit-test methods, harness algorithm and acceptance criteria do not change. Candidate performance remains untested. Environment or capture drift requires a new recorded tuple and fresh authority, not inherited readiness.

The accompanying `CA-001-CUSTODY-BINDINGS-v1.template.json` deliberately uses a different record type from the executable Stage B manifest. It has no execution receipt and leaves every deployment/acceptance binding null and every authorization false. It is not a new validator, configuration API or automatic approval mechanism.

## Bounded acceptance checks proposed

After separate authorization to provision and perform inert checks:

- Verify the producer cannot administer or log into the custodian host or use its storage, hypervisor, recovery, task/delegation or credential paths. A filtered administrator token or unavailable key alone is not proof.
- Use disposable sentinels to check denial of create, append, overwrite, truncate, delete, rename, replace, owner and ACL changes through relevant producer/worker paths. Include ancestor replacement, inherited grants, reparse/symlink substitution and existing handles; never tamper-test real evidence.
- Verify the custodian can capture an inert command directly and retain successful, failed, timeout, malformed, oversized and aborted records without producer filtering. Check exact byte counts, raw-stream hashes and fail-closed behavior.
- Reconfirm the worker's identity, source/runtime hashes, isolation, no egress, controller-path invisibility and outside-write restriction. Verify cleanup within the declared scope; Windows client termination alone is not proof.
- Record identities, methods, raw observations, expected/actual outcomes and limitations for each check. Negative probes are scoped evidence, not a universal isolation certificate.

These checks do not import the checker or execute its Stage A tests or Stage B. No check in this list has been run by preparing this design. Prior WSL warnings and all original failures remain in the historical preparation record and must not be erased or used as proof of a new host's health.

## Approvals and stop conditions

The next authority decision is acceptance of this design direction, not permission to install it. An exact target-specific provisioning/implementation diff, custody verification and acceptance, final freeze and separately bounded Stage B approval are still required. Independent review and four-gate outcomes remain with the other chat. Post-evaluation outcomes are required before admission, not manufactured as pre-execution evidence.

Keep existing authority boundaries for new identities/credentials, trust changes, publication, signing, merge and production. No provider, paid resource, unattended service or standing operation is authorized. No host has been selected or purchased.

On missing independence, unexpected administrative access, unsupported capture reuse, source/environment drift or failed preservation, defer and retain the failure. Before freeze, abandon a failed proposal without deleting history. After freeze, stop new work and preserve inputs, logs and consumed-attempt markers; do not roll back by restoring producer write access or erasing failed attempts.

## Governing references

- Candidate Admission Protocol v0.1, sections 2–6.
- CA-001 Evaluation Packet v1, sections 4–10; its existing hash remains unchanged by this patch.
- ADR-0002, Decisions 1–5.
- Caller Production Contract v1 and Sandbox-1 Production Baseline v1, unchanged and excluded.
