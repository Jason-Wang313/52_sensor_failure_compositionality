import csv
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs"
OUT_CSV = OUT_DIR / "synthetic_composition_results.csv"


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def main():
    random.seed(7)
    OUT_DIR.mkdir(exist_ok=True)

    rows = []
    settings = [
        ("independent", 0.0),
        ("mild_interaction", 0.8),
        ("strong_interaction", 1.8),
    ]

    for regime, interaction in settings:
        for n_failures in range(4):
            for _ in range(200):
                base = 2.2
                failure_a = random.choice([0.0, 1.0])
                failure_b = random.choice([0.0, 1.0])
                failure_c = random.choice([0.0, 1.0])
                composed = failure_a + failure_b + failure_c
                interaction_term = interaction * (failure_a * failure_b + failure_b * failure_c + failure_a * failure_c)
                logit = base - 1.1 * composed - interaction_term
                p_true = sigmoid(logit)
                pred_additive = sigmoid(base - 1.1 * composed)
                pred_interaction = sigmoid(base - 1.1 * composed - interaction_term)
                rows.append(
                    {
                        "regime": regime,
                        "composed_failures": int(composed),
                        "true_success": p_true,
                        "additive_pred": pred_additive,
                        "interaction_pred": pred_interaction,
                        "abs_error_additive": abs(pred_additive - p_true),
                        "abs_error_interaction": abs(pred_interaction - p_true),
                    }
                )

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {OUT_CSV}")


if __name__ == "__main__":
    main()
