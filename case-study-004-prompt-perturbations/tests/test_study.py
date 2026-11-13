import json
import shutil
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from adapters import build_request, response_text
from design import VARIANTS, fixtures, trials
from metrics import agreement, parse, parse_json, score

RUNS = ("qwen3-4b", "mistral", "qwen3-4b-pilot", "mistral-pilot")


class StudyTests(unittest.TestCase):
    def test_dataset_and_schedule(self):
        cases = json.loads((ROOT / "data/cases.json").read_text())
        self.assertEqual(cases, fixtures())
        self.assertEqual(Counter(case["family"] for case in cases),
                         {"inventory": 8, "threshold": 8, "ordering": 8})
        for family in ("inventory", "threshold", "ordering"):
            self.assertEqual(Counter(case["answer"] for case in cases if case["family"] == family),
                             dict.fromkeys("ABCD", 2))
        self.assertEqual(len(set(trial[:3] for trial in trials(cases))), 144)
        for case in cases:
            self.assertEqual(len(set(case["options"])), 4)
            self.assertEqual(tuple(case["prompts"]), VARIANTS)
            for label, option in zip("ABCD", case["options"]):
                self.assertTrue(all(f"{label}. {option}" in p for p in case["prompts"].values()))

    def test_parsers(self):
        self.assertEqual(parse(" A\n"), "A")
        self.assertIsNone(parse("A. Dee"))
        self.assertEqual(parse_json('{"answer":"D"}'), "D")
        for bad in ('{"answer":"A","answer":"B"}', '[["answer","A"]]',
                    '{"answer":"C","why":"x"}', 'A', '{"answer":"a"}'):
            self.assertIsNone(parse_json(bad))
        self.assertFalse(agreement(None, None))
        self.assertTrue(agreement("B", "B"))

    def test_adapters(self):
        prompt = fixtures()[0]["prompts"]["baseline"]
        _, local = build_request("ollama", "qwen3:4b", prompt, 1301)
        url, hosted = build_request("anthropic", "pinned-example", prompt, 1301)
        self.assertEqual(local["messages"], hosted["messages"])
        self.assertEqual(local["options"]["seed"], 1301)
        self.assertNotIn("seed", hosted)
        self.assertFalse(local["think"])
        self.assertEqual(url, "https://api.anthropic.com/v1/messages")
        example = {"type": "message", "role": "assistant",
                   "content": [{"type": "text", "text": '{"answer":"B"}'}]}
        self.assertEqual(parse_json(response_text("anthropic", {"body": json.dumps(example)})), "B")

    def test_release_recomputes(self):
        published = json.loads((ROOT / "results/summary.json").read_text())
        self.assertEqual([score(ROOT / "results" / name) for name in RUNS], published["runs"])

    def test_tampered_evidence_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "run"
            shutil.copytree(ROOT / "results/qwen3-4b-pilot", copy)
            with (copy / "raw.jsonl").open("a") as stream:
                stream.write("{}\n")
            with self.assertRaisesRegex(ValueError, "raw digest mismatch"):
                score(copy)
