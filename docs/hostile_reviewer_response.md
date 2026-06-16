# Hostile Reviewer Response

The strongest criticism is correct: the original pairwise law won because it matched the synthetic data-generating law, and v2 showed that pairwise laws can fail badly on hidden triple/common-cause cells. The v3 paper does not hide that. It makes order calibration and coverage the central mechanism.

The full-scale revision adds task families, robot embodiments, sensor suites, failure factors, true interaction regimes, coverage regimes, and protocol comparisons. The decisive change is that robust certification depends on measured interaction support. Under targeted high-order coverage, the calibrated protocol has false robust certification 0.018 and utility 1.000. Under unknown sparse coverage, it becomes more cautious, with abstention 0.238 and utility 0.595.

The paper should still concede three limits. First, the benchmark is deterministic and simulated. Second, it does not discover every hidden failure. Third, cascading latent common causes remain hard: calibrated false robust certification is still 0.212 in that regime. These limits are compatible with the submitted claim: composed sensor failure reports should calibrate interaction order before certifying robustness.
