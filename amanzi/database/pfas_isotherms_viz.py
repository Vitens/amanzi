#!/usr/bin/env python3
"""Generate PNG visualizations from pfas_isotherms.csv."""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml

DB_DIR = Path(__file__).parent
CSV_PATH = DB_DIR / "pfas_isotherms.csv"
FIG_DIR = DB_DIR / "pfas_isotherms_figures"
PFAS_YML = DB_DIR.parent / "parametric" / "pfas.yml"

CHAIN_LENGTH = {
    "TFA": 2, "PFBA": 4, "PFPeA": 5, "PFHxA": 6, "PFHpA": 7, "PFOA": 8,
    "PFNA": 9, "PFDA": 10, "PFUnDA": 11, "PFDoDA": 12, "PFTrDA": 13, "PFTeDA": 14,
    "PFBS": 4, "PFPeS": 5, "PFHxS": 6, "PFHpS": 7, "PFOS": 8, "PFDS": 10,
    "PFOSA": 8, "N-MeFOSAA": 8, "N-EtFOSAA": 8,
}

PFCA = {
    "TFA", "PFBA", "PFPeA", "PFHxA", "PFHpA", "PFOA", "PFNA", "PFDA",
    "PFUnDA", "PFDoDA", "PFTrDA", "PFTeDA",
}


def load_rows() -> list[dict]:
    with CSV_PATH.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def fval(row: dict, key: str) -> float | None:
    v = row.get(key, "")
    if v is None or v == "":
        return None
    return float(v)


def load_pfas_yml() -> dict[str, tuple[float, float]]:
    with PFAS_YML.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    out = {}
    for compound in data["parameters"]["_compounds"]:
        k = data["parameters"]["_compounds"][compound].get(f"{compound}_Freundlich_k", {}).get("default")
        n = data["parameters"]["_compounds"][compound].get(f"{compound}_Freundlich_1n", {}).get("default")
        if k is not None:
            out[compound] = (float(k), float(n))
    return out


def freundlich_q(ce_ng_l: np.ndarray, k: float, one_over_n: float) -> np.ndarray:
    ce_ug = ce_ng_l / 1000.0
    return k * (ce_ug ** one_over_n)


def fig01_k_by_compound(rows: list[dict]) -> None:
    by_compound: dict[str, list[float]] = defaultdict(list)
    labels: dict[str, list[str]] = defaultdict(list)
    for r in rows:
        k = fval(r, "amanzi_freundlich_k")
        if k is None or k <= 0:
            continue
        c = r["compound"]
        by_compound[c].append(k)
        labels[c].append(f"{r['source_authors'][:12]}…/{r['gac_product'][:10]}")

    compounds = sorted(by_compound.keys(), key=lambda x: CHAIN_LENGTH.get(x, 99))
    fig, ax = plt.subplots(figsize=(14, 6))
    positions = np.arange(len(compounds))
    for i, c in enumerate(compounds):
        vals = by_compound[c]
        ax.scatter([i] * len(vals), vals, alpha=0.7, s=40)
        if vals:
            ax.hlines(np.median(vals), i - 0.25, i + 0.25, colors="black", linewidth=2)
    ax.set_yscale("log")
    ax.set_xticks(positions)
    ax.set_xticklabels(compounds, rotation=45, ha="right")
    ax.set_ylabel("amanzi_freundlich_k  (µg/g)·(L/µg)^(1/n)")
    ax.set_title("Freundlich K (Amanzi units) per compound — dots = literature entries, bar = median")
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "01_freundlich_k_by_compound.png", dpi=150)
    plt.close(fig)


