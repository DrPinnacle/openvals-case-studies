# Methodology

## Design and execution

Each model received 24 items × 3 forms × 2 repeats in a shuffled order using schedule seed 4004. Each request starts a fresh conversation. Local repeats use seeds 1301 and 1302 at temperature 0.2 with top-p 1, top-k 0, and a 2,048-token context. Baseline comparisons match by item and repeat. Different repeat seeds exercise sampling stability. The order is shared across models within each protocol. The runs were serial and model loading or server caching can affect request latency.

The first pass requested a bare option letter with a 32-token limit. After observing pervasive format failures, a follow-up used a uniform JSON instruction, Ollama schema-constrained generation, and a 96-token limit. Qwen received `think: false` in both passes. Because the follow-up changed the instruction, decoding constraint, and token budget together, differences between passes cannot isolate a single cause. Treat the follow-up as exploratory. The fixtures were reused after the first pass.

The hosted Anthropic adapter is included for extension. It requests JSON via the prompt with a 96-token cap and temperature 0.2, without the local decoder constraint or a seed. Provider-specific controls and model capabilities matter when interpreting a future comparison. The released evidence has no commercial measurements.

## Scoring

- **Strict accuracy** is correct parsed options divided by planned attempts for the condition. The pilot accepts one uppercase A–D letter after trimming whitespace. The follow-up requires a JSON object with exactly one `answer` key and a value in A–D. Wrong answers, invalid responses, and request failures count as incorrect.
- **Agreement with baseline** is the fraction of matched item/repeat pairs where both answers parse and select the same option, including shared wrong options. Agreement between unparseable outputs is excluded from the numerator. The denominator includes every pair.
- **Repeat agreement** uses the same rule for the two requests to a fixed item and form. The denominator is 24 items per condition.
- **All six correct** requires a correct answer on both repeats of all three forms for an item.
- **Paired change** is variant minus baseline accuracy. The report gives the two directions of discordance and a percentile interval from 10,000 bootstrap draws over items, holding repeats together, with seed 4004. The interval describes sensitivity to resampling these fixtures. Templated items are related, and the interval is exploratory. Degenerate intervals can result from uniform failure or ceiling effects.
- **Latency** is wall-clock request time for responses that reached the response extractor successfully. The p95 uses nearest rank. It includes client overhead and may include model loading, caching, or scheduling effects.
- **Failure counts** classify each unsuccessful trial as request/response error, format error, or wrong option, in that order. Provider stop reasons are counted independently.

A complete block requires one recorded attempt per scheduled trial. There are no silent retries. Fatal configuration HTTP errors leave partial evidence with an in-progress manifest. Completed manifests record the dataset, runner and evidence hashes. Provider response text and metadata are retained as the unmodified HTTP response body within JSONL. For failed HTTP calls, only the status and exception category are retained.
