import csv
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PAPER = ROOT / "paper"
FIGURES = PAPER / "figures"
SYNTHETIC_CSV = DOCS / "synthetic_composition_results.csv"
RELATED_CSV = DOCS / "related_work_matrix.csv"


REGIME_LABELS = {
    "independent": "Independent",
    "mild_interaction": "Mild interactions",
    "strong_interaction": "Strong interactions",
}


def count_csv_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as f:
        return sum(1 for _ in csv.DictReader(f))


def summarize_synthetic() -> list[dict[str, float | str | int]]:
    groups: dict[str, dict[str, float | int]] = defaultdict(
        lambda: {"add": 0.0, "interaction": 0.0, "true": 0.0, "n": 0}
    )
    with SYNTHETIC_CSV.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            group = groups[row["regime"]]
            group["add"] += float(row["abs_error_additive"])
            group["interaction"] += float(row["abs_error_interaction"])
            group["true"] += float(row["true_success"])
            group["n"] += 1

    summary = []
    for regime in ("independent", "mild_interaction", "strong_interaction"):
        group = groups[regime]
        n = int(group["n"])
        add = float(group["add"]) / n
        interaction = float(group["interaction"]) / n
        summary.append(
            {
                "regime": regime,
                "label": REGIME_LABELS[regime],
                "additive": add,
                "compositional": interaction,
                "gap": add - interaction,
                "mean_success": float(group["true"]) / n,
                "n": n,
            }
        )
    return summary


