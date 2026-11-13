"""Deterministic fixture generation and trial scheduling."""
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ("baseline", "paraphrase", "layout")
SEEDS = (1301, 1302)
LETTERS = "ABCD"
INSTRUCTION = "Reply with exactly one option letter (A, B, C, or D)."


def fixtures():
    items = []
    for i in range(8):
        initial, boxes, size, sent = 5+i, 2+i%3, 4+i, 3+2*i
        correct = initial + boxes * size - sent
        items.append(("inventory", [
            f"A store has {initial} loose bolts and {boxes} boxes containing {size} bolts each. It ships {sent} bolts. How many remain?",
            f"After sending out {sent} bolts, how many bolts are left from a stock of {boxes} boxes of {size} bolts apiece plus {initial} loose bolts?",
        ], correct, [correct+sent, correct-initial, correct+1],
            f"{initial} + {boxes} × {size} − {sent} = {correct}"))
        low, high = 10+i, 16+2*i
        value = (low-1, low, high-1, high)[i%4]
        allowed = low <= value < high
        correct = "Allow" if allowed else ("Too low" if value < low else "Too high")
        items.append(("threshold", [
            f"A gate allows scores from {low} inclusive to {high} exclusive. Classify the score {value} as Allow, Too low, or Too high.",
            f"For a score of {value}, choose its gate classification. The minimum allowed score is {low}, and scores of {high} and above are too high.",
        ], correct, [label for label in ("Allow", "Too low", "Too high", "Unknown") if label != correct],
            f"{low} <= {value} < {high} is {allowed}. Classification: {correct}."))
        people = ["Ari", "Bo", "Cy", "Dee"]
        order = people[i%4:] + people[:i%4]
        a, b, c, d = order
        place = 2+i%2
        ordinal = ("second", "third")[i%2]
        correct = order[place-1]
        items.append(("ordering", [
            f"Four people finish a race with no ties. {c} finishes before {d}. {a} finishes before {b}. {b} finishes before {c}. Who finishes {ordinal}?",
            f"Who is in place {place} in a four-person race with distinct finish positions? {d} trails {c}, {c} trails {b}, and {b} trails {a}.",
        ], correct, [person for person in people if person != correct], " < ".join(order)))
    cases = []
    for index, (family, questions, answer, distractors, rationale) in enumerate(items):
        position = index % len(LETTERS)
        options = list(map(str, distractors))
        options.insert(position, str(answer))
        lines = [f"{letter}. {option}" for letter, option in zip(LETTERS, options)]
        cases.append({
            "id": f"item-{index+1:02}", "family": family, "options": options,
            "answer": LETTERS[position], "rationale": rationale,
            "prompts": {
                "baseline": "\n".join([questions[0], *lines, INSTRUCTION]),
                "paraphrase": "\n".join([questions[1], *lines, INSTRUCTION]),
                "layout": f"{questions[0]}\n\n" + " | ".join(lines) + f"\n\n{INSTRUCTION}",
            },
        })
    return cases


def trials(cases):
    schedule = [(item["id"], variant, repeat, seed, item["prompts"][variant])
                for item in cases for variant in VARIANTS
                for repeat, seed in enumerate(SEEDS, 1)]
    random.Random(4004).shuffle(schedule)
    return schedule


if __name__ == "__main__":
    print(json.dumps(fixtures(), ensure_ascii=False, indent=2))
