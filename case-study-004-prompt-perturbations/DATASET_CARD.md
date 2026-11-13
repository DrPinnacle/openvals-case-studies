# Dataset card

This public dataset contains 24 newly authored, procedurally instantiated English multiple-choice items. Eight items each cover inventory arithmetic, boundary classification, and ordering by transitive constraints. Each item includes a deterministic answer and rationale. No external benchmark, private data, or model-generated answer key was used.

Each item has three variants. The baseline and layout forms have the same question and choices, with different whitespace and option separators. The paraphrase preserves the task, choice text, choice order, and correct answer. The inventory paraphrase also reorders facts. The ordering paraphrase changes relation phrasing and sequence. The threshold paraphrase restates the boundary rules.

The public JSON stores the original pilot instruction. The follow-up replaces the final line uniformly at request time, leaving questions and choices intact. Exact transmitted prompts are in the raw JSONL. Each family has two correct answers per option letter.

The fixtures are small, templated, and deliberately narrow. Item variants were checked against their generating rules and answer keys. There was no independent annotator panel or held-out sample. Use the fixtures to examine controlled sensitivity and output-contract failures. The dataset provides no estimate of broad LLM capability.
