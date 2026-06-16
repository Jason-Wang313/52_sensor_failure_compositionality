# Novelty Boundary Map

## What Survives

Sensor robustness evaluations should report how failures compose and which interaction order is supported by measured cells. Isolated corruption curves and missing-modality tests are marginal slices, not guarantees about composed failures.

## What V2 Exposed

The fixed pairwise law was not universal. On the held-out triple-failure cell, pairwise MAE rose to 0.284 under a hidden mild triple and 0.758 under a hidden strong triple. That result now motivates the final order-calibrated benchmark.

## What V3 Adds

- A 432000-row full-scale deterministic suite.
- Twelve task families, five robot embodiments, six sensor-suite families, eight failure factors, five interaction regimes, five coverage regimes, and six protocols.
- Protocol summaries that include MAE, RMSE, false robust certification, false failure alarm, high-order recall, unsupported abstention, coverage recall, query cost, and utility.
- Coverage-regime evidence showing that calibrated certification improves under targeted high-order coverage and becomes cautious under weak or unknown coverage.
- A 24-page anonymous review manuscript with generated tables and figures.

## Supported Framing

- Present isolated and additive reporting as high false-certification baselines.
- Present pairwise composition as useful but insufficient under omitted high-order/common-cause failures.
- Present order calibration as an evaluation protocol, not as a perception backbone.
- Emphasize that oracle true-order remains the upper bound.

## Unsafe Framing

- "Pairwise composition solves robust perception."
- "The method proves real-world robot safety."
- "The protocol discovers every hidden sensor failure."
- "High-order laws are valid without high-order coverage."
