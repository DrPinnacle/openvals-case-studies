# OpenVals Case Study 004 · LLM Reliability Under Meaning-Preserving Prompt Perturbations

**OpenVals — A DrPinnacle Initiative**  
**Evidence classification:** Controlled local-model experiment with an exploratory follow-up  
**Release date:** 13 November 2026

Does a model still choose the correct option when a question is paraphrased or reformatted? This study runs two locally installed Apache-licensed model builds, Qwen3-4B and Mistral, against 24 known-answer items. Each item has a baseline, a paraphrase, a layout variant, and two attempts per form. The package includes the original unconstrained pilot and a follow-up using schema-constrained JSON. The commercial hosted cohort was **not run**.

- [Technical report](reports/TECHNICAL_REPORT.md)
- [Executive brief](reports/ENTERPRISE_SUMMARY.md)
- [Methodology](METHODOLOGY.md) and [dataset card](DATASET_CARD.md)
- [Reproduction instructions](REPRODUCIBILITY.md) and [references](REFERENCES.md)
- [Machine-readable results](results/summary.json) and [cohort status](results/cohorts.json)

Raw JSONL and run manifests are in `results/<run>/`. Each raw record contains the exact transmitted prompt and model settings, request timing, and original response body when available. See [LICENSE.rtf](LICENSE.rtf) for study terms. Model weights are not distributed.
