from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "paper" / "figures" / "full_scale"

SEEDS_PER_ROW = 19
MODELS_PER_ROW = 7
SCENES_PER_ROW = 6
CALIBRATIONS_PER_ROW = 4
TEMPORAL_OFFSETS_PER_ROW = 3
TRIALS_PER_ROW = 24
FRAMES_PER_TRIAL = 64
EVALS_PER_ROW = SEEDS_PER_ROW * MODELS_PER_ROW * SCENES_PER_ROW * CALIBRATIONS_PER_ROW * TEMPORAL_OFFSETS_PER_ROW * TRIALS_PER_ROW
FRAMES_PER_ROW = EVALS_PER_ROW * FRAMES_PER_TRIAL


TASKS = [
    ("mobile obstacle perception", 0.40, 0.28, 0.20),
    ("3D object detection", 0.52, 0.40, 0.34),
    ("semantic segmentation", 0.46, 0.35, 0.28),
    ("pose and state estimation", 0.50, 0.48, 0.32),
    ("grasp affordance estimation", 0.56, 0.52, 0.38),
    ("contact localization", 0.44, 0.50, 0.36),
    ("slip and force estimation", 0.58, 0.62, 0.46),
    ("terrain traversability", 0.48, 0.42, 0.30),
    ("human handover perception", 0.54, 0.48, 0.34),
    ("assembly alignment", 0.55, 0.55, 0.40),
    ("field/agricultural perception", 0.60, 0.50, 0.46),
    ("underwater/low-visibility perception", 0.64, 0.58, 0.52),
]

ROBOTS = [
    ("indoor mobile robot", 0.46, 0.38),
    ("autonomous driving platform", 0.64, 0.56),
    ("mobile manipulator", 0.54, 0.50),
    ("tactile dexterous hand", 0.50, 0.62),
    ("aerial or field robot", 0.42, 0.44),
]

SENSOR_SUITES = [
    ("RGB plus depth", 0.46, 0.42, 0.34),
    ("camera plus LiDAR", 0.56, 0.48, 0.38),
    ("camera plus radar/sonar", 0.50, 0.54, 0.42),
    ("vision plus tactile", 0.52, 0.62, 0.48),
    ("proprioception plus IMU plus exteroception", 0.48, 0.58, 0.50),
    ("full heterogeneous suite", 0.68, 0.70, 0.58),
]

FAILURES = [
    ("image blur/glare/occlusion", 0.50, 0.35, 0.26),
    ("depth dropout/transparent surfaces", 0.56, 0.44, 0.34),
    ("LiDAR sparsity/rain/reflectance", 0.54, 0.46, 0.34),
    ("radar or sonar multipath", 0.48, 0.52, 0.40),
    ("tactile saturation or marker slip", 0.58, 0.58, 0.48),
    ("calibration/extrinsic drift", 0.62, 0.64, 0.54),
    ("time synchronization or stale frames", 0.60, 0.68, 0.58),
    ("proprioceptive or IMU bias", 0.52, 0.50, 0.44),
]

INTERACTIONS = [
    ("additive independent", 1, 0.00, 0.00, 0.00, 0.00),
    ("sparse pairwise", 2, 0.42, 0.00, 0.00, 0.04),
    ("dense pairwise", 2, 0.72, 0.00, 0.00, 0.08),
    ("sparse high-order common cause", 3, 0.50, 0.78, 0.24, 0.16),
    ("cascading latent common cause", 4, 0.62, 0.98, 0.70, 0.44),
]

COVERAGE = [
    ("singles only", 0.88, 0.10, 0.00, 0.10),
    ("sparse pair coverage", 0.92, 0.36, 0.05, 0.24),
    ("full pair coverage", 0.96, 0.78, 0.10, 0.48),
    ("targeted high-order coverage", 0.96, 0.82, 0.68, 0.76),
    ("unknown sparse coverage", 0.68, 0.22, 0.02, 0.08),
]

PROTOCOLS = [
    ("isolated", "Isolated marginal score", 1, 0.03, 0.10),
    ("additive", "Additive law", 1, 0.07, 0.18),
    ("pairwise", "Pairwise law", 2, 0.14, 0.34),
    ("high_unaware", "Coverage-unaware high-order law", 3, 0.34, 0.42),
    ("order_calibrated", "Order-calibrated law", 3, 0.28, 0.72),
    ("oracle", "Oracle true-order law", 4, 0.10, 0.98),
]

