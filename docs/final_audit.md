# Final Audit

Paper-readiness judgment: workshop-only.

Submission-hardening version: v2.

## Original Diagnostic

- 2,400 synthetic trials.
- Independent regime: additive MAE 0.0000, interaction-aware MAE 0.0000.
- Mild pairwise interaction regime: additive MAE 0.0927, interaction-aware MAE 0.0000.
- Strong pairwise interaction regime: additive MAE 0.1696, interaction-aware MAE 0.0000.

## V2 Higher-Order Stress

The hardening pass adds `scripts/v2_higher_order_stress.py`, which creates a held-out triple-failure cell with an unmodeled high-order common-cause interaction.

- Pairwise-only regime: held-out triple-cell pairwise MAE 0.000.
- Hidden mild triple: held-out triple-cell pairwise MAE 0.284.
- Hidden strong triple: held-out triple-cell pairwise MAE 0.758.
- Full high-order law remains exact because it is given the true high-order term.

## Decision

Workshop-only. The paper is honest as a mechanism note arguing that sensor robustness reports should include composition laws and composed-failure cells. It is not submit-ready as a full conference paper because the evidence is synthetic and v2 shows low-order laws fail under omitted higher-order/common-cause interactions.

## Required Future Work

- Real robot or high-fidelity multi-sensor failure data.
- Higher-order and common-cause failure coverage.
- Learned interaction-order selection rather than hand-specified laws.
- Comparisons against robust fusion, missing-modality, and sensor-corruption benchmark baselines.

## Artifact Audit

- Canonical PDF: `C:/Users/wangz/Downloads/52.pdf`
- Local tracked/generated PDF policy: `paper/main.pdf` is ignored and removed after build.
- Desktop copy: absent.
- Build script: `scripts/build_pdf.ps1`
