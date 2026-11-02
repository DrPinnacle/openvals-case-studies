# Enterprise summary — Case Study 003

**31 October 2026 · Version 1.0 · Powered by Dr.Pinnacle**

## Decision supported

Require evaluation of both authorized task completion and adversarial outcome rates before selecting a prompt-injection control. This study provides a reproducible teaching and measurement package; it does not select a production control or certify a model.

## What the demonstration shows

In 24 synthetic attacks, the programmed keyword filter emits a harmless attacker marker six times. It also blocks six of 12 benign tasks. Its apparent reduction in marker emission leaves overall task completion unchanged at 6/36. An idealized trusted-field oracle answers all 36 correctly by ignoring unneeded context. Every outcome follows from deliberately written rules; no real LLM, customer system, OpenVals platform, or RedShield product was tested.

## Proposed pilot and ownership

The AI application owner should define the authorized task and acceptable failure levels. Security should specify attacker-controlled surfaces and isolated test boundaries. Evaluation engineering should collect version-pinned model responses, preserve all failures and costs, and compare both attack outcomes and benign utility on independently authored held-out cases. Risk and governance should review residual failures and evidence provenance before release.

Proposed controls to evaluate include separating trusted instructions from retrieved content, limiting action permissions, and validating outputs against the application's contract. These are pilot candidates, not mitigations validated by this package. Do not connect this demonstration to real tools or credentials.

## Publication guardrails

A suitable claim is: “Case Study 003 demonstrates a reproducible, synthetic protocol for measuring prompt-injection outcomes and task utility.” Avoid claims of model resilience, prevented incidents, percentage risk reduction, compliance, ROI, or superiority over commercial defenses. No empirical product finding or business benefit has been established.

See the [technical report](TECHNICAL_REPORT.md) and [methodology](../METHODOLOGY.md) before using the results in decisions. Enterprise reuse is subject to the study's [license](../LICENSE.txt).
