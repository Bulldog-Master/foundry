# Jev + Valyu pattern: admission candidate (synthetic only)

Bulldog requested incorporating the Jevinik evidence-first and typed-decision approach into Foundry's Hermes/Ollama/Codex work. This does **not** authorize stock trading, financial recommendations, provider credentials, runtime deployment, new egress or reserved gate routing.

## Verified integration references
- Jevinik demonstration source: https://github.com/unicodeveloper/jevocks
- Vercel Jev model and published AI SDK API: https://vercel.com/ai-gateway/models/jev
- Interface: `experimental_evaluate({model:"typesafe-ai/jev",state,questions})`; typed choice/score/boolean outcomes, experimental API. Jevinik uses five parallel **Valyu** evidence classes for its financial example. The demo's latency and predictive statistics **are not Foundry benchmarks**.

## Foundry test design
1. Start with *non-sensitive synthetic Foundry work items*, not stock tickers or sealed evaluator material.
2. Separate external evidence acquisition, provenance/freshness checking, typed Jev evaluation and controller action. The Jev decision is a signal, **never a command**.
3. Keep existing Hermes→ChatGPT/Codex backend and Ollama reference configuration unchanged. Map Jev results to diagnostic triage only during shadow testing.
4. `jev_shadow.py` rejects malformed evidence, stale/future capture, missing provenance, unknown categories, out-of-range probabilities and action-like decisions. It has no network/provider/tool invocation. `test_jev_shadow.py` supplies ten synthetic cases.
5. After independent candidate review, decide whether to test Jev's real provider API in an expressly authorized disposable environment and under an approved credential and cost boundary. Separately consider whether Valyu adds *relevant* evidence for a specific Foundry domain. Financial data retrieval is not generally required for Foundry control-plane work.
6. Measure evidence retrieval time, Jev decision latency, cost, disagreement with declared truth labels and false acceptance / missing-evidence rates. Do not benchmark Jev vs LLM using model agreement as truth. No production activation or merger from this draft.

The current protocol at `operations/candidate-admission/PROTOCOL-v0.1.md` remains draft and specifies version-bound evidence and stopping before integration. This packet is exploratory, pending exact-live-interface verification and bounded commissioning.
