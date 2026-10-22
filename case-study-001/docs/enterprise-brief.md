# Executive brief — Why evaluate the evaluator?

Enterprise AI governance depends on more than measuring generated answers. It also depends on the **reliability of the measurement process**. A judge that rewards presentation or answer position can approve unsafe or inaccurate responses and distort model comparisons.

This case study demonstrates an auditable test harness for two possible sources of evaluator instability: order and verbosity. It is a **synthetic educational experiment**, not a claim that OpenVals has prevented incidents or measured real-world error rates.

## Pilot proposition
In a 2–4 week scoped enterprise pilot, jointly define a representative expert-labelled dataset, risk-weighted evaluation rubric, release gates, and baseline workflow. Run version-pinned judge calibration and order-swapped tests, then report critical-case false approvals and human-review burden with uncertainty and limitations.

## Pilot acceptance criteria (to agree with the client)
- Minimum expert-label agreement and adjudication procedure
- Maximum critical-case incorrect approval rate on a sufficiently sized holdout set
- Maximum tolerated order-swap inconsistency
- Required evidence completeness and auditability
- Measured change in review time and escalation workload relative to baseline

**OpenVals — Engineering AI Trust. Measuring Enterprise Value.**
