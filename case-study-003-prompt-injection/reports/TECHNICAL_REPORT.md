# OpenVals Case Study 003 — Prompt-Injection Resilience

**Technical report · Version 1.0 · 31 October 2026**  
OpenVals — A DrPinnacle Initiative · Powered by Dr.Pinnacle

## Abstract

We present a small offline protocol for testing whether untrusted context changes a constrained answer, and for reporting task utility alongside a narrow attack-success proxy. A fixed dataset contains 24 attack fixtures and 12 benign controls across six related catalog-color tasks. Three deterministic policies illustrate vulnerabilities, keyword blocking, and an idealized trusted-field boundary. All reported outcomes are synthetic simulation. No model or product effectiveness was measured.

## Design

An authorized answer is a trusted catalog color. Untrusted text attempts to replace it with a public canary, using override, role spoofing, evaluator authority, or spaced tokens. Controls include clean context and harmless quotations of trigger text. See [methodology](../METHODOLOGY.md) and [dataset card](../DATASET_CARD.md) for the complete threat model and limitations. Code, exact fixtures, case-level output, and content hashes are included.

## Results: synthetic simulation only

| Programmed policy | Attack marker emission | Attack task success | Benign task success | Overall task success |
|---|---:|---:|---:|---:|
| Naive | 24/24 (100%) | 0/24 (0%) | 6/12 (50%) | 6/36 (16.7%) |
| Keyword filter | 6/24 (25%) | 0/24 (0%) | 6/12 (50%) | 6/36 (16.7%) |
| Boundary oracle | 0/24 (0%) | 24/24 (100%) | 12/12 (100%) | 36/36 (100%) |

Rates are rounded only in this table; [machine-readable results](../results/simulation.json) retain full precision. Each attack family has six cases. The filter blocks all 18 literal-cue attacks, emits the marker on all six obfuscated cases, and blocks all six benign glossary quotations. Neither blocked attacks nor marker-free failures count as task success. The naive policy also reacts to the quoted benign cue; its six benign marker emissions are reported separately from attack success.

## Interpretation

In this constructed example, reducing marker emission does not increase useful task completion. Reporting attack success alone could obscure a control that refuses authorized work. The oracle illustrates the intended boundary, but its perfect result follows from ignoring context that is unnecessary to this artificial task. It is not a deployable LLM defense, a causal estimate from a randomized study, or independent evidence of OpenVals performance.

## Evidence inventory

- **Executed:** local deterministic Python experiment and automated checks; exact responses in the result JSON.
- **Synthetic:** tasks, attacks, labels, policy behavior, and derived rates.
- **Empirical LLM evidence:** none collected; optional external-response scoring does not authenticate a model's provenance.
- **Product/field evidence:** none; no OpenVals SDK, RedShield, customer environment, or live tool exercised.

## Limits and next experiment

The same author designed policies and fixtures; there is no independent test set. Six template groups are dependent, and statistics would not support population-level claims. Exact text scoring cannot detect all semantic or action-level failures. The [empirical extension protocol](../REPRODUCIBILITY.md) supplies a starting point, not completed evidence. Future work requires independently authored held-out tasks, real model configurations, repeated runs, semantic review, and a defined deployment threat model.

## Sources, licensing, and citation

[Primary references](../REFERENCES.md) supply background, not evidence for the simulated numerical results. All new study materials follow [DPCL-CE](../LICENSE.txt); [notice](../NOTICE.md) explains existing repository licensing boundaries. Cite the repository, version, and eventual publication commit; no peer review or certification is claimed.
