# OpenVals Case Study 001 — Evaluating the Evaluator

**LLM-as-a-Judge Reliability: Position Bias, Verbosity Bias and Critical-Case Detection**  
**OpenVals — A DrPinnacle Initiative**  
**Author:** Vishwanath Akuthota — Founder of DrPinnacle, OpenVals and The Foundry's  
**Positioning:** Engineering AI Trust. Measuring Enterprise Value.

## Status and scientific integrity

**Version 1.0 — reproducible synthetic proof of concept.** This study **does not** execute a real LLM, integrate with a live OpenVals service, or establish empirical product performance. It demonstrates how an evaluation protocol can reveal presentation-induced judging errors under explicitly programmed assumptions. No customer incidents, commercial results, or real-world accuracy claims are asserted.

## Research questions

1. Can a synthetic evaluator prefer an expert-labelled incorrect response due to response length?
2. Does swapping the order of responses change the chosen winner?
3. How do these effects influence agreement with reference expert labels and critical-case false approvals?

## Quick start

Requires **Python 3.10+** and no external dependencies.

```bash
python3 case-studies/001-llm-judge-reliability/experiment.py --output reports/results.json
python3 -m unittest discover -s tests -v
```

The script prints a JSON summary and writes the same report to the specified path. The report is generated, not a measured result from OpenVals or a commercial model.

## Repository map

- `case-studies/001-llm-judge-reliability/experiment.py`: deterministic synthetic judge and metrics
- `case-studies/001-llm-judge-reliability/test_cases.json`: expert-labelled synthetic IT support pairs
- `tests/test_case001.py`: regression tests
- `docs/methodology.md`: formal protocol, definitions, limitations, extension plan
- `docs/enterprise-brief.md`: executive interpretation and pilot criteria
- `reports/results.json`: output from running the script
- `reports/OpenVals_Case_Study_001.pdf`: printable research brief
- `reports/OpenVals_Case_Study_001.docx`: editable research brief

## Research-to-product roadmap

Replace the synthetic judge with a **version-pinned** LLM judge adapter and separately validate integration with OpenVals. Introduce blinded domain-expert labels, balanced answer ordering, confidence intervals, safety-severity strata, immutable manifests and prespecified acceptance thresholds. Only then make empirical claims.

## Licensing

Code: MIT (`LICENSE`). Dataset: synthetic examples written for this demonstration; see `DATASET_CARD.md`. Not a certification or guarantee of safety.
