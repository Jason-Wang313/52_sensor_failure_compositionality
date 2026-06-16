# Final Audit

Paper-readiness judgment: final v3 full-scale submission artifact.

Submission-hardening version: v3.

## Final Experiment

- Compact condition rows: 432000.
- Represented evaluations: 99283968000.
- Represented frame decisions: 6354173952000.
- Factors: 12 task families, 5 robot embodiments, 6 sensor-suite families, 8 failure-factor families, 5 interaction regimes, 5 coverage regimes, and 6 evaluation protocols.
- Each compact row represents 19 seeds, 7 policy/perception model instances, 6 scenes, 4 sensor calibrations, 3 temporal offsets, 24 trials, and 64 perception frames.

## Main Results

- Isolated marginal score: MAE 0.229, false robust certification 0.431, high-order recall 0.028, utility -0.164.
- Additive law: MAE 0.210, false robust certification 0.395, high-order recall 0.060, utility -0.040.
- Pairwise law: MAE 0.144, false robust certification 0.245, high-order recall 0.140, utility 0.280.
- Coverage-unaware high-order law: MAE 0.112, false robust certification 0.160, high-order recall 0.358, cost 0.349, utility 0.421.
- Order-calibrated law: MAE 0.072, false robust certification 0.051, false failure alarm 0.089, high-order recall 0.507, unsupported abstention 0.204, coverage recall 0.542, utility 0.768.
- Oracle true-order law: MAE 0.012, false robust certification 0.021, false failure alarm 0.029, high-order recall 0.996, coverage recall 0.980, utility 1.000.

## Coverage Stress

- Singles only: false robust certification 0.062, high-order recall 0.358, abstention 0.261, utility 0.627.
- Sparse pair coverage: false robust certification 0.055, high-order recall 0.426, abstention 0.224, utility 0.751.
- Full pair coverage: false robust certification 0.048, high-order recall 0.527, abstention 0.160, utility 0.865.
- Targeted high-order coverage: false robust certification 0.018, high-order recall 0.865, abstention 0.135, utility 1.000.
- Unknown sparse coverage: false robust certification 0.074, high-order recall 0.360, abstention 0.238, utility 0.595.

## Decision

The final paper is ready as a v3 full-scale submission artifact. It should be framed as a simulated benchmark and reporting discipline for order-calibrated composed sensor failure evaluation. It should not be framed as a real-robot safety proof or as universal hidden-failure discovery.

## Artifact Audit

- Canonical PDF: `C:/Users/wangz/Downloads/52.pdf`
- Pages: 24.
- File size: 323143 bytes.
- SHA256: `EFDC73077E60BFE5057D47BD3A0AD848F0A15D6416BF1508989B5A7CB3159C0D`.
- Visual QA pages: 1, 5, 7, 18, and 24.
- Local tracked/generated PDF policy: `paper/main.pdf` is ignored and removed after build.
- Desktop copy: absent.
- Build script: `scripts/build_pdf.ps1`
