"""Verify recorded trial integrity and recompute metrics from provider responses."""
import argparse
import importlib.util
import json
import math
import random
import re
import statistics
from pathlib import Path

import adapters
from design import ROOT, VARIANTS, fixtures, trials
from run import sha256


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parse(text):
    cleaned = text.strip()
    return cleaned if re.fullmatch(r"[A-D]", cleaned) else None


def parse_json(text):
    try:
        fields = json.loads(text, object_pairs_hook=lambda pairs: pairs)
    except ValueError:
        return None
    if isinstance(fields, list) and len(fields) == 1 and isinstance(fields[0], tuple):
        key, value = fields[0]
        if key == "answer" and isinstance(value, str) and value in ("A", "B", "C", "D"):
            return value
    return None


def load_protocol(manifest):
    source = Path(__file__).parent
    protocol = manifest.get("protocol", "pilot")
    if protocol == "constrained":
        return source, adapters, parse_json
    require(protocol == "pilot", "Unknown study protocol")
    source = source / "pilot"
    spec = importlib.util.spec_from_file_location("pilot_adapters", source / "adapters.py")
    adapter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adapter)
    return source, adapter, parse


def tally(values):
    return {"count": sum(values), "denominator": len(values)}


def agreement(left, right):
    return left is not None and left == right


def paired_interval(differences):
    """Percentile interval from resampling items, with their repeats kept together."""
    rng = random.Random(4004)
    means = sorted(statistics.mean(rng.choices(differences, k=len(differences)))
                   for _ in range(10000))
    return [means[249], means[9749]]


def score(path):
    dataset = ROOT / "data/cases.json"
    cases = json.loads(dataset.read_text(encoding="utf-8"))
    require(cases == fixtures(), "Dataset generator does not reproduce the frozen dataset")
    plan = trials(cases)
    manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
    raw = path / "raw.jsonl"
    require(manifest["schema"] == 1 and manifest["status"] == "complete",
            f"{path}: run is not complete")
    require(manifest["dataset_sha256"] == sha256(dataset), f"{path}: dataset digest mismatch")
    require(manifest["raw_sha256"] == sha256(raw), f"{path}: raw digest mismatch")
    source, adapter, parse_answer = load_protocol(manifest)
    for name in ("adapters.py", "design.py", "run.py"):
        require(manifest["code_sha256"][name] == sha256(source / name),
                f"{path}: recorded runner differs from packaged {name}")
    rows = [json.loads(line) for line in raw.read_text(encoding="utf-8").splitlines()]
    require(len(plan) == len(rows) == manifest["planned"], f"{path}: trial count mismatch")
    provider = manifest["provider"]
    require(provider in {"ollama", "anthropic"}, "Unexpected provider")
    answers = {}
    latencies = []
    failures = []
    keys = {case["id"]: case["answer"] for case in cases}
    models = set()
    stop_reasons = {}
    for sequence, (row, (item, variant, repeat, seed, prompt)) in enumerate(zip(rows, plan), 1):
        url, payload = adapter.build_request(provider, manifest["model"], prompt, seed)
        require((row["sequence"], row["item"], row["variant"], row["repeat"],
                 row["url"], row["request"]) == (sequence, item, variant, repeat, url, payload),
                f"{path}: schedule or request mismatch at {sequence}")
        latency = row["latency_ms"]
        require(isinstance(latency, (float, int)) and math.isfinite(latency) and latency >= 0,
                f"{path}: invalid latency at {sequence}")
        if row["error"] is None:
            require(row["response"]["http_status"] == 200, f"{path}: unexpected HTTP status")
            provider_payload = json.loads(row["response"]["body"])
            models.add(provider_payload["model"])
            reason = provider_payload.get("done_reason", provider_payload.get("stop_reason", "unknown"))
            stop_reasons[reason] = stop_reasons.get(reason, 0) + 1
            answer = parse_answer(adapter.response_text(provider, row["response"]))
            latencies.append(latency)
        else:
            answer = None
        answers[item, variant, repeat] = answer
        if answer != keys[item]:
            failures.append({"sequence": sequence, "item": item, "variant": variant,
                             "repeat": repeat, "expected": keys[item], "parsed": answer,
                             "outcome": ("request_error" if row["error"] else
                                         "format_error" if answer is None else "wrong_option")})
    require(len(models) <= 1, f"{path}: provider returned multiple model identifiers")
    if provider == "ollama" and models:
        require(models == {manifest["model"]}, f"{path}: provider returned another model tag")
    summary = {}
    for variant in VARIANTS:
        accuracy = [answers[item, variant, repeat] == gold
                    for item, gold in keys.items() for repeat in (1, 2)]
        repeatable = [agreement(answers[item, variant, 1], answers[item, variant, 2])
                      for item in keys]
        summary[variant] = {"accuracy": tally(accuracy), "repeat_agreement": tally(repeatable)}
        if variant == "baseline":
            continue
        pairs = [(answers[item, "baseline", repeat], answers[item, variant, repeat], gold)
                 for item, gold in keys.items() for repeat in (1, 2)]
        changes = [int(after == gold) - int(before == gold) for before, after, gold in pairs]
        summary[variant].update(
            agreement_with_baseline=tally([agreement(before, after) for before, after, _ in pairs]),
            baseline_correct_variant_failed=changes.count(-1),
            baseline_failed_variant_correct=changes.count(1),
            accuracy_delta=statistics.mean(changes),
            accuracy_delta_item_bootstrap_95=paired_interval(
                [statistics.mean(changes[i:i+2]) for i in range(0, len(changes), 2)]),
        )
    failures_by_type = {outcome: sum(row["outcome"] == outcome for row in failures)
                        for outcome in ("request_error", "format_error", "wrong_option")}
    return {
        "protocol": manifest.get("protocol", "pilot"), "provider": provider, "model": manifest["model"], "observed_models": sorted(models),
        "items": len(keys), "attempts": len(rows), "correct": len(rows)-len(failures),
        "all_six_correct": tally([all(answers[item, variant, repeat] == gold
                                      for variant in VARIANTS for repeat in (1, 2))
                                  for item, gold in keys.items()]),
        "failures_by_type": failures_by_type,
        "stop_reasons": stop_reasons,
        "failure_rows": failures, "conditions": summary,
        "successful_http_latency_ms": {
            "count": len(latencies),
            "median": statistics.median(latencies) if latencies else None,
            "p95_nearest_rank": sorted(latencies)[math.ceil(.95*len(latencies))-1]
            if latencies else None,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    result = {"schema": 1, "runs": [score(path) for path in args.runs]}
    if args.verify:
        require(result == json.loads(args.verify.read_text(encoding="utf-8")),
                "Recomputed metrics differ from the release summary")
        print(f"Verified {len(args.runs)} run(s) and all reported machine-readable metrics.")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
