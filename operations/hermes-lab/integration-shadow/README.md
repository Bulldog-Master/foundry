# Hermes + Ollama: initial Standalone shadow probe

**Status:** Development candidate only. Founder has directed Hermes and Ollama integration; this does not mean standing agent framework adoption or authority delegation is commissioned.

Scope: existing `foundry-agent` user on Standalone, read-only discovery of Hermes executable presence and Ollama localhost model catalog. No secret readings, inherited HERMES_HOME, provider calls, arbitrary commands, GitHub writes, evaluator exposure, privileged access or production mutation. No claims about actual Hermes runtime behavior are made until the live preflight is observed.

Run as unprivileged `foundry-agent` in its existing approved Standalone lab workspace:
```
python3 -m unittest discover -p 'test_*.py' -v
python3 probe.py
```
The probe emits only sanitized JSON to stdout by default. Optional `--output` allows an exclusive new file immediately under `/srv/hermes-lab/foundry-agent`. The producer's own output is diagnostic, **not independent custody**.

Next after actual source verification: inspect Hermes documented CLI in its existing approved lab path, establish a disposable HERMES_HOME and independently observed read-only shadow planning task. The Windows controller retains execution/PAUSE/KILL; no plan can become authority by prose alone. Candidate Admission and any relevant frozen activation gates apply before a standing operational role.

Issue: #36. No installation/promotion implied.
