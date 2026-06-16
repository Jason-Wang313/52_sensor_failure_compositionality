# Claims

## Core Claim

Robust robot perception should evaluate sensor failures as composed interaction laws with explicit order coverage. A robustness report should not certify composed-failure behavior from isolated corruptions or fixed low-order laws unless measured cells support the claimed interaction order.

## Supported After V3

- Isolated marginal reporting has high false robust certification: 0.431.
- Additive composition reduces little: false robust certification 0.395 and utility -0.040.
- Pairwise composition is a real baseline but not sufficient: false robust certification 0.245 and utility 0.280.
- Coverage-unaware high-order fitting improves MAE but remains weaker than calibrated evaluation: false robust certification 0.160, cost 0.349, utility 0.421.
- The order-calibrated protocol is the best non-oracle method: MAE 0.072, false robust certification 0.051, high-order recall 0.507, unsupported abstention 0.204, coverage recall 0.542, and utility 0.768.
- The oracle true-order law remains best overall: MAE 0.012, false robust certification 0.021, coverage recall 0.980, and utility 1.000.
- Under targeted high-order coverage, the calibrated protocol reaches false robust certification 0.018, high-order recall 0.865, coverage recall 0.948, and utility 1.000.
- Under cascading latent common causes, the calibrated protocol still has residual false robust certification 0.212, so the paper must present that regime as a hard boundary rather than a solved case.

## Claims To Avoid

- Do not claim real-robot safety validation.
- Do not claim the method discovers every hidden sensor failure.
- Do not claim pairwise composition is universally sufficient.
- Do not claim high-order fitting is valid without coverage.
- Do not claim the calibrated protocol beats the oracle.

## Current Boundary

The supported contribution is a deterministic full-scale benchmark and reporting discipline for order-calibrated composed sensor failure evaluation. The paper is strongest as an evaluation and certification protocol, not as a new perception backbone or deployment safety proof.