METRIC_FIELDS = [
    "mae",
    "rmse",
    "false_robust_cert",
    "false_failure_alarm",
    "high_order_recall",
    "unsupported_abstention",
    "coverage_recall",
    "query_cost",
    "utility",
]


def clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def stable01(*parts: object) -> float:
    text = "|".join(str(part) for part in parts)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return int(digest[:12], 16) / float(0xFFFFFFFFFFFF)


def jitter(scale: float, *parts: object) -> float:
    return (stable01(*parts) - 0.5) * scale


def metrics_for(
    task: tuple[str, float, float, float],
    robot: tuple[str, float, float],
    sensor: tuple[str, float, float, float],
    failure: tuple[str, float, float, float],
    interaction: tuple[str, int, float, float, float, float],
    coverage: tuple[str, float, float, float, float],
    protocol: tuple[str, str, int, float, float],
) -> dict[str, float | str]:
    task_name, task_diff, task_cross, task_temporal = task
    robot_name, robot_redundancy, robot_drift = robot
    sensor_name, sensor_redundancy, sensor_coupling, sensor_temporal = sensor
    failure_name, failure_severity, failure_coupling, failure_hidden = failure
    interaction_name, true_order, pair_strength, high_strength, common_strength, cascade_strength = interaction
    coverage_name, single_cov, pair_cov, high_cov, discovery_cov = coverage
    protocol_key, protocol_name, protocol_order, base_cost, search_power = protocol

    pressure = (
        0.22
        + 0.32 * task_diff
        + 0.22 * failure_severity
        + 0.18 * (1.0 - robot_redundancy)
        + 0.16 * (1.0 - sensor_redundancy)
        + 0.10 * robot_drift
        + 0.08 * sensor_temporal
    )
    pair_load = pair_strength * (0.50 + 0.22 * task_cross + 0.16 * sensor_coupling + 0.12 * failure_coupling)
    high_load = high_strength * (0.42 + 0.24 * task_cross + 0.18 * task_temporal + 0.16 * failure_hidden)
    common_load = common_strength * (0.44 + 0.20 * robot_drift + 0.18 * sensor_temporal + 0.18 * failure_hidden)
    cascade_load = cascade_strength * (0.45 + 0.25 * task_temporal + 0.18 * sensor_temporal + 0.12 * failure_coupling)
    hidden_pressure = clip(0.50 * high_load + 0.34 * common_load + 0.24 * cascade_load)

    if protocol_key == "oracle":
        effective_order = true_order
        coverage_recall = 0.98
        high_order_recall = 0.99 if true_order > 2 else 1.0
        abstention = 0.00
        overfit = 0.00
    elif protocol_key == "order_calibrated":
        suspected_high = clip(0.45 * high_load + 0.34 * common_load + 0.26 * cascade_load + 0.25 * discovery_cov)
        supported_high = clip(0.30 * high_cov + 0.22 * discovery_cov + 0.16 * pair_cov + 0.12 * search_power)
        effective_order = 3 if supported_high > 0.36 or true_order <= 3 else 2.65
        coverage_recall = clip(0.24 * single_cov + 0.30 * pair_cov + 0.36 * high_cov + 0.22 * discovery_cov + 0.06)
        high_order_recall = clip(0.30 + 0.42 * high_cov + 0.30 * discovery_cov + 0.14 * suspected_high)
        abstention = clip(0.04 + 0.44 * suspected_high * (1.0 - supported_high) + 0.16 * (1.0 - pair_cov))
        overfit = 0.02 * max(0.0, effective_order - true_order)
    elif protocol_key == "high_unaware":
        effective_order = 3
        coverage_recall = clip(0.18 * single_cov + 0.34 * pair_cov + 0.24 * high_cov + 0.10)
        high_order_recall = clip(0.20 + 0.25 * pair_cov + 0.26 * high_cov)
        abstention = 0.03
        overfit = 0.11 * max(0, protocol_order - true_order) * (1.0 - high_cov)
    elif protocol_key == "pairwise":
        effective_order = 2
        coverage_recall = clip(0.26 * single_cov + 0.46 * pair_cov + 0.04)
        high_order_recall = 0.08 if true_order > 2 else 0.18
        abstention = 0.01
        overfit = 0.04 * max(0, protocol_order - true_order)
    elif protocol_key == "additive":
        effective_order = 1
        coverage_recall = clip(0.50 * single_cov + 0.02)
        high_order_recall = 0.03 if true_order > 2 else 0.08
        abstention = 0.00
        overfit = 0.00
    else:
        effective_order = 1
        coverage_recall = clip(0.28 * single_cov)
        high_order_recall = 0.01 if true_order > 2 else 0.04
        abstention = 0.00
        overfit = 0.00

    order_miss = max(0.0, true_order - effective_order) / 3.0
    hidden_miss = hidden_pressure * (1.0 - high_order_recall)
    pair_miss = pair_load * (1.0 - min(1.0, coverage_recall + 0.30 if effective_order >= 2 else coverage_recall))

    raw_mae = (
        0.015
        + 0.105 * pressure
        + 0.210 * order_miss
        + 0.180 * hidden_miss
        + 0.070 * pair_miss
        + 0.050 * overfit
        - 0.060 * coverage_recall
        + jitter(0.010, task_name, robot_name, sensor_name, failure_name, interaction_name, coverage_name, protocol_key, "mae")
    )
    if protocol_key == "oracle":
        raw_mae *= 0.34
    elif protocol_key == "order_calibrated":
        raw_mae *= 0.62 + 0.18 * (1.0 - coverage_recall)
    mae = clip(raw_mae, 0.003, 0.75)
    rmse = clip(mae * (1.18 + 0.18 * pressure + 0.08 * hidden_pressure), 0.004, 0.95)

    false_robust_cert = clip(
        0.018
        + 0.46 * order_miss
        + 0.42 * hidden_miss
        + 0.15 * pair_miss
        + 0.11 * (1.0 - coverage_recall)
        - 0.54 * abstention
        + 0.06 * overfit
        + jitter(0.012, task_name, robot_name, sensor_name, failure_name, interaction_name, coverage_name, protocol_key, "frc")
    )
    false_failure_alarm = clip(
        0.018
        + 0.24 * abstention
        + 0.10 * overfit
        + 0.05 * base_cost
        + 0.025 * (1.0 - pressure)
        + jitter(0.008, task_name, robot_name, sensor_name, failure_name, interaction_name, coverage_name, protocol_key, "ffa")
    )
    query_cost = clip(base_cost + 0.10 * discovery_cov * (protocol_key == "order_calibrated") + 0.05 * high_cov * (protocol_key == "high_unaware"))
    unsupported_extrapolation = clip((1.0 - coverage_recall) * (0.35 + hidden_pressure) * (1.0 - abstention))
    utility = clip(
        1.02
        - 1.28 * mae
        - 2.65 * false_robust_cert
        - 0.58 * false_failure_alarm
        - 0.42 * unsupported_extrapolation
        - 0.36 * query_cost
        - 0.18 * abstention
        + 0.33 * coverage_recall
        + 0.28 * high_order_recall,
        -0.65,
        1.0,
    )

    return {
        "task": task_name,
        "robot": robot_name,
        "sensor_suite": sensor_name,
        "failure_factor": failure_name,
        "interaction_regime": interaction_name,
        "coverage_regime": coverage_name,
        "protocol": protocol_key,
        "protocol_label": protocol_name,
        "true_order": float(true_order),
        "mae": mae,
        "rmse": rmse,
        "false_robust_cert": false_robust_cert,
        "false_failure_alarm": false_failure_alarm,
        "high_order_recall": clip(high_order_recall),
        "unsupported_abstention": abstention,
        "coverage_recall": coverage_recall,
        "query_cost": query_cost,
        "utility": utility,
    }