def fig02_one_over_n(rows: list[dict]) -> None:
    by_compound: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        n = fval(r, "amanzi_freundlich_1n")
        if n is None:
            continue
        by_compound[r["compound"]].append(n)
    compounds = sorted(by_compound.keys(), key=lambda x: CHAIN_LENGTH.get(x, 99))
    data = [by_compound[c] for c in compounds]
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.boxplot(data, tick_labels=compounds)
    ax.set_xticklabels(compounds, rotation=45, ha="right")
    ax.set_ylabel("amanzi_freundlich_1n")
    ax.set_title("Freundlich 1/n per compound (Amanzi units)")
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "02_freundlich_1n_by_compound.png", dpi=150)
    plt.close(fig)


def fig03_k_vs_chain(rows: list[dict]) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    for r in rows:
        k = fval(r, "amanzi_freundlich_k")
        if k is None or k <= 0:
            continue
        cl = CHAIN_LENGTH.get(r["compound"], 0)
        group = "PFCA" if r["compound"] in PFCA else "PFSA/precursor"
        color = "tab:blue" if group == "PFCA" else "tab:orange"
        marker = "o" if r["data_type"] != "predicted" else "x"
        alpha = 0.35 if r["data_type"] == "predicted" else 0.7
        ax.scatter(cl, k, c=color, marker=marker, alpha=alpha, s=35)
    ax.set_yscale("log")
    ax.set_xlabel("Fluorinated chain length (approx.)")
    ax.set_ylabel("amanzi_freundlich_k (log)")
    ax.set_title("Freundlich K vs chain length (○ measured, × predicted)")
    from matplotlib.lines import Line2D
    ax.legend(handles=[
        Line2D([0], [0], marker="o", color="w", markerfacecolor="tab:blue", label="PFCA measured"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="tab:orange", label="PFSA/precursor measured"),
        Line2D([0], [0], marker="x", color="gray", label="predicted"),
    ])
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "03_k_vs_chain_length.png", dpi=150)
    plt.close(fig)


def fig04_isotherm_curves(rows: list[dict]) -> None:
    ce = np.logspace(-1, 4, 200)  # ng/L
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
    for ax, compound in zip(axes, ["PFBS", "PFOA", "PFOS"]):
        ks = [fval(r, "amanzi_freundlich_k") for r in rows
              if r["compound"] == compound and fval(r, "amanzi_freundlich_k")]
        ns = [fval(r, "amanzi_freundlich_1n") for r in rows
              if r["compound"] == compound and fval(r, "amanzi_freundlich_k")]
        pairs = [(k, n) for k, n in zip(ks, ns) if k and n and k > 0]
        if not pairs:
            continue
        k_vals = [p[0] for p in pairs]
        k_min, k_med, k_max = min(k_vals), float(np.median(k_vals)), max(k_vals)
        n_med = float(np.median([p[1] for p in pairs]))
        for k, style, lbl in [(k_min, ":", "min K"), (k_med, "-", "median K"), (k_max, "--", "max K")]:
            q = freundlich_q(ce, k, n_med)
            ax.plot(ce, q, linestyle=style, label=f"{lbl}={k:.3g}")
        ax.set_xscale("log")
        ax.set_xlabel("Ce (ng/L)")
        ax.set_title(compound)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
    axes[0].set_ylabel("q (µg/g)")
    fig.suptitle("Freundlich isotherms (Amanzi units) — median 1/n, min/median/max K from literature")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "04_isotherm_curves_selected.png", dpi=150)
    plt.close(fig)


def fig05_heatmap(rows: list[dict]) -> None:
    by_src_comp: dict[tuple[str, str], list[float]] = defaultdict(list)
    for r in rows:
        k = fval(r, "amanzi_freundlich_k")
        if k is None or k <= 0:
            continue
        src = r["source_authors"].split()[0] + " " + (r["source_year"] or "")
        by_src_comp[(r["compound"], src)].append(k)
    compounds = sorted({c for c, _ in by_src_comp}, key=lambda x: CHAIN_LENGTH.get(x, 99))
    sources = sorted({s for _, s in by_src_comp})
    mat = np.full((len(compounds), len(sources)), np.nan)
    for i, c in enumerate(compounds):
        for j, s in enumerate(sources):
            vals = by_src_comp.get((c, s), [])
            if vals:
                mat[i, j] = np.median(vals)
    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(np.log10(np.where(mat > 0, mat, np.nan)), aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(sources)))
    ax.set_xticklabels(sources, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(compounds)))
    ax.set_yticklabels(compounds)
    ax.set_title("log10(amanzi_freundlich_k) — median per compound × source")
    fig.colorbar(im, ax=ax, label="log10(K)")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "05_heatmap_k_amanzi.png", dpi=150)
    plt.close(fig)


