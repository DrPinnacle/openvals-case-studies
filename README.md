<div align="center">

# OpenVals Case Studies

### Reproducible AI Evaluation, LLM Validation & Enterprise AI Assurance Research

**Engineering AI Trust. Measuring Enterprise Value.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/Code%20License-MIT-green.svg)](LICENSE)
[![Research Status](https://img.shields.io/badge/Research-Synthetic%20PoC-orange)](case-studies/001-llm-judge-reliability/)
[![Organization](https://img.shields.io/badge/Organization-DrPinnacle-172554)](https://github.com/DrPinnacle)

**OpenVals — A DrPinnacle Initiative**  
**Author:** Vishwanath Akuthota — Founder of DrPinnacle, OpenVals and The Foundry's

[Explore Case Study 001](#featured-case-study-001--evaluating-the-evaluator) · [Quick Start](#quick-start) · [Methodology](docs/methodology.md) · [Enterprise Brief](docs/enterprise-brief.md) · [Contribute](CONTRIBUTING.md)

</div>

---

## Overview

**OpenVals Case Studies** is a public research repository for reproducible experiments in **AI model evaluation**, **large language model (LLM) validation**, **LLM-as-a-Judge reliability**, **AI benchmarking**, **critical-case detection**, and **enterprise AI assurance**.

The goal is to turn questions about AI quality, reliability, and trust into explicit research protocols with inspectable datasets, runnable code, documented metrics, and clearly stated limitations.

This repository complements the [OpenVals core project](https://github.com/vishwanathakuthota/openvals). Case studies are evidence-building exercises; they are **not** automatically demonstrations of production OpenVals capabilities.

## Why AI Evaluation Needs Evaluation

An AI system may generate a fluent answer that is incorrect, unsafe, or unsuitable for an enterprise workflow. The evaluation system used to assess that answer can also introduce errors. For example, an LLM judge may be influenced by **response order** or **verbosity**, rather than the correctness of the underlying response.

A credible enterprise evaluation process should examine not just *what an AI model answered*, but also *whether the evaluator's decision is reliable*. This repository explores such questions through controlled experiments, transparent assumptions, and reproducible artifacts.

## Featured Case Study 001 — Evaluating the Evaluator

### LLM-as-a-Judge Reliability: Position Bias, Verbosity Bias & Critical-Case Detection

**Research question:** Can presentation features change a judge's preference even when an author-defined reference label favors a different answer?

| Dimension | What the study examines |
| --- | --- |
| **Position bias** | Whether swapping answer order changes the selected response |
| **Verbosity bias** | Whether response length can influence preference |
| **Reference-label agreement** | How often decisions match author-assigned preferred responses |
| **Incorrect approval rate** | How often a non-preferred response is selected |
| **Critical-case analysis** | How the protocol treats synthetically designated higher-severity cases |
| **Reproducibility** | Whether the deterministic experiment and tests can be rerun |

**Evidence level: synthetic proof of concept.** Version 1.0 uses **six synthetic IT-support cases** (12 candidate responses) and a **programmed simulated judge**. It does **not** call a real LLM, establish human-expert agreement, evaluate a deployed customer system, or measure production OpenVals performance. The reference labels are author-assigned, not independently adjudicated by domain experts.

**Read the materials:**

- [Experiment and dataset](case-studies/001-llm-judge-reliability/)
- [Detailed research methodology](docs/methodology.md)
- [Dataset card and limitations](DATASET_CARD.md)
- [Enterprise interpretation and pilot criteria](docs/enterprise-brief.md)
- [Printable research report (PDF)](reports/OpenVals_Case_Study_001.pdf)
- [Editable research report (Word)](reports/OpenVals_Case_Study_001.docx)
- [Example generated results (JSON)](reports/results.json)

> **Scientific integrity:** Synthetic results illustrate how a test protocol behaves under programmed assumptions. They must not be presented as measured detection rates, risk reductions, ROI, or validated OpenVals product claims.

## Quick Start

**Requirements:** Python 3.10+; no external dependencies for Case Study 001.

```bash
git clone https://github.com/DrPinnacle/openvals-case-studies.git
cd openvals-case-studies

# Run the deterministic demonstration and generate its JSON report
python3 case-studies/001-llm-judge-reliability/experiment.py --output reports/results.json

# Run the regression tests
python3 -m unittest discover -s tests -v
```

The experiment prints a JSON summary and writes the requested output file. Re-running it should reproduce the same deterministic outputs for the same code and dataset. Inspect the [methodology](docs/methodology.md) before interpreting metrics.

## Repository Structure

```text
openvals-case-studies/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── DATASET_CARD.md
├── case-studies/
│   └── 001-llm-judge-reliability/
│       ├── experiment.py
│       └── test_cases.json
├── docs/
│   ├── methodology.md
│   └── enterprise-brief.md
├── reports/
│   ├── results.json
│   ├── OpenVals_Case_Study_001.pdf
│   └── OpenVals_Case_Study_001.docx
└── tests/
    └── test_case001.py
```

## Research Principles

1. **Reproducibility first:** Publish runnable methods, input provenance, and enough configuration detail to replicate the analysis.
2. **Separate evidence from aspiration:** Label synthetic simulations, prototypes, real-model experiments, and independently validated findings distinctly.
3. **Evaluate the evaluator:** Test sensitivity to ordering, presentation, rubric changes, and disagreement with trusted references.
4. **Report failure modes:** Include incorrect approvals, missed critical cases, uncertainty, and study limitations—not only aggregate scores.
5. **Protect enterprise data:** Do not commit secrets, customer data, or restricted materials without explicit authorization.

## Roadmap (Proposed — Not Yet Implemented)

- **Case Study 002:** Critical-case detection and false-negative analysis
- **Case Study 003:** Prompt injection and adversarial resilience evaluation
- **Case Study 004:** Enterprise AI reliability and consistency testing
- **Case Study 005:** AI model benchmarking across quality, latency, and cost

Future real-model experiments should pin model and evaluator versions, define rubrics before testing, obtain blinded domain-expert annotations, balance answer order, report confidence intervals, and preserve run manifests. Integration with the live OpenVals evaluation engine remains a separate validation milestone.

## Who This Repository Is For

AI/ML engineers, evaluation researchers, enterprise architects, AI governance and risk teams, CIOs, CTOs, CAIOs, CISOs, and organizations designing evidence-based AI deployment gates.

## Contributing

Contributions that improve experimental design, documentation, datasets, testing, or reproducibility are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. For research questions or proposed case studies, use the repository's **Issues** tab.

## License & Responsible Use

Source code is provided under the [MIT License](LICENSE). See [DATASET_CARD.md](DATASET_CARD.md) for synthetic dataset provenance and usage limitations. The reports are research materials; this repository does not provide AI safety certification, regulatory compliance assurance, or performance guarantees.

## Project Links

- **Case studies:** [DrPinnacle/openvals-case-studies](https://github.com/DrPinnacle/openvals-case-studies)
- **OpenVals core:** [vishwanathakuthota/openvals](https://github.com/vishwanathakuthota/openvals)
- **DrPinnacle organization:** [github.com/DrPinnacle](https://github.com/DrPinnacle)

---

<div align="center">

**OpenVals — Engineering AI Trust. Measuring Enterprise Value.**  
*A DrPinnacle Initiative*

</div>
