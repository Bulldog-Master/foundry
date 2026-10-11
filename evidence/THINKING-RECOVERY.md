# Parser recovery development record

Subject PR #26 head f949d06fa43581b8851b789e28d108b7da9950b5; sealed packet f1efc313cd27a05e84b85c48438137aae2ea8bcb32f4b7b10a928a3aeffebf8b.

Founder-reported attempt 1: transport COMPLETED, schema INVALID_MALFORMED, adverse_signal_scan NONE, provider blocks [thinking,text], rejected as unexpected provider content. No attempt evidence or sealed packet was read, rewritten, removed, rebuilt, or reclassified. Root-only custody remains inaccessible to this development account. Prior release source and all development evidence are preserved.

Parser accepts thinking and redacted_thinking as non-verdict envelope content. Only text is concatenated, scanned, parsed, and validated. Tool-use, unknown, non-object, malformed text, and textless envelopes reject. Raw provider bytes remain unchanged in attempt evidence. Model, stop reason, schema, binding, routing, retry accounting, custody, and publication rules remain intact.

Complete conformance passes. The runtime suite has 28 unique tests, including four new regressions; running compatibility entry points as well executes 84 passing tests. These producer-run offline checks are development evidence, not independent gate verdicts. No live provider request, attempt 2, verdict publication, PR merge, gate override, Foundry 2 activation, or automation was performed.

This separate source release is frozen by MANIFEST.sha256. Installation uses install-runtime.sh only, preserving credentials, packets, runs, and previous releases while refusing active automation. Installation must not seal another packet or invoke evaluation.
