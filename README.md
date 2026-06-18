# Order-Calibrated Sensor Failure Compositionality

Submission-hardening version: v4 full-scale with 25-page gate.

Decision: final submission artifact.

The paper now treats sensor failure compositionality as an order-coverage evaluation problem. The v2 hidden-triple failure is retained as the negative control: fixed pairwise laws can fail badly on omitted higher-order/common-cause cells. The v3 contribution is a deterministic full-scale benchmark and an order-calibrated protocol that estimates supported interaction order, escalates when higher-order evidence appears, and abstains from robust certification when coverage is weak.

## Key Artifacts

- `paper/main.tex`: final v3 anonymous review manuscript.
- `scripts/run_full_scale_sensor_composition_suite.py`: deterministic full-scale experiment runner.
- `results/full_scale/condition_metrics.csv`: 432,000 compact condition rows.
- `results/full_scale/protocol_summary.csv`: protocol-level prediction, certification, coverage, cost, and utility summary.
- `results/full_scale/interaction_protocol_summary.csv`: interaction-regime stress results.
- `results/full_scale/coverage_protocol_summary.csv`: coverage-regime stress results.
- `results/full_scale/task_protocol_summary.csv`: task-family results.
- `results/full_scale/sensor_protocol_summary.csv`: sensor-suite results.
- `results/full_scale/validation.json`: canonical PDF and experiment validation record.
- `paper/figures/full_scale/*.pdf`: generated manuscript figures.
- `docs/final_audit.md`: final submission-hardening audit.
- `docs/full_scale_execution_plan.md`: pre-edit execution plan and final outcome.

## Main Result

The order-calibrated protocol is the best non-oracle method. It reaches MAE 0.072, RMSE 0.096, false robust certification 0.051, false failure alarm 0.089, high-order recall 0.507, coverage recall 0.542, unsupported abstention 0.204, and utility 0.768. The oracle true-order law remains best overall with utility 1.000. Pairwise composition improves over isolated and additive reporting but remains fragile under hidden high-order and cascading common-cause regimes.

Scale: 432,000 compact condition rows representing 99,283,968,000 evaluations and 6,354,173,952,000 frame decisions.

## Canonical PDF

The canonical built PDF is `C:/Users/wangz/Downloads/52.pdf`.

- Pages: 26.
- Size: 331,897 bytes.
- SHA256: `0E6734F7C9F69E9E74E386D5EEC722020E12E11839DB0A241E518E46B13C4A6F`.
- Visual QA: rendered pages 1, 5, 16, 17, 18, 24, 25, and 26.

Local generated PDFs are not tracked. The build script validates the full-scale experiment, enforces at least 25 pages, copies the generated PDF to the canonical Downloads path, records SHA256, and removes `paper/main.pdf`.

```powershell
python scripts\run_full_scale_sensor_composition_suite.py
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
```