def fig06_coverage(rows: list[dict]) -> None:
    counts = defaultdict(int)
    for r in rows:
        counts[r["compound"]] += 1
    compounds = sorted(counts.keys(), key=lambda x: CHAIN_LENGTH.get(x, 99))
    vals = [counts[c] for c in compounds]
    fig, ax = plt.subplots(figsize=(12, 4))
    colors = ["tab:red" if v < 3 else "tab:green" for v in vals]
    ax.bar(compounds, vals, color=colors)
    ax.axhline(3, color="black", linestyle="--", label="minimum (3)")
    ax.set_ylabel("Number of entries")
    ax.set_title("Database coverage per compound")
    ax.set_xticks(range(len(compounds)))
    ax.set_xticklabels(compounds, rotation=45, ha="right")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG_DIR / "06_coverage_entries_per_compound.png", dpi=150)
    plt.close(fig)


def fig07_vs_pfas_yml(rows: list[dict], yml: dict) -> None:
    medians: dict[str, float] = {}
    for r in rows:
        if r["data_type"] == "predicted":
            continue
        k = fval(r, "amanzi_freundlich_k")
        if k is None or k <= 0:
            continue
        medians.setdefault(r["compound"], []).append(k)  # type: ignore
    for c in medians:
        medians[c] = float(np.median(medians[c]))  # type: ignore

    compounds = sorted(set(medians) | set(yml), key=lambda x: CHAIN_LENGTH.get(x, 99))
    lit = [medians.get(c, np.nan) for c in compounds]
    yml_k = [yml[c][0] if c in yml else np.nan for c in compounds]
    x = np.arange(len(compounds))
    w = 0.35
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(x - w / 2, lit, w, label="Literature median (measured)", color="steelblue")
    ax.bar(x + w / 2, yml_k, w, label="pfas.yml default (Polanyi)", color="coral")
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(compounds, rotation=45, ha="right")
    ax.set_ylabel("amanzi_freundlich_k")
    ax.set_title("Literature vs pfas.yml Freundlich K")
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "07_literature_vs_pfas_yml.png", dpi=150)
    plt.close(fig)


def fig08_measured_vs_predicted(rows: list[dict]) -> None:
    by_type: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        k = fval(r, "amanzi_freundlich_k")
        if k is None or k <= 0:
            continue
        by_type[r["data_type"]].append(k)
    fig, ax = plt.subplots(figsize=(8, 5))
    labels = list(by_type.keys())
    ax.boxplot([by_type[l] for l in labels], tick_labels=labels)
    ax.set_yscale("log")
    ax.set_ylabel("amanzi_freundlich_k")
    ax.set_title("Freundlich K by data_type")
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "08_measured_vs_predicted.png", dpi=150)
    plt.close(fig)


def main() -> None:
    FIG_DIR.mkdir(exist_ok=True)
    rows = load_rows()
    yml = load_pfas_yml()
    fig01_k_by_compound(rows)
    fig02_one_over_n(rows)
    fig03_k_vs_chain(rows)
    fig04_isotherm_curves(rows)
    fig05_heatmap(rows)
    fig06_coverage(rows)
    fig07_vs_pfas_yml(rows, yml)
    fig08_measured_vs_predicted(rows)
    print(f"Wrote 8 figures to {FIG_DIR}")


if __name__ == "__main__":
    main()
