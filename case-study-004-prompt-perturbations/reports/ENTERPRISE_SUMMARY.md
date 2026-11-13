# Executive brief · OpenVals Case Study 004

## Prompt wording, layout, and reliable answers

We recorded 576 real inference attempts across Qwen3-4B and Mistral, including an initial single-letter pilot and a structured-output follow-up. The study checked whether known-answer tasks kept the same outcome under equivalent prompt forms.

The pilot recorded 288 format failures in 288 attempts. The follow-up used schema-constrained decoding and a higher generation limit.

- **qwen3:4b** answered 20/48 baseline attempts, 18/48 paraphrases and 16/48 layout variants correctly. It answered all six trials correctly on 5/24 items.
- **mistral:latest** answered 14/48 baseline attempts, 12/48 paraphrases and 17/48 layout variants correctly. It answered all six trials correctly on 2/24 items.

**Commercial cohort not run.** No configured commercial model API credential was available. No commercial requests or scores are included.

For a workflow that consumes model outputs automatically, the pilot illustrates the importance of measuring response validity. The follow-up illustrates how paired trials can expose answer changes that aggregate accuracy can hide. The observations are limited to these fixtures, model builds, and decoding settings.

See the [technical report](TECHNICAL_REPORT.md) for paired results, uncertainty, and links to the underlying evidence.
