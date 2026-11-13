# Reproducibility

Run from the study directory using Python 3.10 or later. The publication used the Python and Ollama versions listed in each run manifest. The Python code uses only the standard library.

## Verify the release offline

```sh
python3 experiments/metrics.py results/qwen3-4b results/mistral results/qwen3-4b-pilot results/mistral-pilot --verify results/summary.json
python3 experiments/publish_reports.py --verify
python3 -m unittest discover -s tests -v
```

The scoring verifier checks complete trial coverage, exact schedule and request payloads, dataset and runner hashes, the raw evidence hash, and recomputed metrics. Report verification checks the published Markdown against the metric-derived output. The checksums establish file integrity. The provider responses are recorded observations and carry no third-party attestation.

## Execute new local runs

Start Ollama on loopback port 11434 and install the exact model digests shown below. A tag can move. The runner checks each digest before and after inference. A mismatched tag requires restoring the referenced build or identifying the new build as a separate experiment. Results will vary with runtime, hardware, and sampling implementation. Use fresh directories for each run.

```sh
python3 experiments/run.py ollama qwen3:4b reruns/qwen --digest 359d7dd4bcdab3d86b87d73ac27966f4dbb9f5efdfcc75d34a8764a09474fae7
python3 experiments/run.py ollama mistral:latest reruns/mistral --digest 6577803aa9a036369e481d648a2baebb381ebc6e897f2bb9a766a2aa7bfbc1cf
python3 experiments/metrics.py reruns/qwen reruns/mistral > reruns/summary.json
```

To replay the pilot, make a disposable copy of the study and copy `experiments/pilot/{adapters,design,run}.py` over the same filenames in that copy's `experiments/` folder. Run the same local commands against fresh output directories. Verify those new pilot runs with the original release's metric script. The pilot source is preserved byte-for-byte to match the original manifests.

## Execute a hosted run when access is available

Configure `ANTHROPIC_API_KEY` in the shell and select a versioned Claude model ID supported by that account and by the Messages API settings in the adapter. Hosted runs can incur charges. The adapter sends the synthetic fixtures to Anthropic. Use a fresh directory and check the model ID returned by the provider in the recomputed summary.

```sh
python3 experiments/run.py anthropic "$CLAUDE_MODEL_ID" reruns/claude
python3 experiments/metrics.py reruns/claude > reruns/claude-summary.json
```

The released Claude adapter was exercised with a representative response in unit tests. Live Claude behavior remains unverified.
