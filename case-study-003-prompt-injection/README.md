# OpenVals Case Study 003 — Prompt-Injection Resilience
Powered by Dr.Pinnacle

## Abstract and evidence status

This reproducible offline study illustrates how to measure instruction-boundary failures alongside task utility. It uses 36 author-created catalog-color tasks, harmless canary strings, and three deterministic policies. **Published results are synthetic simulation, not empirical LLM evidence.** No AI provider, OpenVals engine, RedShield, network tool, or production system is executed. The boundary oracle is an engineered upper bound, not a demonstrated LLM defense.

The simulated keyword filter emits the attack canary on 6/24 attack cases and answers only 6/12 benign cases correctly. These outcomes follow from code written for this illustration. They establish neither model resilience nor enterprise security effectiveness.

## Run in under a minute

Python 3.10+; standard library only. From the repository root:

```bash
python3 case-study-003-prompt-injection/benchmark.py
python3 -m unittest discover -s case-study-003-prompt-injection/tests -v
python3 scripts/check_links.py
```

The first command regenerates [results/simulation.json](results/simulation.json). It contains every response, per-family metrics, input and harness SHA-256 hashes, evidence class, and Python version. No installation, credentials, or paid calls are needed. Results are deterministic; Python version metadata may differ.

## Publication materials

- [Technical report](reports/TECHNICAL_REPORT.md): findings, interpretation, limitations.
- [Enterprise summary](reports/ENTERPRISE_SUMMARY.md): decisions and a proposed pilot.
- [Methodology](METHODOLOGY.md): threat model, controls, metrics and empirical extension.
- [Dataset card](DATASET_CARD.md) and [safe synthetic cases](data/cases.json).
- [Reproducibility and real-model response protocol](REPRODUCIBILITY.md).
- [References](REFERENCES.md), [license terms](LICENSE.txt), [licensing scope](NOTICE.md).
- [Runnable harness](benchmark.py), [tests](tests/test_benchmark.py), [published case-level output](results/simulation.json).

## Scope of claims

The harness demonstrates a measurement workflow and a constructed safety–utility tradeoff. Literal marker emission is a narrow proxy for attack success. A missing marker is not proof that an answer is safe. The fixture set has six highly related task groups, no independent held-out test, and no statistical generalization. No real-model results are included. External response import is supported but self-reported provenance is not independently authenticated.

This is standalone research under the OpenVals collection. Actual OpenVals integration remains future work. Retain evidence labels when quoting results.

## Citation

DrPinnacle. (2026). *OpenVals Case Study 003: Prompt-Injection Resilience*, version 1.0. Repository: https://github.com/DrPinnacle/openvals-case-studies (folder `case-study-003-prompt-injection`). Cite the publication commit once pushed.
