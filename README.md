<div align="center">

# OpenVals Case Studies

### Reproducible AI Evaluation, LLM Validation, Cybersecurity Research & Enterprise AI Assurance

**Engineering AI Trust. Measuring Enterprise Value.**

[![Organization](https://img.shields.io/badge/Organization-DrPinnacle-172554)](https://github.com/DrPinnacle)
[![Research](https://img.shields.io/badge/Focus-Evidence--Driven%20Research-0F766E)](#research-standards)
[![Case Studies](https://img.shields.io/badge/Case%20Studies-001%20%7C%20002-2563EB)](#case-study-index)
[![Contributions](https://img.shields.io/badge/Contributions-Welcome-64748B)](CONTRIBUTING.md)

**OpenVals — A DrPinnacle Initiative**  
**Research lead:** Vishwanath Akuthota — Founder of DrPinnacle, OpenVals and The Foundry's

[Case Studies](#case-study-index) · [Research Standards](#research-standards) · [Getting Started](#getting-started) · [Contributing](#contributing) · [OpenVals Core](https://github.com/vishwanathakuthota/openvals)

</div>

---

## About This Repository

**OpenVals Case Studies** is an evolving, publicly accessible research collection exploring **AI model evaluation, LLM evaluation and validation, AI benchmarking, agentic AI assurance, AI safety, cybersecurity failure analysis, and enterprise AI governance**.

Our objective is to turn real-world incidents, research questions, and operational AI risks into **testable hypotheses, transparent methods, inspectable evidence, and practical enterprise lessons**. Each case study is independently scoped; not every study uses the same dataset, programming language, experiment design, or level of empirical validation.

This repository complements the [OpenVals core project](https://github.com/vishwanathakuthota/openvals). **Publication here does not by itself demonstrate that OpenVals detected, prevented, or mitigated a reported incident.** Product-specific claims must be supported by actual, documented integrations and experiments.

## Why This Research Matters

AI systems can fail in ways that conventional benchmarks miss: unreliable evaluation judgments, missed high-severity cases, adversarial inputs, insecure integrations, data leakage, and brittle operational controls. Likewise, cybersecurity incidents can expose gaps in the assumptions underlying AI-enabled workflows.

OpenVals research examines **what failed, how to measure it, what evidence is available, and what organizations can validate before deployment**. We distinguish historical incident analysis from controlled experiments, simulations, and independently verified product results.

## Case Study Index

> **Living index:** Add one row for every newly published study. Keep case-study identifiers stable; use version numbers within each study when its findings evolve. A study's folder README is the source of truth for its methods, evidence, and execution instructions.

| ID | Case study | Research area | Evidence / scope | Materials |
|:--|:--|:--|:--|:--|
| **001** | **Evaluating the Evaluator — LLM-as-a-Judge Reliability** | LLM evaluation, position bias, verbosity bias, incorrect approvals | Synthetic deterministic demonstration; not a real-model or production benchmark | [Study 001](case-studies/001-llm-judge-reliability/) |
| **002** | **PHP2Shell — Security Incident Analysis** | Cybersecurity, exploit analysis, enterprise assurance | Consult the study's own documentation for verified facts, methodology, and any OpenVals-specific tests | [Study 002](PHP2Shell_Case_Study_002/) |

**Future studies:** New research will be listed here **only when published**. Planned work and proposed experiments should be tracked through [Issues](https://github.com/DrPinnacle/openvals-case-studies/issues) rather than represented as completed findings.

### Case Study 001 · LLM-as-a-Judge Reliability

Explores how simulated evaluator preferences can affect response selection, including **position bias**, **verbosity bias**, and disagreement with author-assigned reference labels. Its initial evidence is **synthetic**: it does not establish the behavior of a real LLM judge or the measured performance of the OpenVals platform.

[Open Case Study 001](case-studies/001-llm-judge-reliability/) · [Dataset card](DATASET_CARD.md) · [Methodology](docs/methodology.md)

### Case Study 002 · PHP2Shell

A cybersecurity-focused case study published under `PHP2Shell_Case_Study_002`. Read its primary materials to distinguish **reported incident facts**, **technical hypotheses**, **reproduced observations**, and **potential OpenVals × RedShield assurance applications**. The existence of an incident case study is not evidence that OpenVals detected the exploit.

[Open Case Study 002](PHP2Shell_Case_Study_002/)

## Getting Started

Clone the research repository:

```bash
git clone https://github.com/DrPinnacle/openvals-case-studies.git
cd openvals-case-studies
```

Choose a case study from the [index](#case-study-index) and follow **that study's README** for prerequisites, datasets, commands, and reproducibility instructions. Different studies may require different tools or have no executable code.

For Case Study 001, see its documented experiment and test commands before running; do not assume commands or dependencies are shared across studies.

## Repository Organization

The repository is a **collection of independent studies**, not a single application. Existing and future folders may differ in structure:

```text
openvals-case-studies/
├── README.md                         # This living index and repository charter
├── CONTRIBUTING.md                   # Contribution guidance (where present)
├── case-studies/
│   └── 001-llm-judge-reliability/    # Case Study 001
├── PHP2Shell_Case_Study_002/         # Case Study 002
├── docs/                             # Shared methods and guidance (where present)
├── reports/                          # Published research outputs (where present)
└── tests/                            # Shared automated checks (where present)
```

**Recommended convention for each new study** (not a claim that all existing studies already follow it):

```text
<CASE_ID>-<short-slug>/
├── README.md             # Abstract, research questions, evidence status
├── methodology.md        # Study design, assumptions, metrics, limitations
├── data/                 # Licensed, de-identified, or synthetic inputs
├── experiments/          # Reproducible scripts/notebooks, if applicable
├── results/              # Outputs and provenance, if applicable
└── references.md         # Primary sources and relevant literature
```

## Research Standards

Every study should aim to document:

1. **Research question and scope** — a precise problem statement and intended audience.
2. **Evidence classification** — incident review, synthetic simulation, controlled real-model experiment, or independently validated field finding.
3. **Sources and provenance** — original reporting, datasets, licenses, model versions, configurations, and dates where relevant.
4. **Methodology and reproducibility** — steps, assumptions, controls, evaluation metrics, and runnable artifacts when possible.
5. **Results and uncertainty** — observations separated from interpretations; report false negatives, counterexamples, confidence intervals, or other relevant caveats.
6. **Enterprise relevance** — practical risk implications, potential controls, and what would need testing before deployment.
7. **Limitations and responsible disclosure** — no unsubstantiated detection claims, exposed secrets, unauthorized targets, or operationally harmful exploit instructions.

### Evidence Labels

| Label | Meaning |
|---|---|
| **Incident analysis** | Interpretation of reported events and available technical evidence; not necessarily reproduced. |
| **Synthetic demonstration** | Programmed or generated scenarios illustrating a methodology; not production evidence. |
| **Controlled experiment** | Documented measurements under specified conditions; generalization requires care. |
| **Field-validated finding** | Observations supported by a defined real-world evaluation and documented constraints. |
| **Proposed application** | An idea for how OpenVals or related tooling might help; not a demonstrated capability. |

## How OpenVals Fits

OpenVals is positioned around **evaluation, validation, benchmarking, and assurance** for enterprise AI. Research in this repository can inform test design and potential platform integrations, but the relationship between a case study and the live product must be explicitly stated in that study.

For security-oriented investigations, **OpenVals × RedShield** may be discussed as a *proposed assurance approach*. Any claims of prevention, exploit detection, safety improvement, compliance, or ROI require independently inspectable supporting evidence.

## Who This Is For

AI/ML engineers, security researchers, enterprise architects, AI governance and risk teams, developers of agentic systems, CISOs, CIOs, CTOs, CAIOs, researchers, and technical decision-makers seeking evidence-based assurance methods.

## Contributing

We welcome improvements to research design, source verification, datasets, reproducibility, documentation, and tests. Please review [CONTRIBUTING.md](CONTRIBUTING.md) if present, or open an [Issue](https://github.com/DrPinnacle/openvals-case-studies/issues) to propose a study or correction. Do not submit confidential customer data, credentials, or unapproved exploit material.

**Maintainers:** When publishing a new study, update only the **Case Study Index**, add a concise summary section if helpful, and ensure the study has its own standalone README. Keep this root README focused on discovery, principles, and navigation.

## Licensing and Responsible Use

Check the repository's [LICENSE](LICENSE) and any **study-specific licenses or notices** before reusing code, datasets, images, or reports. Different artifacts may carry different terms. Research is provided for education and validation; it is **not** a certification of safety, security, regulatory compliance, or incident prevention.

## Project Links

- **Research repository:** [DrPinnacle/openvals-case-studies](https://github.com/DrPinnacle/openvals-case-studies)
- **OpenVals core:** [vishwanathakuthota/openvals](https://github.com/vishwanathakuthota/openvals)
- **DrPinnacle GitHub:** [DrPinnacle](https://github.com/DrPinnacle)

---

<div align="center">

**OpenVals — Engineering AI Trust. Measuring Enterprise Value.**  
*A DrPinnacle Initiative*

</div>
