# Submission Version Log

## v1

- Recovery-generated mechanism paper and 2400-trial synthetic composition diagnostic.
- Compared additive and interaction-aware laws under independent, mild pairwise, and strong pairwise regimes.
- Marked as requiring revision because the interaction-aware law matched the synthetic data-generating law by construction.

## v2

- Added `scripts/v2_higher_order_stress.py`.
- Added held-out triple-failure stress with hidden higher-order/common-cause terms.
- Found pairwise MAE rises badly under omitted hidden triples.
- Reframed the claim around reporting interaction order and omitted-order stress.

## v3

- Added `scripts/run_full_scale_sensor_composition_suite.py`.
- Generated 432000 compact condition rows representing 99283968000 evaluations and 6354173952000 frame decisions.
- Added six protocol baselines: isolated marginal score, additive law, pairwise law, coverage-unaware high-order law, order-calibrated law, and oracle true-order law.
- Added interaction-regime, coverage-regime, task-family, sensor-suite, and failure-factor summaries.
- Generated LaTeX tables and PDF figures consumed directly by the manuscript.
- Rewrote `paper/main.tex` as a 24-page anonymous review manuscript.
- Exported the canonical PDF to `C:/Users/wangz/Downloads/52.pdf`.
- Recorded final PDF hash and visual QA in validation files.
