# Methodology — OpenVals Case Study 001

## Study design
A deterministic synthetic pairwise evaluator scores each candidate using an explicitly provided oracle-quality label (1 = preferred, 0 = nonpreferred) plus optional presentation bonuses. This is a **simulation**, not an LLM judge. Six synthetic IT-support cases are used; four are tagged `critical` for illustrative safety-severity stratification. Dataset selection is purposive, not random.

## Mathematical specification
For candidate response r in display position p (first=0, second=1):

`S(r,p) = Q(r) + alpha * I(p=0) + beta * W(r)`

- `Q(r)`: dataset oracle quality, not model-inferred correctness
- `alpha`: synthetic first-position bonus
- `beta`: synthetic bonus per whitespace-delimited word
- `W(r)`: whitespace-delimited word count

The response with higher score wins. Ties favor the first response. For each case, judge both `[A,B]` and `[B,A]`.

## Metrics and denominators
- **AB accuracy:** number of AB winners matching the synthetic expert-preferred ID / all cases.
- **AB incorrect approval rate:** AB winners not matching the expert-preferred ID / all cases. This is the complement of AB accuracy **only for this binary one-correct-option design**.
- **Order-swap inconsistency:** cases with different winner IDs across AB and BA / all cases.
- **Critical incorrect approval rate:** incorrect AB winners among critical cases / number of critical cases.

These are *sample descriptive statistics*, not estimated population error rates. No confidence intervals are warranted for a six-case convenience demonstration.

## Bias conditions
1. Unbiased oracle: `alpha=0, beta=0`.
2. Position only: `alpha=1.2, beta=0`.
3. Verbosity only: `alpha=0, beta=0.14`.
4. Combined: `alpha=0.6, beta=0.14`.

Parameters are illustrative and deliberately exaggerated to make failure modes visible. They are not fitted to observed judge behavior.

## Threats to validity
- Oracle quality is directly available to the simulated judge; real evaluators do not have such access.
- All expert labels are authored as part of synthetic data; no independent human adjudication.
- Small, intentionally constructed examples cannot establish prevalence, model rankings, or enterprise ROI.
- Simple word counts are not semantic quality measurements.
- Order-specific metrics depend on AB presentation; evaluate both directions before deployment decisions.

## Real-model extension protocol
1. Preregister rubric, critical-case taxonomy, acceptance thresholds and failure costs.
2. Obtain permissioned representative tasks, stratified by severity and domain.
3. Blindly collect at least two independent domain-expert ratings; adjudicate disagreements.
4. Freeze model identifiers, prompts, inference settings, evaluator version and input hashes.
5. Run both orderings with repeated independent trials when nondeterminism exists.
6. Measure expert agreement, error rates, order effects, verbosity sensitivity, and critical false approvals; report denominators and uncertainty intervals.
7. Conduct ablations and holdout evaluation; store immutable audit artifacts.
8. Integrate the actual OpenVals API/CLI only after confirming its current interface and record adapter versions.
9. Quantify operational benefit in a controlled pilot (e.g., reviewer hours, prevented incorrect approvals), not from this simulation.

## Reproducibility
`python3 case-studies/001-llm-judge-reliability/experiment.py --output reports/results.json`
`python3 -m unittest discover -s tests -v`

No network access, keys, or third-party dependencies are required.
