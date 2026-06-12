import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "docs" / "synthetic_composition_results.csv"


def main():
    groups = defaultdict(lambda: {"add": 0.0, "inter": 0.0, "n": 0})
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            g = groups[row["regime"]]
            g["add"] += float(row["abs_error_additive"])
            g["inter"] += float(row["abs_error_interaction"])
            g["n"] += 1
    for regime, g in groups.items():
        print(regime, round(g["add"] / g["n"], 4), round(g["inter"] / g["n"], 4), g["n"])


if __name__ == "__main__":
    main()
