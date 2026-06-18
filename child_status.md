# Child Status 52

Status: final_v4_25_page_gate
Attempt: 5
Stage: submission_hardened_exported_and_page_gated

Current facts:
- Canonical PDF target: `C:/Users/wangz/Downloads/52.pdf`.
- Canonical PDF pages: 26.
- Canonical PDF size: 331897 bytes.
- Canonical PDF SHA256: `0E6734F7C9F69E9E74E386D5EEC722020E12E11839DB0A241E518E46B13C4A6F`.
- Local generated `paper/main.pdf` is removed after build.
- Desktop PDF copy is absent.
- Full-scale suite compact rows: 432000.
- Represented evaluations: 99283968000.
- Represented frame decisions: 6354173952000.
- The v2 hidden triple stress is retained as a negative control.
- Order-calibrated protocol: MAE 0.072, false robust certification 0.051, false failure alarm 0.089, high-order recall 0.507, unsupported abstention 0.204, coverage recall 0.542, utility 0.768.
- Oracle true-order law: MAE 0.012, false robust certification 0.021, high-order recall 0.996, coverage recall 0.980, utility 1.000.
- Build script enforces full-scale validation and a 25-page minimum.
- Visual QA completed on rendered pages 1, 5, 16, 17, 18, 24, 25, and 26.

Decision:
- Final v4 full-scale submission artifact with 25-page gate. The paper supports order-calibrated composed-failure evaluation while explicitly excluding real-robot safety proof and universal hidden-failure discovery claims.

End time: 2026-06-19
