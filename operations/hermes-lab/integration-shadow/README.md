# Hermes/Ollama probe and advisory routing candidates

**Status:** Development candidate only. Founder has directed Hermes and Ollama integration; this does not mean standing agent framework adoption or authority delegation is commissioned.

Scope: a Hermes executable-presence/local catalog probe, an inert backend router, and a synthetic Jev advisory validator for the existing Standalone lab. The candidates do not invoke models, read normal Hermes state, dispatch tasks, write GitHub, appoint evaluators or grant authority. Live Hermes/Ollama state has not been verified here. The Jevinik installer and install guide are split into a separate draft candidate and are not part of this PR.

| File | Role |
| --- | --- |
| `probe.py` | PATH presence check and fixed-loopback catalog request; optional diagnostic file output |
| `router.py` | Backend proposal from caller-supplied task and availability data |
| `jev_shadow.py` | Advisory validation of synthetic evidence/decision data |
| `JEV-CANDIDATE.md` | Unverified upstream references and proposed bounded test design |
| `test_probe.py` | Seven fixture tests, including in-memory HTTP handlers |
| `test_router.py` | Thirteen fixture tests, including malformed input handling |
| `test_jev_shadow.py` | Fourteen synthetic validator tests |
| `README.md` | Candidate scope, limits and review boundary |

All 34 tests are offline fixtures, with injected fake openers, binary lookups or in-memory HTTP responses. They are not Standalone runtime evidence. The probe uses a fixed `127.0.0.1` endpoint, disables environment proxies and refuses redirects. A `reachable` result means only that the listener returned an object with a `models` list; it does not establish service identity or version. Model names are unvalidated strings, with no character or byte-length guarantee.

Fixture-test command:
```
python3 -m unittest discover -p 'test_*.py' -v
```

Any live `python3 probe.py` execution requires its separately authorized host envelope and unprivileged identity. The probe emits diagnostic JSON to stdout by default. Optional `--output` allows an exclusive new file immediately under `/srv/hermes-lab/foundry-agent`; directory-ancestor identity and ownership are not verified by that lexical check. The producer's own output is diagnostic, **not independent custody**.

Model names and Hermes presence belong in private execution records under `operations/hermes-lab.md`. Do not paste probe output into GitHub issues or PRs. Before live use, response-size limits, name handling, PATH/actor checks and output-directory protections must be reviewed in the concrete execution envelope.

Next after actual source verification: inspect Hermes documented CLI in its existing approved lab path, establish a disposable HERMES_HOME and independently observed read-only shadow planning task. Windows execution/PAUSE/KILL behaviour is reported, not verified here; the merged program-state record governs controller location and authority. No proposal becomes authority by prose alone. Candidate Admission and applicable activation gates apply before a standing operational role.

Issue: #36. No installation/promotion implied.

## Disposable native recovery follow-up

The [2026-10-21 producer record](RECOVERY-RESULTS-2026-10-21.md) retains the
original restart response-contract failure and the successful bounded follow-up.
`recovery_contract.py` and `test_recovery_contract.py` export the clarified
synthetic proposal policy and offline regression checks; they add no live calls,
standing operation, controller authority or integration/configuration changes.
Earlier verification statements above describe the original offline candidates,
not a claim that these later private native-worker checks did not occur.
Independent review remains separate; no gate outcome or activation is inferred.
