from __future__ import annotations

import csv
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PAPER = ROOT / "paper"


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def make_rows() -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    settings = [
        ("pairwise_only", 0.0),
        ("hidden_mild_triple", 1.5),
        ("hidden_strong_triple", 4.0),
    ]
    base = 3.0
    single = 0.25
    pair = 0.15
    for regime, triple in settings:
        for a, b, c in itertools.product([0, 1], repeat=3):
            failure_count = a + b + c
            pair_count = a * b + a * c + b * c
            triple_cell = a * b * c
            true_success = sigmoid(base - single * failure_count - pair * pair_count - triple * triple_cell)
            additive = sigmoid(base - single * failure_count)
            pairwise = sigmoid(base - single * failure_count - pair * pair_count)
            full = sigmoid(base - single * failure_count - pair * pair_count - triple * triple_cell)
            rows.append(
                {
                    "regime": regime,
                    "camera_failure": a,
                    "depth_failure": b,
                    "tactile_failure": c,
                    "triple_cell": triple_cell,
                    "true_success": true_success,
                    "additive_pred": additive,
                    "pairwise_pred": pairwise,
                    "full_high_order_pred": full,
                    "abs_error_additive": abs(additive - true_success),
                    "abs_error_pairwise": abs(pairwise - true_success),
                    "abs_error_full_high_order": abs(full - true_success),
                }
            )
    return rows


def summarize(rows: list[dict[str, float | int | str]]) -> list[dict[str, float | str]]:
    out: list[dict[str, float | str]] = []
    for regime in ["pairwise_only", "hidden_mild_triple", "hidden_strong_triple"]:
        subset = [row for row in rows if row["regime"] == regime]
        triple = [row for row in subset if int(row["triple_cell"]) == 1]
        for split_name, split_rows in [("all_cells", subset), ("heldout_triple_cell", triple)]:
            out.append(
                {
                    "regime": regime,
                    "split": split_name,
                    "n": float(len(split_rows)),
                    "additive_mae": sum(float(row["abs_error_additive"]) for row in split_rows) / len(split_rows),
                    "pairwise_mae": sum(float(row["abs_error_pairwise"]) for row in split_rows) / len(split_rows),
                    "full_high_order_mae": sum(float(row["abs_error_full_high_order"]) for row in split_rows) / len(split_rows),
                }
            )
    return out


def write_outputs(rows: list[dict[str, float | int | str]], summary: list[dict[str, float | str]]) -> None:
    with (DOCS / "v2_higher_order_stress_cases.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with (DOCS / "v2_higher_order_stress_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["regime", "split", "n", "additive_mae", "pairwise_mae", "full_high_order_mae"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summary)

    (DOCS / "v2_higher_order_stress.json").write_text(
        json.dumps({"cases": rows, "summary": summary}, indent=2),
        encoding="utf-8",
    )

    display = [row for row in summary if row["split"] == "heldout_triple_cell"]
    lines = [
        r"\begin{tabular}{lrrr}",
        r"\toprule",
        r"Regime & Additive MAE & Pairwise MAE & Full high-order MAE \\",
        r"\midrule",
    ]
    labels = {
        "pairwise_only": "Pairwise only",
        "hidden_mild_triple": "Hidden mild triple",
        "hidden_strong_triple": "Hidden strong triple",
    }
    for row in display:
        lines.append(
            f"{labels[str(row['regime'])]} & "
            f"{float(row['additive_mae']):.3f} & "
            f"{float(row['pairwise_mae']):.3f} & "
            f"{float(row['full_high_order_mae']):.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    (PAPER / "v2_higher_order_table.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = make_rows()
    summary = summarize(rows)
    write_outputs(rows, summary)
    print(json.dumps({"summary": summary}, indent=2))


if __name__ == "__main__":
    main()
