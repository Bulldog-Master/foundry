# Runtime release status

This separate runtime branch is a prepared, offline-tested BOOTSTRAP administrative release. It is outside PR #26. It is not Foundry 2 commissioning acceptance or activation and grants no merge or override authority.

Pinned subject: PR #26, head `f949d06fa43581b8851b789e28d108b7da9950b5`, governing main `4c2c611b61a1947bef409e5357f5426703bca452`. Amendment 0001 is checked at the governing base against `c74befb7587c866cffb06f9214b4c4ec5434395dcdbf99ca4dc725f5a5352d60`. Its ratification resolves the review-record interpretation only.

`install-and-seal-pr26.sh` installs a manifest-verified, root-owned release, runs offline conformance and regression tests in its pinned venv, and seals the exact PR packet. It does not invoke Claude, publish a verdict, enable the timer, merge PR #26, or activate Foundry 2. If base/head moved, installation can complete but sealing refuses; all existing and failed evidence remains. Repeating the same seal reuses the accepted packet for that base, head, and runtime release.

The final root-custodied packet is not yet created by this development session. The checked exact-commit packet is a developer fixture, never authoritative evaluation or commissioning evidence. Live provider transmission and App publication have not been exercised by this release; the mocked transports establish offline behavior only.

Git 2.53.0 is mandatory. Python must support venv; the installer provisions Debian/Ubuntu python3-venv when absent and installs exact Python dependency versions in its own venv. Provider and App credentials are preserved. Runtime failures, transport bytes, malformed outputs, all invocation attempts, staging failures, and uncertain publication journals are append-preserved. No retention deletion job is enabled.
