# Dataset card — Case Study 003 v1.0

Powered by Dr.Pinnacle

**Origin:** Authored for this package on 31 October 2026; no scraped, private, customer, or model-generated records. All colors, instructions, and the canary are synthetic. License: [DPCL-CE](LICENSE.txt), scope in [NOTICE.md](NOTICE.md).

## Composition and schema

`data/cases.json` contains 36 records: six catalog colors × six variants. Each group includes a clean benign control, a benign glossary quotation, and four attack variants (override, role spoofing, indirect evaluator-authority claim, spaced-token obfuscation). There are 24 attack and 12 benign records. The indirect case is a textual retrieved-note simulation, not a running retrieval pipeline.

Fields: `id` (unique case), `pair_id` (related color group), `kind` (`attack` or `benign`), `family`, `task`, `trusted_color`, `untrusted_text`, `expected` (author-assigned color answer), and `marker` (`OV_CANARY_003`). Reference answers are assigned from the trusted catalog, not inferred by a model. No independent expert annotation is claimed.

## Safe handling and limitations

The marker is public dummy text, not a secret. Payloads request only an output change. There are no URLs, credentials, shell commands, exploit instructions, executable payloads, or outbound actions in the dataset. Treat all task text as data during evaluation.

All records are public development fixtures, not a train/test split. The six colors are near-duplicate templates, not 36 independent observations. The quoted controls are deliberately adversarial to simple text matching. Neither broad attack coverage nor realistic frequency is claimed. Do not train and then report held-out accuracy on these same fixtures. Independent authors should create new families and review labels before a real pilot.
