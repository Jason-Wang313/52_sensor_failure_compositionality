# Reproducibility Checklist

- Main diagnostic generator: `scripts/run_synthetic_experiment.py`.
- V2 hardening generator: `scripts/v2_higher_order_stress.py`.
- V2 outputs: `docs/v2_higher_order_stress.json`, `docs/v2_higher_order_stress_cases.csv`, `docs/v2_higher_order_stress_summary.csv`, and `paper/v2_higher_order_table.tex`.
- Manuscript source: `paper/main.tex`.
- Build command: `powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`.
- Canonical PDF: `C:/Users/wangz/Downloads/52.pdf`.
- Local generated PDF policy: `paper/main.pdf` is ignored and removed after build.
- Desktop PDF copy: absent.
