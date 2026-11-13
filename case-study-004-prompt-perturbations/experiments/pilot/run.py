"""Run a complete randomized block and preserve each attempt as JSONL."""
import argparse
import hashlib
import json
import platform
import time
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

from adapters import CLAUDE_VERSION, auth, build_request, local_metadata, request, response_text
from design import ROOT, fixtures, trials


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("provider", choices=("ollama", "anthropic"))
    parser.add_argument("model")
    parser.add_argument("output", type=Path, help="New run directory")
    parser.add_argument("--digest", help="Required Ollama SHA-256 model digest")
    args = parser.parse_args()
    headers = auth(args.provider)
    dataset = ROOT / "data/cases.json"
    cases = json.loads(dataset.read_text(encoding="utf-8"))
    if cases != fixtures():
        parser.error("Dataset differs from the frozen fixture generator")
    plan = trials(cases)
    metadata = local_metadata(args.model) if args.provider == "ollama" else {
        "api_version": CLAUDE_VERSION, "seed_supported": False,
    }
    if args.provider == "ollama" and metadata["tag"]["digest"] != args.digest:
        parser.error("Installed tag does not match the required --digest")
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = {
        "schema": 1, "provider": args.provider, "model": args.model, "metadata": metadata,
        "python": platform.python_version(), "os": platform.system(),
        "os_release": platform.release(), "architecture": platform.machine(),
        "dataset_sha256": sha256(dataset),
        "code_sha256": {name: sha256(Path(__file__).with_name(name))
                        for name in ("run.py", "adapters.py", "design.py")},
        "started_at_utc": now(), "planned": len(plan), "status": "in_progress",
    }
    manifest_path = args.output / "manifest.json"
    raw = args.output / "raw.jsonl"
    write_json(manifest_path, manifest)
    with raw.open("x", encoding="utf-8") as stream:
        for number, (item, variant, repeat, seed, prompt) in enumerate(plan, 1):
            url, payload = build_request(args.provider, args.model, prompt, seed)
            row = {
                "sequence": number, "item": item, "variant": variant, "repeat": repeat,
                "url": url, "request": payload, "started_at_utc": now(),
                "response": None, "error": None,
            }
            start = time.monotonic()
            try:
                row["response"] = request(url, payload, headers)
                if not isinstance(response_text(args.provider, row["response"]), str):
                    raise TypeError("Response content must be text")
            except urllib.error.HTTPError as error:
                row["error"] = {"kind": "http", "status": error.code}
            except (OSError, ValueError, KeyError, TypeError) as error:
                row["error"] = {"kind": type(error).__name__}
            row["latency_ms"] = round((time.monotonic() - start) * 1000, 3)
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            stream.flush()
            if number % 12 == 0:
                print(f"{args.model}: {number}/{len(plan)} attempts", flush=True)
            if row["error"] and row["error"].get("status") in {400, 401, 403, 404}:
                raise SystemExit(f"Provider returned HTTP {row['error']['status']}; partial run retained.")
    if args.provider == "ollama" and local_metadata(args.model)["tag"]["digest"] != args.digest:
        raise SystemExit("Model digest changed; partial run retained without completion marker.")
    manifest.update(status="complete", completed_at_utc=now(), raw_sha256=sha256(raw))
    write_json(manifest_path, manifest)


if __name__ == "__main__":
    main()