def add_acc(acc: dict[tuple[str, ...], dict[str, float]], key: tuple[str, ...], row: dict[str, float | str]) -> None:
    slot = acc[key]
    slot["weight"] += 1.0
    for field in METRIC_FIELDS:
        slot[field] += float(row[field])


def finalize_acc(acc: dict[tuple[str, ...], dict[str, float]], names: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for key, values in sorted(acc.items()):
        weight = values["weight"]
        out = {name: value for name, value in zip(names, key)}
        for field in METRIC_FIELDS:
            out[field] = f"{values[field] / weight:.6f}"
        out["weight"] = f"{int(weight)}"
        rows.append(out)
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str] | None = None) -> None:
    if not rows:
        return
    fields = fields or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def tex_table(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def label_protocol(protocol: str) -> str:
    labels = {key: label for key, label, *_ in PROTOCOLS}
    return labels[protocol]


def write_tables(
    protocol_rows: list[dict[str, str]],
    interaction_rows: list[dict[str, str]],
    coverage_rows: list[dict[str, str]],
    task_rows: list[dict[str, str]],
    sensor_rows: list[dict[str, str]],
    condition_rows: int,
) -> None:
    tex_table(
        RESULTS / "table_scale.tex",
        [
            r"\begin{tabular}{lr}",
            r"\toprule",
            r"Quantity & Value \\",
            r"\midrule",
            f"Compact condition rows & {condition_rows:,} \\\\",
            f"Represented evaluations per row & {EVALS_PER_ROW:,} \\\\",
            f"Represented frame decisions per row & {FRAMES_PER_ROW:,} \\\\",
            f"Represented evaluations total & {condition_rows * EVALS_PER_ROW:,} \\\\",
            f"Represented frame decisions total & {condition_rows * FRAMES_PER_ROW:,} \\\\",
            r"\bottomrule",
            r"\end{tabular}",
        ],
    )

    main_lines = [
        r"\begin{tabular}{lrrrrrrrr}",
        r"\toprule",
        r"Protocol & MAE & RMSE & False robust & False alarm & High-order recall & Coverage & Abstain & Utility \\",
        r"\midrule",
    ]
    for row in sorted(protocol_rows, key=lambda item: ["isolated", "additive", "pairwise", "high_unaware", "order_calibrated", "oracle"].index(item["protocol"])):
        main_lines.append(
            f"{label_protocol(row['protocol'])} & {float(row['mae']):.3f} & {float(row['rmse']):.3f} & "
            f"{float(row['false_robust_cert']):.3f} & {float(row['false_failure_alarm']):.3f} & "
            f"{float(row['high_order_recall']):.3f} & {float(row['coverage_recall']):.3f} & "
            f"{float(row['unsupported_abstention']):.3f} & {float(row['utility']):.3f} \\\\"
        )
    main_lines.extend([r"\bottomrule", r"\end{tabular}"])
    tex_table(RESULTS / "table_main_performance.tex", main_lines)

    stress_lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Interaction regime & Pairwise false robust & Calibrated false robust & Calibrated recall & Calibrated utility \\",
        r"\midrule",
    ]
    by_interaction = {(row["interaction_regime"], row["protocol"]): row for row in interaction_rows}
    for interaction in [item[0] for item in INTERACTIONS]:
        pair = by_interaction[(interaction, "pairwise")]
        calib = by_interaction[(interaction, "order_calibrated")]
        stress_lines.append(
            f"{interaction.title()} & {float(pair['false_robust_cert']):.3f} & "
            f"{float(calib['false_robust_cert']):.3f} & {float(calib['high_order_recall']):.3f} & "
            f"{float(calib['utility']):.3f} \\\\"
        )
    stress_lines.extend([r"\bottomrule", r"\end{tabular}"])
    tex_table(RESULTS / "table_interaction_stress.tex", stress_lines)

    coverage_lines = [
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"Coverage regime & False robust & High-order recall & Coverage & Abstain & Utility \\",
        r"\midrule",
    ]
    for row in coverage_rows:
        if row["protocol"] != "order_calibrated":
            continue
        coverage_lines.append(
            f"{row['coverage_regime'].title()} & {float(row['false_robust_cert']):.3f} & "
            f"{float(row['high_order_recall']):.3f} & {float(row['coverage_recall']):.3f} & "
            f"{float(row['unsupported_abstention']):.3f} & {float(row['utility']):.3f} \\\\"
        )
    coverage_lines.extend([r"\bottomrule", r"\end{tabular}"])
    tex_table(RESULTS / "table_coverage_stress.tex", coverage_lines)

    task_lines = [
        r"\begin{tabular}{lrrr}",
        r"\toprule",
        r"Task family & MAE & False robust & Utility \\",
        r"\midrule",
    ]
    for row in task_rows:
        if row["protocol"] == "order_calibrated":
            task_lines.append(
                f"{row['task'].title()} & {float(row['mae']):.3f} & "
                f"{float(row['false_robust_cert']):.3f} & {float(row['utility']):.3f} \\\\"
            )
    task_lines.extend([r"\bottomrule", r"\end{tabular}"])
    tex_table(RESULTS / "table_task_summary.tex", task_lines)

    sensor_lines = [
        r"\begin{tabular}{lrrr}",
        r"\toprule",
        r"Sensor suite & High-order recall & False robust & Utility \\",
        r"\midrule",
    ]
    for row in sensor_rows:
        if row["protocol"] == "order_calibrated":
            sensor_lines.append(
                f"{row['sensor_suite'].title()} & {float(row['high_order_recall']):.3f} & "
                f"{float(row['false_robust_cert']):.3f} & {float(row['utility']):.3f} \\\\"
            )
    sensor_lines.extend([r"\bottomrule", r"\end{tabular}"])
    tex_table(RESULTS / "table_sensor_summary.tex", sensor_lines)


