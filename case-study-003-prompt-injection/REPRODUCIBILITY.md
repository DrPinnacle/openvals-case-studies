# Reproducibility and external-response protocol

Powered by Dr.Pinnacle

## Offline reproduction

Use Python 3.10+ on macOS, Linux, or Windows, with no third-party dependencies. From repository root:

```bash
python3 case-study-003-prompt-injection/benchmark.py --output /tmp/case003-reproduced.json
python3 -m unittest discover -s case-study-003-prompt-injection/tests -v
python3 -m unittest discover -s case-study-001/tests -v
python3 scripts/check_links.py
python3 scripts/package_release.py
```

On Windows use a writable output path instead of `/tmp`. The harness has no randomness. Compare `policies`, `dataset_sha256`, and `harness_sha256` against the published JSON; the Python version can differ. Source and dataset hashes are inside each output. The archive builder emits SHA-256 manifests and the full publication ZIP in the parent directory, excluding Git internals, caches, and `.DS_Store`.

## Optional real-model evidence collection — not executed

No provider connection or credential is required for the offline study. To perform a future real-model study, export requests:

```bash
python3 case-study-003-prompt-injection/export_requests.py --output /tmp/case003-requests.json
```

Each request contains only its ID and two messages. The system message defines the authority boundary; the user message is JSON containing `task`, `trusted_catalog_color`, and `untrusted_context`. Labels, family, kind, and scoring metadata are excluded. Exact message bytes should be retained with response evidence. Use the same serialization and prompts across comparison arms and document any modifications. No tool calls should be enabled for this task.

Collect responses through an approved model runner outside this package, one independent session per case. Store raw text without cleanup. Errors must remain explicit responses (for example, `ERROR: timeout`), counting as task failures; do not omit records. Do not insert simulated answers into an empirical bundle. A response bundle must have this shape (schematic only, not a complete runnable bundle):

```json
{
  "metadata": {
    "provider": "actual provider",
    "model": "actual model ID",
    "model_version": "resolved version or explicitly unavailable",
    "run_utc": "actual ISO-8601 UTC collection time",
    "prompt_template": "export_requests.py v1, plus exact request artifact hash",
    "sampling": {"temperature": 0, "max_output_tokens": 128},
    "repeats": 1,
    "dataset_sha256": "actual SHA-256 of data/cases.json"
  },
  "responses": [{"id": "ITEM-01-clean", "response": "raw model response"}]
}
```

Supply all 36 unique IDs. Then:

```bash
python3 case-study-003-prompt-injection/benchmark.py --responses /path/to/responses.json --output /path/to/empirical-results.json
```

Missing, duplicate, extra, and non-string responses are rejected, as is a mismatched dataset hash. Required metadata must be present, but its truth is self-attested: output is labeled `external_responses_unverified_provenance`. Preserve request files, timestamps, model settings, provider receipts when available, response hashes, failures, and review notes for independent provenance review. The importer does not authenticate provider execution. Run repeated collections into separate bundles; do not treat the six related color groups as 36 independent trials. Never replace the published simulation artifact with an empirical output.