def write_figure(summary: list[dict[str, float | str | int]]) -> bool:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return False

    FIGURES.mkdir(parents=True, exist_ok=True)
    labels = [str(row["label"]).replace(" interactions", "") for row in summary]
    additive = [float(row["additive"]) for row in summary]
    compositional = [float(row["compositional"]) for row in summary]
    xs = list(range(len(summary)))
    width = 0.34

    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.bar([x - width / 2 for x in xs], additive, width, label="Additive", color="#4C78A8")
    ax.bar([x + width / 2 for x in xs], compositional, width, label="Compositional", color="#F58518")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Mean absolute error")
    ax.set_ylim(0, max(additive) * 1.25 if max(additive) else 0.1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(FIGURES / "composition_error_bars.png", dpi=180)
    plt.close(fig)
    return True


def table_rows(summary: list[dict[str, float | str | int]]) -> str:
    lines = []
    for row in summary:
        lines.append(
            f"{row['label']} & {int(row['n'])} & {float(row['additive']):.4f} & "
            f"{float(row['compositional']):.4f} & {float(row['gap']):.4f} \\\\"
        )
    return "\n".join(lines)


def write_paper(summary: list[dict[str, float | str | int]], related_rows: int, figure_written: bool) -> None:
    for filename in ("iclr2026_conference.sty", "iclr2026_conference.bst", "math_commands.tex"):
        shutil.copy2(ROOT / filename, PAPER / filename)

    mild = next(row for row in summary if row["regime"] == "mild_interaction")
    strong = next(row for row in summary if row["regime"] == "strong_interaction")
    figure_block = ""
    if figure_written:
        figure_block = r"""
\begin{figure}[t]
\centering
\includegraphics[width=0.82\linewidth]{figures/composition_error_bars.png}
\caption{Prediction error rises only when failures interact. The additive model is perfect under independent failures, but its error grows under mild and strong composed-failure regimes.}
\label{fig:composition-errors}
\end{figure}
"""

    tex = rf"""\documentclass{{article}}

\usepackage{{iclr2026_conference,times}}
\input{{math_commands.tex}}
\usepackage{{hyperref}}
\usepackage{{url}}
\usepackage{{graphicx}}
\usepackage{{booktabs}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{array}}
\usepackage{{enumitem}}

\title{{Sensor Failure Compositionality:\\Why Robust Robot Perception Needs Interaction Laws}}

\author{{Anonymous Authors}}

\newcommand{{\method}}{{\textsc{{CompFail}}}}
\newcommand{{\fvec}}{{\mathbf{{f}}}}

\begin{{document}}
\maketitle

\begin{{abstract}}
Robotic perception robustness is often evaluated one sensor failure, one corruption family, or one missing-modality pattern at a time. That practice assumes, usually without saying so, that failure effects compose approximately additively. We argue that this assumption is the wrong unit of analysis for embodied systems: failures in cameras, depth, LiDAR, tactile sensing, calibration, and timing can interact, so single-failure success is a weak predictor of composed-failure behavior. We support the claim with a {related_rows:,}-entry literature sweep, a hostile prior-work map, and a controlled synthetic study with {sum(int(row["n"]) for row in summary):,} trials. In the synthetic study, an additive failure law has mean absolute error {float(mild["additive"]):.4f} under mild interactions and {float(strong["additive"]):.4f} under strong interactions, while the interaction-aware law recovers the composed degradation exactly by construction. The contribution is a mechanism claim: robust robot perception should estimate and evaluate failure composition laws, not only isolated dropout heuristics.
\end{{abstract}}

\section{{Introduction}}

Robots rarely lose exactly one sensing pathway in isolation. Cameras degrade under glare and blur, LiDAR becomes sparse under rain or reflectance changes, depth sensors fail near transparent surfaces, tactile arrays saturate near contact edges, and calibration or timing errors can couple those failures across modalities. Yet much of the robustness literature still reports one corruption at a time or uses modality dropout as a training regularizer rather than as an object of study.

This paper makes a narrow thesis:
\begin{{quote}}
Sensor failure behavior in embodied perception is often non-additive, so robustness should be modeled and evaluated as a composition law over failure factors.
\end{{quote}}

The thesis matters because a system that survives each isolated failure may still fail when two mild failures coincide. Conversely, redundancy can mask one failure when a complementary sensor remains healthy. Both cases are invisible if evaluation stops at the single-failure boundary.

\section{{Related Work and Novelty Boundary}}

The literature sweep for this project covers {related_rows:,} candidate papers, including missing-modality learning, sensor-corruption benchmarks, robust fusion, calibration drift, and robot state-estimation work. The hostile-prior set includes nearby systems such as selective fusion, multi-sensor corruption benchmarks, missing-modality BEV perception, and modality-unavailability evaluations. These works make general sensor robustness, dropout training, and benchmark enumeration non-novel.

The remaining gap is the explicit interaction law. Existing papers often ask whether a method survives a named corruption or absent modality. We ask whether composed failures obey an additive degradation model and how badly robustness claims are miscalibrated when that model is false.

\section{{Compositional Failure Law}}

Let $\fvec \in \{{0,1\}}^m$ encode whether each sensor or failure factor is active. The isolated-failure view predicts performance from the count or independent sum of failures:
\begin{{equation}}
    \hat{{y}}_{{\mathrm{{add}}}} = g\!\left(b - \sum_i \beta_i f_i\right).
\end{{equation}}
That model is useful only if failures compose independently. A composition-aware view adds interaction structure:
\begin{{equation}}
    \hat{{y}}_{{\mathrm{{comp}}}} = g\!\left(b - \sum_i \beta_i f_i - \sum_{{i<j}} \alpha_{{ij}} f_i f_j\right).
\end{{equation}}
The pairwise form is not meant to be universal. It is a minimal diagnostic: if even low-order interactions change predicted success, then robustness evaluation should treat composed failures as first-class cells rather than extrapolating from isolated tests.

\section{{Synthetic Evidence}}

We ran a controlled synthetic experiment generated by \texttt{{scripts/run\_synthetic\_experiment.py}} and stored in \texttt{{docs/synthetic\_composition\_results.csv}}. Each regime has 800 samples, for 2,400 total trials. The independent regime sets all interaction penalties to zero. The mild and strong regimes add increasingly large pairwise penalties. We compare an additive predictor to an interaction-aware predictor that is given the correct composed form.

\begin{{table}}[t]
\centering
\caption{{Mean absolute prediction error across synthetic failure regimes. The additive baseline ignores interaction terms; the compositional predictor uses the correct interaction law.}}
\label{{tab:synthetic}}
\begin{{tabular}}{{lrrrr}}
\toprule
Regime & Trials & Additive error & Compositional error & Gap \\
\midrule
{table_rows(summary)}
\bottomrule
\end{{tabular}}
\end{{table}}
{figure_block}

The pattern is deliberately simple. When failures are independent, the additive view is exact. Once interactions appear, additive prediction error increases from {float(mild["additive"]):.4f} to {float(strong["additive"]):.4f}. The compositional predictor has zero error in this controlled diagnostic because its hypothesis class matches the data-generating law. The point is not that real robots will have zero-error pairwise laws; the point is that the additive assumption is empirically testable and can fail cleanly.

\section{{Implications}}

The practical implication is to change what robustness reports measure. A single-sensor dropout curve should be treated as a marginal slice, not a robustness guarantee. A better protocol should enumerate composed-failure cells, estimate an interaction model, and report where single-failure extrapolation breaks.

This also changes model selection. A larger fusion network is not automatically more robust if it improves isolated corruption scores while leaving composed-failure behavior unexplained. Likewise, a benchmark is incomplete if it lists corruptions but does not ask whether their effects are additive, redundant, or super-additive.

\section{{Limitations}}

The evidence here is synthetic and therefore cannot establish transfer to all robot perception systems. The paper is strongest as a mechanism note and weakest as a deployment claim. A real-robot follow-up should evaluate camera-depth-LiDAR-tactile combinations under paired corruptions, calibration drift, and asynchronous dropout, then fit the low-order and high-order interaction terms actually observed.

\section{{Conclusion}}

Sensor failure compositionality is a sharper organizing principle than isolated dropout heuristics for robust robot perception. The core novelty is not the existence of robustness work, missing-modality work, or sensor-corruption benchmarks. It is the claim that the central object should be the failure composition law. Once interactions exist, additive robustness claims become systematically miscalibrated, and composed-failure evaluation becomes necessary rather than optional.

\begin{{thebibliography}}{{9}}
\bibitem[Chen et~al.(2019)]{{selectfusion}}
Changhao Chen, Stefano Rosa, Chris Xiaoxuan Lu, Bing Wang, Niki Trigoni, and Andrew Markham.
\newblock Learning selective sensor fusion for states estimation.
\newblock 2019.

\bibitem[Hao et~al.(2025)]{{mscb}}
Xiaoshuai Hao, Guanqun Liu, Yuting Zhao, Yuheng Ji, Mengchuan Wei, Haimei Zhao, Lingdong Kong, and Rong Yin.
\newblock MSC-Bench: Benchmarking and analyzing multi-sensor corruption for driving perception.
\newblock 2025.

\bibitem[Wang et~al.(2023)]{{unibev}}
Shiming Wang, Holger Caesar, Liangliang Nan, and Julian F. P. Kooij.
\newblock UniBEV: Multi-modal 3D object detection with uniform BEV encoders for robustness against missing sensor modalities.
\newblock 2023.

\bibitem[Zheng et~al.(2026)]{{mutebench}}
Wugeng Zheng, Ziwen Kan, Tianlong Chen, Chen Chen, and Song Wang.
\newblock MuteBench: Modality unavailability tolerance evaluation for incomplete multimodal fusion.
\newblock 2026.
\end{{thebibliography}}

\end{{document}}
"""
    (PAPER / "main.tex").write_text(tex, encoding="utf-8")


def write_readme(summary: list[dict[str, float | str | int]], related_rows: int) -> None:
    lines = [
        "# Sensor Failure Compositionality",
        "",
        "Paper 52 for the robotics 60-paper batch.",
        "",
        "## Recovery artifacts",
        "",
        f"- Literature sweep rows: {related_rows}",
        f"- Synthetic trials: {sum(int(row['n']) for row in summary)}",
        "- Manuscript source: `paper/main.tex`",
        "- Build output: `paper/main.pdf`",
        "",
        "## Synthetic summary",
        "",
        "| Regime | Trials | Additive MAE | Compositional MAE | Gap |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(
            f"| {row['label']} | {int(row['n'])} | {float(row['additive']):.4f} | "
            f"{float(row['compositional']):.4f} | {float(row['gap']):.4f} |"
        )
    lines.append("")
    lines.append("The core claim is that robot perception failures should be evaluated as composed interaction laws, not inferred from isolated dropout cases.")
    (ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_status(summary: list[dict[str, float | str | int]], related_rows: int) -> None:
    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    status = f"""# Child Status 52

Status: recovered
Attempt: manual recovery after two runner attempts
Stage: paper rebuilt and ready for PDF compilation
Last update: {now}
Current facts:
- Literature sweep rows: {related_rows}.
- Synthetic experiment rows: {sum(int(row["n"]) for row in summary)}.
- Additive MAE under mild interactions: {float(next(row for row in summary if row["regime"] == "mild_interaction")["additive"]):.4f}.
- Additive MAE under strong interactions: {float(next(row for row in summary if row["regime"] == "strong_interaction")["additive"]):.4f}.
Recovery steps:
- Reused generated literature and synthetic CSV artifacts.
- Wrote clean ICLR manuscript in paper/main.tex.
- Added reproducible recovery script scripts/recover_paper52.py.
"""
    (ROOT / "child_status.md").write_text(status, encoding="utf-8")


def write_audit(summary: list[dict[str, float | str | int]], related_rows: int) -> None:
    strong = next(row for row in summary if row["regime"] == "strong_interaction")
    audit = f"""# Final Audit

1. chosen thesis: sensor failures in robot perception compose nonlinearly, so robustness must model interaction laws rather than isolated failures.
2. field assumption broken: failure cases are independent or additively decomposable.
3. new central mechanism: compositional failure modeling with explicit interaction terms and composed-failure evaluation.
4. genuine novelty: shifts the unit of analysis from one corruption at a time to failure compositions and their degradation law.
5. closest hostile prior work: missing-modality, sensor-corruption, and robust fusion benchmarks/methods such as MSC-Bench, MuteBench, RoboBEV, UniBEV, MMRNet, and recent resilient sensor-fusion papers.
6. literature coverage: {related_rows:,}-entry sweep; hostile prior map in `docs/hostile_prior_work.md`.
7. proof/formal-claim status if any: no formal theorem; empirical mechanism claim only, supported by a controlled synthetic compositional-failure experiment.
8. strongest evidence: additive prediction error reaches {float(strong["additive"]):.4f} under the strong-interaction synthetic regime while the interaction-aware law has {float(strong["compositional"]):.4f} error.
9. biggest weaknesses: currently limited empirical evidence and no real-robot dataset proving generality.
10. paper-readiness judgment: recovered workshop-style mechanism paper; revise before archival submission.
11. exact Downloads PDF path: `C:/Users/wangz/Downloads/52.pdf`.
12. GitHub URL: pending push.
13. whether the PDF was copied to the visible Desktop by the orchestrator: pending orchestrator copy.
"""
    (DOCS / "final_audit.md").write_text(audit, encoding="utf-8")


def main() -> None:
    PAPER.mkdir(exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    summary = summarize_synthetic()
    related_rows = count_csv_rows(RELATED_CSV)
    figure_written = write_figure(summary)
    write_paper(summary, related_rows, figure_written)
    write_readme(summary, related_rows)
    write_status(summary, related_rows)
    write_audit(summary, related_rows)
    print(f"Recovered paper 52 with {related_rows} literature rows and {sum(int(row['n']) for row in summary)} synthetic trials.")
    for row in summary:
        print(f"{row['regime']}: add={float(row['additive']):.4f} comp={float(row['compositional']):.4f} n={int(row['n'])}")


if __name__ == "__main__":
    main()
