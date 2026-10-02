# Run-009 Integrity Record

## Status

Run-009 dual-model pilot execution is **INVALID** under the frozen
preregistration.

No PROMISING, INCONCLUSIVE, or FAIL performance classification is assigned.

Existing Run-009 outputs are quarantined as exploratory / diagnostic evidence
only.

## Independent invalidation reasons

### 1. Evaluator substitution after freeze

The frozen dual-model pilot named Codex and Claude as the two evaluators.

Codex solo evaluation completed and its results became visible before the
second evaluator substitution was frozen.

Claude was subsequently replaced by DeepSeek-R1 8B.

The preregistration freeze condition states that after any solo evaluator
result becomes visible to anyone involved in design or execution, changes to
the protocol must not be retroactively applied to the same pilot.

The Claude-to-DeepSeek substitution therefore independently invalidates this
execution.

The original cost criterion also remained defined against solo-Claude and was
not validly redefined by the later substitution.

### 2. Malformed required cross-critique output

DeepSeek R-08 cross-critique produced analysis but no explicit PASS, FAIL, or
ABSTAIN verdicts for any of the four gates.

The frozen protocol required post-cross-critique verdicts for fusion.

No preregistered rule authorized inference from prose, silent carry-forward of
first-pass verdicts, or retrospective replacement.

### 3. Runtime drift during scored cross-critique

DeepSeek scored execution did not remain under one equivalent frozen runtime.

Earlier execution used:

- NVIDIA driver 595.91.07
- CUDA 13.2
- Ollama context length 65536

Following repeated GPU/CUDA failures, later scored cross-critique execution
used:

- NVIDIA driver 580.178.04
- CUDA 13.0
- Ollama context length 49152

The failed attempts were preserved as evidence, but exact runtime/configuration
equivalence was lost.

## Sealed-truth custody and recoverability finding

The complete authoritative 24-candidate × four-gate adjudication matrix was
not recoverable at final reporting time.

The execution harness did not hard-enforce, before evaluator execution:

- an immutable sealed-truth storage location;
- an authoritative artifact identifier;
- a recorded SHA-256 tied to that exact artifact;
- an independent recovery copy;
- a verified restore procedure;
- a write-authority / chain-of-custody record;
- proof of who could modify, replace, suppress, or delete the sealed artifact;
- fail-closed verification that a recovered artifact matched the expected hash.

Truth-dependent metrics must remain unavailable rather than being reconstructed
from evaluator outputs, remembered examples, or post-exposure inference.

## Frozen local evidence

Standalone evidence root:

`/srv/hermes-lab/evidence/run009-pilot/`

Recorded SHA-256 values:

- Codex solo first-pass ledger:
  `201ea541b0bf0f325bfe126974ddffeb7540224857958d5580d91be97f34eacc`
- DeepSeek solo first-pass ledger:
  `66b76064ea876c469fa3741b7a3d643ff20dde67f7b57da0e9faf9c016ff44e3`
- First-pass disagreement matrix:
  `b4c284b32db55ac1ca938264b7c85d88c25772447f007e7a98291c577bd258f2`
- Cross-critique artifact manifest:
  `281a45c32b3b439184253eddc6154e3222aac2bfb380590b064069b40c82898d`
- Codex post-cross-critique ledger:
  `6286701fd655e34ac850e10a753e3aba496161e2d7874474c3d2bf17e64d2d60`
- DeepSeek post-cross-critique ledger:
  `ccd5294dcfd6cc76e175890d02bc9a61315fac63d9d108c99d87600a1c85b43a`
- Post-cross-critique extraction audit:
  `7a58e68a0371af02232693525e5a46d57e6c5b6dc00acd36bc4b9fd3d74996d0`
- Original integrity finding:
  `9d4683f93fb1a489141ca4e9d5e22dae63419e4a99c2a7da474f6ce6fa82de57`
- Final report:
  `bf88e6aa8499b02e3a2f8aa09a72104b3cf3c9edd6d9f185bfe20f6879ce067e`
- Integrity addendum:
  `5c34a846012e2881cee6ab021e19b19ad13d3ec4d16a7e8604c1f0f5f729d1a3`

## Quarantine rule

Run-009 outputs may be retained for exploratory and diagnostic use.

They must not support:

- a performance classification;
- evaluator-superiority claims;
- architectural adoption;
- permanent evaluator assignment;
- production-policy changes.

## Required next stage

No replication is authorized until:

1. Every frozen protocol requirement is mapped to an enforcement mechanism,
   deterministic human checkpoint, or explicitly accepted unenforceable
   assumption.
2. That requirements-to-enforcement matrix receives an independent review.
3. Every identified red or yellow gap is repaired.
4. A fail-closed pilot-execution preflight checker is in place.
5. Sealed-truth custody, backup, recovery, and hash matching are verified.
6. One evaluator runtime is frozen before scored execution.
7. Evaluator output schema is validated immediately after every invocation.
8. Synthetic non-scored plumbing tests pass before real replication begins.

## Foundry 1 scope

Any automated preflight or abort tooling introduced for this work is
**pilot-execution harness infrastructure**.

It does not redefine Foundry 1's standing four-gate review process as automated
gate enforcement.

Any broader automation of Foundry governance requires separate authorization.
