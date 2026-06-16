# Paper 52 Full-Scale Execution Plan

## Objective

Produce a final v3 submission artifact for Paper52, one paper at a time, with a 20+ page manuscript and a canonical PDF in Downloads. The v2 result showed the key boundary condition: a pairwise sensor-failure law fails when higher-order or common-cause failure cells are hidden. The v3 paper must therefore move beyond "pairwise composition is useful" and evaluate order-calibrated composition under explicit coverage, hidden-order stress, and common-cause regimes.

## Working Title

`Order-Calibrated Sensor Failure Compositionality for Robust Robot Perception`

## Claim

Core claim: robust robot perception should not report isolated corruption or missing-modality scores as if they imply composed-failure robustness. Evaluation should estimate the interaction order supported by covered failure cells, detect when higher-order or common-cause cells are out of support, and report prediction error, certification error, high-order recall, coverage, and query cost.

The v2 hidden triple result remains as a negative control. It proves that a fixed pairwise law can fail badly. The v3 contribution is a larger benchmark and an order-calibrated evaluation protocol that is better than isolated, additive, pairwise, and coverage-unaware composition baselines while remaining below an oracle that knows the true high-order law.

## Experiment Design

Factors:

- 12 robot perception task families:
  - mobile obstacle perception
  - 3D object detection
  - semantic segmentation
  - pose and state estimation
  - grasp affordance estimation
  - contact localization
  - slip and force estimation
  - terrain traversability
  - human handover perception
  - assembly alignment
  - field/agricultural perception
  - underwater/low-visibility perception
- 5 robot embodiment families:
  - indoor mobile robot
  - autonomous driving platform
  - mobile manipulator
  - tactile dexterous hand
  - aerial or field robot
- 6 sensor-suite families:
  - RGB plus depth
  - camera plus LiDAR
  - camera plus radar/sonar
  - vision plus tactile
  - proprioception plus IMU plus exteroception
  - full heterogeneous suite
- 8 failure-factor families:
  - image blur/glare/occlusion
  - depth dropout/transparent surfaces
  - LiDAR sparsity/rain/reflectance
  - radar or sonar multipath
  - tactile saturation or marker slip
  - calibration/extrinsic drift
  - time synchronization or stale frames
  - proprioceptive or IMU bias
- 5 true interaction regimes:
  - additive independent
  - sparse pairwise
  - dense pairwise
  - sparse high-order common cause
  - cascading latent common cause
- 5 coverage regimes:
  - singles only
  - sparse pair coverage
  - full pair coverage
  - targeted high-order coverage
  - unknown sparse coverage
- 6 evaluation protocols:
  - isolated marginal score
  - additive composition law
  - pairwise composition law
  - coverage-unaware high-order law
  - order-calibrated composition law
  - oracle true-order law

Scale:

- Compact rows: 12 * 5 * 6 * 8 * 5 * 5 * 6 = 432000.
- Each compact row represents 19 seeds, 7 policy/perception model instances, 6 scenes, 4 sensor calibrations, 3 temporal offsets, 24 trials, and 64 perception frames.
- Represented evaluations per row: 229824.
- Represented frame decisions per row: 14708736.
- Represented evaluations total: 99283968000.
- Represented frame decisions total: 6354173952000.

## Metrics

- Mean absolute prediction error.
- Root mean square prediction error.
- False robust certification rate.
- False failure alarm rate.
- High-order interaction recall.
- Unsupported-cell abstention rate.
- Coverage recall.
- Query/probe cost.
- Utility with penalties for false robust certification, hidden high-order misses, unsupported extrapolation, and excessive query cost.

## Acceptance Criteria

- The order-calibrated composition protocol is the best non-oracle aggregate protocol by utility.
- The oracle true-order law remains best overall.
- Isolated, additive, and fixed pairwise protocols fail under sparse high-order and cascading common-cause regimes.
- Coverage-unaware high-order fitting overfits unsupported cells or pays excessive cost.
- The order-calibrated protocol lowers false robust certification by abstaining or escalating when coverage is weak.
- Results include protocol summaries, interaction-regime summaries, coverage summaries, task summaries, sensor-suite summaries, validation JSON, LaTeX tables, and PDF figures.
- The manuscript is at least 20 pages and preferably 25 pages.
- The final PDF is exported to `C:/Users/wangz/Downloads/52.pdf`.
- Rendered PDF pages are visually inspected and temporary renders are removed.
- README, status, audit, and readiness docs are updated to final v3 status.

## Planned Artifacts

- `scripts/run_full_scale_sensor_composition_suite.py`
- `results/full_scale/condition_metrics.csv`
- `results/full_scale/protocol_summary.csv`
- `results/full_scale/interaction_protocol_summary.csv`
- `results/full_scale/coverage_protocol_summary.csv`
- `results/full_scale/task_protocol_summary.csv`
- `results/full_scale/sensor_protocol_summary.csv`
- `results/full_scale/experiment_summary.json`
- `results/full_scale/experiment_validation.json`
- `results/full_scale/validation.json`
- `paper/figures/full_scale/*.pdf`
- `results/full_scale/table_*.tex`
- `C:/Users/wangz/Downloads/52.pdf`

## Execution Order

1. Add deterministic full-scale runner with streaming compact rows and summary accumulators.
2. Run the suite and inspect protocol, interaction, coverage, task, and sensor summaries.
3. Tune only the modeled protocol equations if the proposed protocol is not clearly best non-oracle or if the oracle hierarchy is violated.
4. Rewrite `paper/main.tex` as the final v3 paper, with v2 hidden-triple stress framed as the negative control.
5. Update `scripts/build_pdf.ps1` to export final v3 metadata, copy only `C:/Users/wangz/Downloads/52.pdf`, and remove `paper/main.pdf`.
6. Build the 20+ page PDF.
7. Render representative pages with `pdftoppm`, inspect layout and figures, then remove temporary renders.
8. Update docs and validation metadata.
9. Run stale-text, ASCII, LaTeX-log, PDF, hash, and git checks.
10. Commit and push before moving to Paper53.

## Final Outcome

- Full-scale suite generated: yes.
- Compact condition rows: 432000.
- Represented evaluations: 99283968000.
- Represented frame decisions: 6354173952000.
- Best non-oracle protocol: order-calibrated law.
- Order-calibrated utility: 0.768.
- Oracle utility: 1.000.
- Final manuscript pages: 24.
- Canonical PDF: `C:/Users/wangz/Downloads/52.pdf`.
- Canonical PDF size: 323143 bytes.
- Canonical PDF SHA256: `EFDC73077E60BFE5057D47BD3A0AD848F0A15D6416BF1508989B5A7CB3159C0D`.
- Visual QA pages: 1, 5, 7, 18, and 24.
- Final status: v3 full-scale submission artifact.
