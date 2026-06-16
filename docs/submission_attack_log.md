# Submission Attack Log

## Attack: fixed pairwise law fails on hidden triples

Result: Addressed by v3 order calibration. Pairwise remains a baseline, and the final method calibrates supported order and abstains under weak coverage.

Decision impact: pairwise sufficiency is not claimed.

## Attack: high-order law is only valid when coverage exists

Result: Addressed. The benchmark includes coverage regimes and reports unsupported abstention. Targeted high-order coverage gives utility 1.000, while weak coverage lowers utility and increases abstention.

Decision impact: keep coverage stress in the main paper.

## Attack: synthetic benchmark cannot prove deployment safety

Result: Sustained. The final paper identifies the benchmark as simulated and deterministic.

Decision impact: do not claim real-robot safety.

## Attack: cascading common causes remain hard

Result: Sustained as a boundary. Calibrated false robust certification is still 0.212 under cascading latent common causes.

Decision impact: present this as residual risk and future work.

## Attack: oracle should dominate

Result: Passed. Oracle utility is 1.000 and remains best overall; order-calibrated utility is 0.768 and best non-oracle.

Decision impact: preserve oracle table row.
