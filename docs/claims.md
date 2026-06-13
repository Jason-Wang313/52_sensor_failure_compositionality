# Claims

## Core Claim

Sensor failures in robot perception should be evaluated as composition laws over failure factors, not only as isolated corruptions or missing-modality cases.

## Supported After V2

- The additive model is exact under independent failures in the original synthetic diagnostic.
- Additive prediction error rises to 0.0927 under mild pairwise interactions and 0.1696 under strong pairwise interactions.
- The pairwise interaction-aware law is exact only when the true data-generating law is pairwise.
- V2 hidden higher-order stress shows pairwise laws can fail badly: held-out triple-cell pairwise MAE reaches 0.758 under a strong hidden triple interaction.

## Claims To Avoid

- Do not claim pairwise interactions are sufficient in general.
- Do not claim real-robot robustness.
- Do not claim the synthetic composition law covers all sensor failures.
- Do not claim zero-error prediction outside the matched synthetic law.

## Current Boundary

The supported contribution is a mechanism/reporting claim: robust perception evaluations should state the assumed interaction order, measure composed-failure cells, and stress omitted higher-order/common-cause failures.
