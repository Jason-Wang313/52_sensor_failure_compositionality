# Novelty Decision

Decision after v3 hardening: final full-scale submission artifact.

Reason: The earlier mechanism note has been expanded into a broad deterministic benchmark with explicit order calibration, coverage regimes, high-order/common-cause stress, multiple protocol baselines, generated tables, generated figures, and a 24-page manuscript. The claim is now substantial enough for submission when framed as a simulated composed-failure evaluation benchmark rather than a real-robot safety proof.

## Surviving Contribution

- Measure false robust certification for composed sensor failures.
- Treat interaction order as a reported property of the evaluation, not an implicit assumption.
- Use coverage to decide whether pairwise or high-order certification is supported.
- Abstain or escalate when composed cells are outside measured support.
- Compare calibrated evaluation against isolated, additive, pairwise, high-order-unaware, and oracle protocols.

## Novelty Boundary

The paper contributes a benchmark, metric contract, and order-calibrated reporting protocol for robot perception robustness. It is not a new fusion backbone, a real-robot deployment guarantee, or a universal hidden-failure discovery method.