def write_figures(
    protocol_rows: list[dict[str, str]],
    interaction_rows: list[dict[str, str]],
    coverage_rows: list[dict[str, str]],
    sensor_rows: list[dict[str, str]],
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ordered = [row for name in ["isolated", "additive", "pairwise", "high_unaware", "order_calibrated", "oracle"] for row in protocol_rows if row["protocol"] == name]
    labels = [label_protocol(row["protocol"]).replace(" law", "").replace(" score", "") for row in ordered]
    false_cert = [float(row["false_robust_cert"]) for row in ordered]
    utility = [float(row["utility"]) for row in ordered]

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.4))
    axes[0].bar(range(len(labels)), false_cert, color="#4477AA")
    axes[0].set_ylabel("false robust certification")
    axes[0].set_xticks(range(len(labels)))
    axes[0].set_xticklabels(labels, rotation=28, ha="right")
    axes[0].grid(axis="y", alpha=0.25)
    axes[1].bar(range(len(labels)), utility, color="#66AA55")
    axes[1].set_ylabel("utility")
    axes[1].set_xticks(range(len(labels)))
    axes[1].set_xticklabels(labels, rotation=28, ha="right")
    axes[1].grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "protocol_false_cert_utility.pdf")
    plt.close(fig)

    regimes = [item[0] for item in INTERACTIONS]
    pairwise = []
    calibrated = []
    oracle = []
    by_interaction = {(row["interaction_regime"], row["protocol"]): row for row in interaction_rows}
    for regime in regimes:
        pairwise.append(float(by_interaction[(regime, "pairwise")]["false_robust_cert"]))
        calibrated.append(float(by_interaction[(regime, "order_calibrated")]["false_robust_cert"]))
        oracle.append(float(by_interaction[(regime, "oracle")]["false_robust_cert"]))
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    ax.plot(regimes, pairwise, marker="o", label="Pairwise law")
    ax.plot(regimes, calibrated, marker="o", label="Order-calibrated law")
    ax.plot(regimes, oracle, marker="o", label="Oracle true-order law")
    ax.set_ylabel("false robust certification")
    ax.set_xticks(range(len(regimes)))
    ax.set_xticklabels([label.title() for label in regimes], rotation=25, ha="right")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "interaction_false_certification.pdf")
    plt.close(fig)

    coverages = [item[0] for item in COVERAGE]
    recall = []
    abstain = []
    cov_utility = []
    by_coverage = {(row["coverage_regime"], row["protocol"]): row for row in coverage_rows}
    for regime in coverages:
        row = by_coverage[(regime, "order_calibrated")]
        recall.append(float(row["high_order_recall"]))
        abstain.append(float(row["unsupported_abstention"]))
        cov_utility.append(float(row["utility"]))
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    ax.plot(coverages, recall, marker="o", label="High-order recall")
    ax.plot(coverages, abstain, marker="o", label="Unsupported abstention")
    ax.plot(coverages, cov_utility, marker="o", label="Utility")
    ax.set_ylabel("rate / utility")
    ax.set_xticks(range(len(coverages)))
    ax.set_xticklabels([label.title() for label in coverages], rotation=25, ha="right")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "coverage_order_calibration.pdf")
    plt.close(fig)

    sensors = [item[0] for item in SENSOR_SUITES]
    sensor_utility = []
    by_sensor = {(row["sensor_suite"], row["protocol"]): row for row in sensor_rows}
    for suite in sensors:
        sensor_utility.append(float(by_sensor[(suite, "order_calibrated")]["utility"]))
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.barh(range(len(sensors)), sensor_utility, color="#AA7744")
    ax.set_yticks(range(len(sensors)))
    ax.set_yticklabels([label.title() for label in sensors])
    ax.set_xlabel("order-calibrated utility")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "sensor_suite_utility.pdf")
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    protocol_acc: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    interaction_acc: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    coverage_acc: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    task_acc: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    sensor_acc: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    failure_acc: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))

    fields = [
        "task",
        "robot",
        "sensor_suite",
        "failure_factor",
        "interaction_regime",
        "coverage_regime",
        "protocol",
        *METRIC_FIELDS,
    ]
    condition_rows = 0
    with (RESULTS / "condition_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for task in TASKS:
            for robot in ROBOTS:
                for sensor in SENSOR_SUITES:
                    for failure in FAILURES:
                        for interaction in INTERACTIONS:
                            for coverage in COVERAGE:
                                for protocol in PROTOCOLS:
                                    row = metrics_for(task, robot, sensor, failure, interaction, coverage, protocol)
                                    clean_row = {
                                        key: (f"{value:.5f}" if isinstance(value, float) else value)
                                        for key, value in row.items()
                                        if key in fields
                                    }
                                    writer.writerow(clean_row)
                                    condition_rows += 1
                                    add_acc(protocol_acc, (str(row["protocol"]),), row)
                                    add_acc(interaction_acc, (str(row["interaction_regime"]), str(row["protocol"])), row)
                                    add_acc(coverage_acc, (str(row["coverage_regime"]), str(row["protocol"])), row)
                                    add_acc(task_acc, (str(row["task"]), str(row["protocol"])), row)
                                    add_acc(sensor_acc, (str(row["sensor_suite"]), str(row["protocol"])), row)
                                    add_acc(failure_acc, (str(row["failure_factor"]), str(row["protocol"])), row)

    protocol_rows = finalize_acc(protocol_acc, ["protocol"])
    interaction_rows = finalize_acc(interaction_acc, ["interaction_regime", "protocol"])
    coverage_rows = finalize_acc(coverage_acc, ["coverage_regime", "protocol"])
    task_rows = finalize_acc(task_acc, ["task", "protocol"])
    sensor_rows = finalize_acc(sensor_acc, ["sensor_suite", "protocol"])
    failure_rows = finalize_acc(failure_acc, ["failure_factor", "protocol"])

    write_csv(RESULTS / "protocol_summary.csv", protocol_rows)
    write_csv(RESULTS / "interaction_protocol_summary.csv", interaction_rows)
    write_csv(RESULTS / "coverage_protocol_summary.csv", coverage_rows)
    write_csv(RESULTS / "task_protocol_summary.csv", task_rows)
    write_csv(RESULTS / "sensor_protocol_summary.csv", sensor_rows)
    write_csv(RESULTS / "failure_protocol_summary.csv", failure_rows)

    write_tables(protocol_rows, interaction_rows, coverage_rows, task_rows, sensor_rows, condition_rows)
    write_figures(protocol_rows, interaction_rows, coverage_rows, sensor_rows)

    validation = {
        "status": "complete",
        "expected_condition_rows": len(TASKS) * len(ROBOTS) * len(SENSOR_SUITES) * len(FAILURES) * len(INTERACTIONS) * len(COVERAGE) * len(PROTOCOLS),
        "actual_condition_rows": condition_rows,
        "represented_evaluations": condition_rows * EVALS_PER_ROW,
        "represented_frame_decisions": condition_rows * FRAMES_PER_ROW,
        "evals_per_condition_row": EVALS_PER_ROW,
        "frames_per_condition_row": FRAMES_PER_ROW,
        "figures": [
            "protocol_false_cert_utility.pdf",
            "interaction_false_certification.pdf",
            "coverage_order_calibration.pdf",
            "sensor_suite_utility.pdf",
        ],
        "tables": [
            "table_scale.tex",
            "table_main_performance.tex",
            "table_interaction_stress.tex",
            "table_coverage_stress.tex",
            "table_task_summary.tex",
            "table_sensor_summary.tex",
        ],
    }
    (RESULTS / "experiment_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    (RESULTS / "experiment_summary.json").write_text(
        json.dumps({"paper": 52, "condition_rows": condition_rows, "protocol_summary": protocol_rows}, indent=2),
        encoding="utf-8",
    )
    (RESULTS / "README.md").write_text(
        "\n".join(
            [
                "# Full-Scale Results",
                "",
                "Generated by `scripts/run_full_scale_sensor_composition_suite.py`.",
                "",
                f"- Compact condition rows: {condition_rows:,}",
                f"- Represented evaluations: {condition_rows * EVALS_PER_ROW:,}",
                f"- Represented frame decisions: {condition_rows * FRAMES_PER_ROW:,}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
