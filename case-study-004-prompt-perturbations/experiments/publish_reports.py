"""Render publication reports from the recomputable results."""
import argparse
import json

from design import ROOT


def ratio(metric):
    return f"{metric['count']}/{metric['denominator']}"


def percent(value):
    return f"{value * 100:+.1f}"


def technical(runs, commercial):
    lines = [
        "# OpenVals Case Study 004",
        "",
        "## LLM reliability under meaning-preserving prompt perturbations",
        "",
        "**13 November 2026 · OpenVals — A DrPinnacle Initiative**",
        "",
        "We tested whether paraphrasing a question or changing its layout affects the "
        "option selected by a model. Each local model saw 24 items in three forms with "
        "two requests per form. The first pass asked for a single letter. The follow-up "
        "used JSON-constrained decoding after the pilot exposed format failures.",
        "",
        "## Structured-output follow-up",
        "",
        "| Model | Form | Strict accuracy | Same option as baseline | Repeat agreement | "
        "Correct → failed | Failed → correct | Accuracy change, pp (95% item bootstrap) |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for run in runs:
        if run["protocol"] != "constrained":
            continue
        for variant, stats in run["conditions"].items():
            values = [run["model"], variant, ratio(stats["accuracy"]),
                      ratio(stats["agreement_with_baseline"]) if variant != "baseline" else "—",
                      ratio(stats["repeat_agreement"])]
            if variant == "baseline":
                values += ["—", "—", "—"]
            else:
                low, high = map(percent, stats["accuracy_delta_item_bootstrap_95"])
                values += [str(stats["baseline_correct_variant_failed"]),
                           str(stats["baseline_failed_variant_correct"]),
                           f"{percent(stats['accuracy_delta'])} [{low}, {high}]"]
            lines.append("| " + " | ".join(values) + " |")
    lines += [
        "",
        "Accuracy and baseline agreement use 48 attempts or pairs per form. Repeat agreement "
        "uses 24 items per form. Agreement includes shared wrong options and requires both "
        "outputs to parse. The item bootstrap keeps both repeats together.",
        "",
        "## Evidence across both passes",
        "",
        "| Model | Pass | Strict correct | Items correct on all six | Request errors | "
        "Format errors | Wrong options | Provider stop reasons | Median / p95 latency (ms) |",
        "|---|---|---:|---:|---:|---:|---:|---|---:|",
    ]
    for run in runs:
        errors = run["failures_by_type"]
        latency = run["successful_http_latency_ms"]
        stops = ", ".join(f"{reason} {count}" for reason, count in sorted(run["stop_reasons"].items()))
        lines.append(
            f"| {run['model']} | {run['protocol']} | {run['correct']}/{run['attempts']} | "
            f"{ratio(run['all_six_correct'])} | {errors['request_error']} | {errors['format_error']} | "
            f"{errors['wrong_option']} | {stops} | "
            f"{latency['median']:.1f} / {latency['p95_nearest_rank']:.1f} |")
    lines += [
        "",
        "The pilot scored output-contract compliance jointly with accuracy. A truncated or "
        "unparseable response gives no basis to infer the option the model would ultimately select. "
        "The follow-up changed the output instruction, decoder constraint and generation budget "
        "together. Changes across the two passes cannot isolate the effect of any one setting.",
        "",
        "## Commercial cohort",
        "",
        f"**{commercial['status'].replace('_', ' ').capitalize()}.** {commercial['reason']}",
        "",
        "## Interpretation and limits",
        "",
        "Baseline accuracy can conceal instability because losses and gains can offset each other. "
        "The discordant pair counts and all-six-correct metric describe this behavior at the item "
        "level. The fixtures cover three templated English task families, and the two local models "
        "used particular quantized builds. The study estimates behavior under those test conditions. "
        "The small, related item set and two repeats limit generalization. No claim about hosted "
        "model performance or enterprise deployment follows from these results.",
        "",
        "The [methodology](../METHODOLOGY.md) defines the metrics. The "
        "[machine-readable results](../results/summary.json) identify every failed trial by its "
        "raw record sequence. See [reproducibility](../REPRODUCIBILITY.md) for verification commands.",
        "",
    ]
    return "\n".join(lines)


def executive(runs, commercial):
    followup = [run for run in runs if run["protocol"] == "constrained"]
    pilot = [run for run in runs if run["protocol"] == "pilot"]
    attempts = sum(run["attempts"] for run in runs)
    lines = [
        "# Executive brief · OpenVals Case Study 004",
        "",
        "## Prompt wording, layout, and reliable answers",
        "",
        f"We recorded {attempts} real inference attempts across Qwen3-4B and Mistral, including "
        "an initial single-letter pilot and a structured-output follow-up. The study checked "
        "whether known-answer tasks kept the same outcome under equivalent prompt forms.",
        "",
        f"The pilot recorded {sum(run['failures_by_type']['format_error'] for run in pilot)} "
        f"format failures in {sum(run['attempts'] for run in pilot)} attempts. The follow-up "
        "used schema-constrained decoding and a higher generation limit.",
        "",
    ]
    for run in followup:
        base, paraphrase, layout = (run["conditions"][form]
                                    for form in ("baseline", "paraphrase", "layout"))
        lines.append(
            f"- **{run['model']}** answered {ratio(base['accuracy'])} baseline attempts, "
            f"{ratio(paraphrase['accuracy'])} paraphrases and {ratio(layout['accuracy'])} "
            f"layout variants correctly. It answered all six trials correctly on "
            f"{ratio(run['all_six_correct'])} items.")
    lines += [
        "",
        f"**Commercial cohort {commercial['status'].replace('_', ' ')}.** {commercial['reason']}",
        "",
        "For a workflow that consumes model outputs automatically, the pilot illustrates the "
        "importance of measuring response validity. The follow-up illustrates how paired trials "
        "can expose answer changes that aggregate accuracy can hide. The observations are limited "
        "to these fixtures, model builds, and decoding settings.",
        "",
        "See the [technical report](TECHNICAL_REPORT.md) for paired results, uncertainty, and "
        "links to the underlying evidence.",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    runs = json.loads((ROOT / "results/summary.json").read_text())["runs"]
    cohorts = json.loads((ROOT / "results/cohorts.json").read_text())["cohorts"]
    commercial = next(cohort for cohort in cohorts if cohort["id"] == "commercial-hosted")
    for filename, content in (("TECHNICAL_REPORT.md", technical(runs, commercial)),
                              ("ENTERPRISE_SUMMARY.md", executive(runs, commercial))):
        path = ROOT / "reports" / filename
        if args.verify:
            if path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"Report differs from metrics: {filename}")
        else:
            path.write_text(content, encoding="utf-8")
    if args.verify:
        print("Verified both publication reports against the release results.")


if __name__ == "__main__":
    main()
