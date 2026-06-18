# Reproducibility Checklist

- Full-scale generator: `scripts/run_full_scale_sensor_composition_suite.py`.
- Full-scale outputs: `results/full_scale/condition_metrics.csv`, `protocol_summary.csv`, `interaction_protocol_summary.csv`, `coverage_protocol_summary.csv`, `task_protocol_summary.csv`, `sensor_protocol_summary.csv`, `failure_protocol_summary.csv`, `experiment_summary.json`, `experiment_validation.json`, and `validation.json`.
- Generated tables: `results/full_scale/table_scale.tex`, `table_main_performance.tex`, `table_interaction_stress.tex`, `table_coverage_stress.tex`, `table_task_summary.tex`, and `table_sensor_summary.tex`.
- Generated figures: `paper/figures/full_scale/protocol_false_cert_utility.pdf`, `interaction_false_certification.pdf`, `coverage_order_calibration.pdf`, and `sensor_suite_utility.pdf`.
- Historical diagnostic generator: `scripts/run_synthetic_experiment.py`.
- Historical v2 hardening generator: `scripts/v2_higher_order_stress.py`.
- Manuscript source: `paper/main.tex`.
- Build command: `powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1`.
- Canonical PDF: `C:/Users/wangz/Downloads/52.pdf`.
- Canonical PDF pages: 26.
- Canonical PDF SHA256: `0E6734F7C9F69E9E74E386D5EEC722020E12E11839DB0A241E518E46B13C4A6F`.
- Build gate: full-scale validation and at least 25 pages.
- Local generated PDF policy: `paper/main.pdf` is ignored and removed after build.
- Desktop PDF copy: absent.
- Visual QA pages: 1, 5, 16, 17, 18, 24, 25, and 26.
