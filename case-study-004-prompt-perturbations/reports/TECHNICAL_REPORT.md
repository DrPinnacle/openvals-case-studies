# OpenVals Case Study 004

## LLM reliability under meaning-preserving prompt perturbations

**13 November 2026 · OpenVals — A DrPinnacle Initiative**

We tested whether paraphrasing a question or changing its layout affects the option selected by a model. Each local model saw 24 items in three forms with two requests per form. The first pass asked for a single letter. The follow-up used JSON-constrained decoding after the pilot exposed format failures.

## Structured-output follow-up

| Model | Form | Strict accuracy | Same option as baseline | Repeat agreement | Correct → failed | Failed → correct | Accuracy change, pp (95% item bootstrap) |
|---|---|---:|---:|---:|---:|---:|---:|
| qwen3:4b | baseline | 20/48 | — | 21/24 | — | — | — |
| qwen3:4b | paraphrase | 18/48 | 25/48 | 20/24 | 6 | 4 | -4.2 [-22.9, +12.5] |
| qwen3:4b | layout | 16/48 | 34/48 | 19/24 | 4 | 0 | -8.3 [-20.8, +0.0] |
| mistral:latest | baseline | 14/48 | — | 24/24 | — | — | — |
| mistral:latest | paraphrase | 12/48 | 18/48 | 24/24 | 8 | 6 | -4.2 [-25.0, +16.7] |
| mistral:latest | layout | 17/48 | 28/48 | 23/24 | 8 | 11 | +6.2 [-18.8, +31.2] |

Accuracy and baseline agreement use 48 attempts or pairs per form. Repeat agreement uses 24 items per form. Agreement includes shared wrong options and requires both outputs to parse. The item bootstrap keeps both repeats together.

## Evidence across both passes

| Model | Pass | Strict correct | Items correct on all six | Request errors | Format errors | Wrong options | Provider stop reasons | Median / p95 latency (ms) |
|---|---|---:|---:|---:|---:|---:|---|---:|
| qwen3:4b | constrained | 54/144 | 5/24 | 0 | 0 | 90 | stop 144 | 673.8 / 768.3 |
| mistral:latest | constrained | 43/144 | 2/24 | 0 | 0 | 101 | stop 144 | 583.2 / 622.4 |
| qwen3:4b | pilot | 0/144 | 0/24 | 0 | 144 | 0 | length 144 | 1360.7 / 1860.7 |
| mistral:latest | pilot | 0/144 | 0/24 | 0 | 144 | 0 | length 14, stop 130 | 496.3 / 1447.2 |

The pilot scored output-contract compliance jointly with accuracy. A truncated or unparseable response gives no basis to infer the option the model would ultimately select. The follow-up changed the output instruction, decoder constraint and generation budget together. Changes across the two passes cannot isolate the effect of any one setting.

## Commercial cohort

**Not run.** No configured commercial model API credential was available. No commercial requests or scores are included.

## Interpretation and limits

Baseline accuracy can conceal instability because losses and gains can offset each other. The discordant pair counts and all-six-correct metric describe this behavior at the item level. The fixtures cover three templated English task families, and the two local models used particular quantized builds. The study estimates behavior under those test conditions. The small, related item set and two repeats limit generalization. No claim about hosted model performance or enterprise deployment follows from these results.

The [methodology](../METHODOLOGY.md) defines the metrics. The [machine-readable results](../results/summary.json) identify every failed trial by its raw record sequence. See [reproducibility](../REPRODUCIBILITY.md) for verification commands.
