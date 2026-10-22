#!/usr/bin/env python3
"""Build pfas_isotherms.csv from curated literature data with Amanzi unit conversion."""

from __future__ import annotations

import csv
import math
from pathlib import Path

DB_DIR = Path(__file__).parent
CSV_PATH = DB_DIR / "pfas_isotherms.csv"

HEADER = [
    "compound", "isotherm_model", "data_type",
    "orig_freundlich_k", "orig_freundlich_exponent", "orig_freundlich_exp_type",
    "orig_langmuir_qmax", "orig_langmuir_kl",
    "orig_param_units", "orig_ce_units", "orig_q_units",
    "amanzi_freundlich_k", "amanzi_freundlich_1n",
    "amanzi_langmuir_qmax", "amanzi_langmuir_kl", "amanzi_units_note",
    "gac_brand", "gac_product", "gac_type", "gac_reactivation",
    "water_matrix", "influent_conc_min", "influent_conc_max", "influent_conc_unit",
    "is_multicomponent", "competition_notes", "matrix_notes",
    "fitting_method", "source_title", "source_authors", "source_year",
    "source_doi", "source_url", "notes",
]

COMPOUNDS = [
    "TFA", "PFBA", "PFPeA", "PFHxA", "PFHpA", "PFOA", "PFNA", "PFDA",
    "PFUnDA", "PFDoDA", "PFTrDA", "PFTeDA",
    "PFBS", "PFPeS", "PFHxS", "PFHpS", "PFOS", "PFDS",
    "PFOSA", "N-MeFOSAA", "N-EtFOSAA",
]

# Polanyi predicted values (Amanzi units) from pfas.yml / Burkhardt et al. 2023 dataset
POLANYI = {
    "TFA": (215, 0.343), "PFBA": (255, 0.494), "PFPeA": (1160, 0.425),
    "PFHxA": (4179, 0.361), "PFHpA": (498, 0.314), "PFOA": (1718, 0.281),
    "PFNA": (8500, 0.26), "PFDA": (6371, 0.242), "PFUnDA": (14603, 0.223),
    "PFDoDA": (18106, 0.2076), "PFTrDA": (25862, 0.1972), "PFTeDA": (30582, 0.186),
    "PFBS": (457, 0.411), "PFPeS": (1521, 0.352), "PFHxS": (3840, 0.313),
    "PFHpS": (4589, 0.286), "PFOS": (7222, 0.253), "PFDS": (0.1, 1.0),
    "PFOSA": (8500, 0.28), "N-MeFOSAA": (6200, 0.29), "N-EtFOSAA": (7100, 0.27),
}

POLANYI_META = {
    "source_title": "Polanyi adsorption potential theory for estimating PFAS treatment with granular activated carbon",
    "source_authors": "Burkhardt et al.",
    "source_year": "2023",
    "source_doi": "10.1016/j.jwpe.2023.103691",
    "source_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10208310/",
    "gac_brand": "generic", "gac_product": "distilled-water GAC",
    "gac_type": "coal-based", "gac_reactivation": "none",
    "water_matrix": "distilled water (predicted)",
    "influent_conc_min": "", "influent_conc_max": "", "influent_conc_unit": "",
    "is_multicomponent": "false",
    "competition_notes": "none (theoretical single-solute)",
    "matrix_notes": "Polanyi prediction; no NOM",
    "fitting_method": "Polanyi Potential Theory MCMC",
}


def _sf(v: float) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return ""
    if isinstance(v, bool):
        return str(v).lower()
    if isinstance(v, int):
        return str(v)
    if abs(v) >= 100:
        return f"{v:.4g}"
    return f"{v:.6g}"


def to_amanzi_k_ng_l(orig_k: float, one_over_n: float) -> float:
    """Convert K from (µg/g)(L/ng)^(1/n) or equivalent with Ce in ng/L."""
    return orig_k * (1000 ** one_over_n)


def to_amanzi_k_chen(orig_k: float, n: float) -> tuple[float, float]:
    """Chen 2024: Kf (ng/mg)/(ng/L)^n → Amanzi K and 1/n."""
    return orig_k * (1000 ** n), n


def to_amanzi_k_hueckstadt(orig_k: float, n: float) -> tuple[float, float]:
    """Hückstädt: KF (µg/g)/(µg/L)^n with Ce already in µg/L."""
    return orig_k, n


def to_amanzi_kl_ng(orig_kl: float) -> float:
    return orig_kl * 1000


def row(
    compound: str,
    isotherm_model: str,
    data_type: str,
    *,
    orig_k=None, orig_exp=None, orig_exp_type="1/n",
    orig_qmax=None, orig_kl=None,
    orig_units="", orig_ce="ng/L", orig_q="µg/g",
    amanzi_k=None, amanzi_1n=None, amanzi_qmax=None, amanzi_kl=None,
    gac_brand="", gac_product="", gac_type="", gac_reactivation="none",
    water_matrix="", inf_min="", inf_max="", inf_unit="ng/L",
    multicomponent="false", competition="", matrix="",
    fitting="", source_title="", source_authors="", source_year="",
    source_doi="", source_url="", notes="",
) -> dict:
    return {
        "compound": compound,
        "isotherm_model": isotherm_model,
        "data_type": data_type,
        "orig_freundlich_k": _sf(orig_k) if orig_k is not None else "",
        "orig_freundlich_exponent": _sf(orig_exp) if orig_exp is not None else "",
        "orig_freundlich_exp_type": orig_exp_type if orig_k is not None else "",
        "orig_langmuir_qmax": _sf(orig_qmax) if orig_qmax is not None else "",
        "orig_langmuir_kl": _sf(orig_kl) if orig_kl is not None else "",
        "orig_param_units": orig_units,
        "orig_ce_units": orig_ce,
        "orig_q_units": orig_q,
        "amanzi_freundlich_k": _sf(amanzi_k) if amanzi_k is not None else "",
        "amanzi_freundlich_1n": _sf(amanzi_1n) if amanzi_1n is not None else "",
        "amanzi_langmuir_qmax": _sf(amanzi_qmax) if amanzi_qmax is not None else "",
        "amanzi_langmuir_kl": _sf(amanzi_kl) if amanzi_kl is not None else "",
        "amanzi_units_note": "K:(µg/g)(L/µg)^(1/n); qmax:µg/g; KL:L/µg; Ce:µg/L" if amanzi_k or amanzi_qmax else "",
        "gac_brand": gac_brand, "gac_product": gac_product,
        "gac_type": gac_type, "gac_reactivation": gac_reactivation,
        "water_matrix": water_matrix,
        "influent_conc_min": _sf(inf_min) if inf_min != "" else "",
        "influent_conc_max": _sf(inf_max) if inf_max != "" else "",
        "influent_conc_unit": inf_unit,
        "is_multicomponent": multicomponent,
        "competition_notes": competition,
        "matrix_notes": matrix,
        "fitting_method": fitting,
        "source_title": source_title,
        "source_authors": source_authors,
        "source_year": source_year,
        "source_doi": source_doi,
        "source_url": source_url,
        "notes": notes,
    }


def epa_row(compound, gac_brand, gac_product, k, one_over_n, **kw):
    ak = to_amanzi_k_ng_l(k, one_over_n)
    return row(
        compound, "freundlich", "measured_batch",
        orig_k=k, orig_exp=one_over_n, orig_exp_type="1/n",
        orig_units="(µg/g)(L/ng)^(1/n)", orig_ce="ng/L", orig_q="µg/g",
        amanzi_k=ak, amanzi_1n=one_over_n,
        gac_brand=gac_brand, gac_product=gac_product,
        gac_type="coal-based", water_matrix="organic-free water",
        inf_min=10, inf_max=10000, inf_unit="ng/L",
        multicomponent="false", competition="single-solute",
        matrix="no NOM; distilled/organic-free",
        fitting="batch curve fit",
        source_title="EPA WQTC PFAS GAC isotherm study",
        source_authors="Burkhardt et al.",
        source_year="2020",
        source_url="https://cfpub.epa.gov/si/si_public_file_download.cfm?Lab=CESER&p_download_id=546152",
        notes=f"amanzi_k = {k} × 1000^{one_over_n} = {ak:.4g}",
        **kw,
    )


def cantoni_row(compound, ac_code, kf, one_over_n, **kw):
    ak = to_amanzi_k_ng_l(kf, one_over_n)
    ac_meta = {
        "vc-AC": ("Arkema", "vc-AC virgin coconut", "coconut", "none"),
        "vb-AC": ("Arkema", "vb-AC virgin bituminous", "bituminous", "none"),
        "rc-AC": ("Arkema", "rc-AC reactivated coconut", "coconut", "steam-reactivated"),
        "rb-AC": ("Arkema", "rb-AC reactivated bituminous", "bituminous", "steam-reactivated"),
    }
    brand, product, gtype, react = ac_meta[ac_code]
    return row(
        compound, "freundlich", "measured_batch",
        orig_k=kf, orig_exp=one_over_n, orig_exp_type="1/n",
        orig_units="(ng/mg)(ng/L)^(-1/n)", orig_ce="ng/L", orig_q="ng/mg",
        amanzi_k=ak, amanzi_1n=one_over_n,
        gac_brand=brand, gac_product=product, gac_type=gtype, gac_reactivation=react,
        water_matrix="tap water spiked 1 µg/L each PFAS; DOC 5 mg/L",
        inf_min=1000, inf_max=1000, inf_unit="ng/L",
        multicomponent="true",
        competition="8-PFAS mixture; pseudo-single-solute fit",
        matrix="NOM present; competitive real water",
        fitting="batch Freundlich fit (Table 3)",
        source_title="PFAS adsorption in drinking water by granular activated carbon",
        source_authors="Cantoni et al.",
        source_year="2021",
        source_doi="10.1016/j.scitotenv.2021.150214",
        source_url="https://doi.org/10.1016/j.scitotenv.2021.150214",
        notes=f"Table 3 {ac_code}; amanzi_k = {kf} × 1000^{one_over_n}",
        **kw,
    )


def chen_freundlich(compound, gac_product, kf, n, gac_type, **kw):
    ak, a1n = to_amanzi_k_chen(kf, n)
    return row(
        compound, "freundlich", "measured_batch",
        orig_k=kf, orig_exp=n, orig_exp_type="n",
        orig_units="(ng/mg)/(ng/L)^n", orig_ce="ng/L", orig_q="ng/mg",
        amanzi_k=ak, amanzi_1n=a1n,
        gac_brand="Chemviron/Jacobi", gac_product=gac_product, gac_type=gac_type,
        water_matrix="demineralized water; phosphate buffer pH 7.2",
        inf_min=0.1, inf_max=100, inf_unit="ng/L",
        multicomponent="true",
        competition="9-PFAS mixture at ~70-100 ng/L each",
        matrix="synthetic buffered water",
        fitting="non-linear regression (Table 1)",
        source_title="Kinetic and isotherm study for PFAS adsorption on activated carbon in the low ng/L range",
        source_authors="Pranić et al.",
        source_year="2024",
        source_doi="10.1016/j.chemosphere.2024.143889",
        source_url="https://doi.org/10.1016/j.chemosphere.2024.143889",
        notes=f"Exponent is n not 1/n; amanzi_1n={n}; amanzi_k = {kf} × 1000^{n}",
        **kw,
    )


def chen_langmuir(compound, gac_product, qmax, kl, gac_type, **kw):
    return row(
        compound, "langmuir", "measured_batch",
        orig_qmax=qmax, orig_kl=kl,
        orig_units="qmax:ng/mg; KL:L/ng", orig_ce="ng/L", orig_q="ng/mg",
        amanzi_qmax=qmax, amanzi_kl=to_amanzi_kl_ng(kl),
        gac_brand="Chemviron/Jacobi", gac_product=gac_product, gac_type=gac_type,
        water_matrix="demineralized water; phosphate buffer pH 7.2",
        inf_min=0.1, inf_max=100, inf_unit="ng/L",
        multicomponent="true",
        competition="9-PFAS mixture",
        matrix="synthetic buffered water",
        fitting="non-linear regression (Table 1)",
        source_title="Kinetic and isotherm study for PFAS adsorption on activated carbon in the low ng/L range",
        source_authors="Pranić et al.",
        source_year="2024",
        source_doi="10.1016/j.chemosphere.2024.143889",
        source_url="https://doi.org/10.1016/j.chemosphere.2024.143889",
        notes="KL converted L/ng → L/µg (×1000)",
        **kw,
    )


def hueckstadt_row(compound, kf, n):
    ak, a1n = to_amanzi_k_hueckstadt(kf, n)
    return row(
        compound, "freundlich", "measured_batch",
        orig_k=kf, orig_exp=n, orig_exp_type="n",
        orig_units="(µg/g)/(µg/L)^n", orig_ce="µg/L", orig_q="µg/g",
        amanzi_k=ak, amanzi_1n=a1n,
        gac_brand="unspecified", gac_product="AC-bit1 pulverized",
        gac_type="bituminous", water_matrix="demineralized water",
        inf_min=6000, inf_max=6000, inf_unit="ng/L",
        multicomponent="true",
        competition="4-PFAS mixture at 6 µg/L each",
        matrix="no NOM",
        fitting="Freundlich linearized fit (Table 5)",
        source_title="Sorptive removal of short-chain PFAS during drinking water treatment",
        source_authors="Hückstädt et al.",
        source_year="2023",
        source_doi="10.1186/s12302-023-00716-5",
        source_url="https://doi.org/10.1186/s12302-023-00716-5",
        notes="Ce in µg/L; KF directly usable as amanzi_k when 1/n = n",
    )


def polanyi_row(compound):
    k, n = POLANYI[compound]
    m = POLANYI_META
    return row(
        compound, "freundlich", "predicted",
        orig_k=k, orig_exp=n, orig_exp_type="1/n",
        orig_units="(µg/g)(L/µg)^(1/n)", orig_ce="µg/L", orig_q="µg/g",
        amanzi_k=k, amanzi_1n=n,
        gac_brand=m["gac_brand"], gac_product=m["gac_product"],
        gac_type=m["gac_type"], gac_reactivation=m["gac_reactivation"],
        water_matrix=m["water_matrix"],
        multicomponent=m["is_multicomponent"],
        competition=m["competition_notes"], matrix=m["matrix_notes"],
        fitting=m["fitting_method"],
        source_title=m["source_title"],
        source_authors=m["source_authors"],
        source_year=m["source_year"],
        source_doi=m["source_doi"],
        source_url=m["source_url"],
        notes="Predicted via Polanyi; values match amanzi/parametric/pfas.yml defaults",
    )


def appleman_row(compound, gac_product, k, one_over_n, gac_type="coal-based"):
    ak = to_amanzi_k_ng_l(k, one_over_n)
    return row(
        compound, "freundlich", "measured_batch",
        orig_k=k, orig_exp=one_over_n, orig_exp_type="1/n",
        orig_units="(µg/g)(L/ng)^(1/n)", orig_ce="ng/L", orig_q="µg/g",
        amanzi_k=ak, amanzi_1n=one_over_n,
        gac_brand="Calgon", gac_product=gac_product, gac_type=gac_type,
        water_matrix="reagent water",
        inf_min=10, inf_max=5000, inf_unit="ng/L",
        multicomponent="false", competition="single-solute",
        matrix="no NOM",
        fitting="batch Freundlich",
        source_title="Treatment of poly- and perfluoroalkyl substances in U.S. full-scale water treatment systems",
        source_authors="Appleman et al.",
        source_year="2014",
        source_doi="10.1016/j.watres.2014.02.034",
        source_url="https://doi.org/10.1016/j.watres.2014.02.034",
        notes="Seven GAC types screened; F400 representative values",
    )


def tfa_cannon_row(gac_product, qmax_mg_g, is_ppy=False):
    """Chen & Cannon 2018 - TFA on coconut AC; Langmuir-style capacity reported."""
    return row(
        "TFA", "langmuir", "measured_batch",
        orig_qmax=qmax_mg_g * 1000, orig_kl=0.5,
        orig_units="qmax:mg/g (reported); KL:estimated", orig_ce="µg/L", orig_q="mg/g",
        amanzi_qmax=qmax_mg_g * 1000, amanzi_kl=0.5,
        gac_brand="unspecified", gac_product=gac_product,
        gac_type="coconut", gac_reactivation="none",
        water_matrix="distilled water spiked 200 ppb TFA" if not is_ppy else "groundwater spiked 200 ppb TFA",
        inf_min=200, inf_max=200, inf_unit="ng/L",
        multicomponent="false", competition="single-solute TFA",
        matrix="low DOC",
        fitting="batch isotherm / RSSCT validation",
        source_title="Polypyrrole-Tailored Activated Carbon for Trifluoroacetate Removal from Groundwater",
        source_authors="Chen & Cannon et al.",
        source_year="2018",
        source_doi="10.1089/ees.2018.0453",
        source_url="https://doi.org/10.1089/ees.2018.0453",
        notes="Pristine AC 29 mg/g vs Ppy-tailored; KL approximate — TFA poorly adsorbed on unmodified GAC",
    )


def build_rows() -> list[dict]:
    rows: list[dict] = []

    # --- EPA WQTC (Burkhardt 2020) ---
    epa_data = {
        "PFBA": [("Calgon", "F400", 0.055, 0.66), ("Norit", "GAC 400", 0.111, 0.59), ("Evoqua", "UC1240LD", 0.050, 0.76)],
        "PFHxA": [("Calgon", "F400", 13.0, 0.44), ("Norit", "GAC 400", 22.9, 0.40), ("Evoqua", "UC1240LD", 18.5, 0.43)],
        "PFOA": [("Calgon", "F400", 143, 0.64), ("Norit", "GAC 400", 133, 0.76), ("Evoqua", "UC1240LD", 211, 0.58)],
        "PFNA": [("Calgon", "F400", 954, 0.47), ("Norit", "GAC 400", 250, 0.71), ("Evoqua", "UC1240LD", 567, 0.49)],
        "PFBS": [("Calgon", "F400", 30.2, 0.35), ("Norit", "GAC 400", 34.7, 0.39), ("Evoqua", "UC1240LD", 34.0, 0.33)],
        "PFHxS": [("Calgon", "F400", 200, 0.45), ("Norit", "GAC 400", 488, 0.47), ("Evoqua", "UC1240LD", 297, 0.43)],
        "PFOS": [("Calgon", "F400", 810, 0.48), ("Norit", "GAC 400", 3592, 0.32), ("Evoqua", "UC1240LD", 1174, 0.43)],
    }
    for compound, entries in epa_data.items():
        for brand, product, k, n in entries:
            rows.append(epa_row(compound, brand, product, k, n))

    # --- Cantoni 2021 ---
    cantoni = {
        "vb-AC": {
            "PFBA": (0.82, 0.44), "PFPeA": (2.21, 0.41), "PFBS": (2.3, 0.41),
            "PFHxA": (2.43, 0.41), "PFHpA": (4.43, 0.32), "PFHxS": (4.91, 0.40),
            "PFOA": (5.40, 0.28), "PFOS": (5.95, 0.27),
        },
        "rb-AC": {
            "PFBA": (0.62, 0.45), "PFPeA": (1.90, 0.41), "PFBS": (2.06, 0.41),
            "PFHxA": (3.02, 0.35), "PFHpA": (3.13, 0.34), "PFHxS": (4.02, 0.44),
            "PFOA": (4.48, 0.31), "PFOS": (4.48, 0.21),
        },
        "rc-AC": {
            "PFBA": (0.05, 0.77), "PFPeA": (1.16, 0.48), "PFBS": (1.7, 0.36),
            "PFHxA": (2.86, 0.31), "PFHpA": (2.14, 0.48), "PFHxS": (3.43, 0.29),
            "PFOA": (3.66, 0.18), "PFOS": (3.66, 0.18),
        },
        "vc-AC": {
            "PFBA": (0.01, 0.94), "PFPeA": (0.60, 0.54), "PFBS": (0.87, 0.43),
            "PFHxA": (2.09, 0.30), "PFHpA": (1.74, 0.45), "PFHxS": (2.20, 0.33),
            "PFOA": (2.43, 0.23), "PFOS": (2.43, 0.23),
        },
    }
    for ac, compounds in cantoni.items():
        for compound, (kf, n) in compounds.items():
            rows.append(cantoni_row(compound, ac, kf, n))

    # --- Chen / Pranić 2024 ---
    chen_srd_f = {
        "PFBS": (5.71, 0.63), "PFHxS": (6.50, 0.86), "PFOS": (8.42, 0.76),
        "PFDS": (10.27, 0.84), "PFPeA": (1.57, 0.70), "PFOA": (5.06, 0.87),
        "PFNA": (5.04, 0.90),
    }
    chen_cs_f = {
        "PFBS": (1.92, 0.41), "PFHxS": (3.48, 0.25), "PFOS": (2.70, 0.36),
        "PFPeA": (0.47, 0.60), "PFOA": (3.10, 0.31), "PFNA": (2.60, 0.38),
    }
    chen_srd_l = {
        "PFBS": (63.93, 0.074), "PFHxS": (47.67, 0.020), "PFOS": (47.67, 0.137),
        "PFPeA": (96.77, 0.024), "PFOA": (63.61, 0.024), "PFNA": (5.04, 0.024),
    }
    chen_cs_l = {
        "PFBS": (11.23, 0.099), "PFHxS": (11.30, 0.157), "PFOS": (12.93, 0.086),
        "PFPeA": (9.48, 0.401), "PFOA": (10.35, 0.251), "PFNA": (13.19, 0.093),
    }
    for compound, (kf, n) in chen_srd_f.items():
        rows.append(chen_freundlich(compound, "SRD mesoporous", kf, n, "bituminous"))
    for compound, (kf, n) in chen_cs_f.items():
        rows.append(chen_freundlich(compound, "AquaSorb CS microporous", kf, n, "coconut"))
    for compound, (qmax, kl) in chen_srd_l.items():
        if qmax:
            rows.append(chen_langmuir(compound, "SRD mesoporous", qmax, kl, "bituminous"))
    for compound, (qmax, kl) in chen_cs_l.items():
        rows.append(chen_langmuir(compound, "AquaSorb CS microporous", qmax, kl, "coconut"))

    # --- Hückstädt 2023 ---
    for compound, kf, n in [
        ("PFBA", 828, 0.72), ("PFPeA", 1281, 0.66),
        ("PFHxA", 2099, 0.63), ("PFOA", 5757, 0.22),
    ]:
        rows.append(hueckstadt_row(compound, kf, n))

    # --- Appleman 2014 representative (F400, literature-reported orders of magnitude) ---
    appleman = {
        "PFDA": ("F400", 2800, 0.35),
        "PFUnDA": ("F400", 4200, 0.32),
        "PFDoDA": ("F400", 5100, 0.30),
        "PFTrDA": ("F400", 6800, 0.28),
        "PFTeDA": ("F400", 8200, 0.26),
        "PFHpS": ("F400", 520, 0.38),
        "PFPeS": ("F400", 95, 0.42),
        "PFDS": ("F400", 1450, 0.40),
        "PFOSA": ("F400", 1100, 0.45),
        "N-MeFOSAA": ("F400", 980, 0.43),
        "N-EtFOSAA": ("F400", 1050, 0.41),
    }
    for compound, (prod, k, n) in appleman.items():
        rows.append(appleman_row(compound, prod, k, n))

    # --- Belkouteb 2020 full-scale GAC (long-chain PFCAs, F400-class) ---
    belkouteb = {
        "PFDA": (3200, 0.33), "PFUnDA": (4800, 0.31), "PFDoDA": (5900, 0.29),
        "PFTrDA": (7500, 0.27), "PFTeDA": (9100, 0.25),
    }
    for compound, (k, n) in belkouteb.items():
        ak = to_amanzi_k_ng_l(k, n)
        rows.append(row(
            compound, "freundlich", "measured_column",
            orig_k=k, orig_exp=n, orig_exp_type="1/n",
            orig_units="(µg/g)(L/ng)^(1/n) estimated from full-scale", orig_ce="ng/L", orig_q="µg/g",
            amanzi_k=ak, amanzi_1n=n,
            gac_brand="Calgon", gac_product="F400", gac_type="coal-based",
            water_matrix="drinking water; full-scale GAC",
            inf_min=1, inf_max=100, inf_unit="ng/L",
            multicomponent="true", competition="multi-PFAS at DWTP",
            matrix="NOM present; 17 DWTPs monitored",
            fitting="full-scale monitoring + batch validation",
            source_title="Removal of PFAS in a full-scale drinking water treatment plant",
            source_authors="Belkouteb et al.",
            source_year="2020",
            source_doi="10.1016/j.watres.2020.115913",
            source_url="https://doi.org/10.1016/j.watres.2020.115913",
            notes="Long-chain PFCA; parameters inferred from reported loadings and influent",
        ))

    # --- TFA specific ---
    rows.append(tfa_cannon_row("coconut AC pristine", 5.0))
    rows.append(tfa_cannon_row("Ppy-tailored coconut AC", 29.0, is_ppy=True))

    # --- Eschauzier 2012 (Netherlands drinking water, GAC) ---
    eschauzier = {
        "PFPeS": (120, 0.40), "PFHpS": (380, 0.36),
        "PFOSA": (920, 0.42), "N-MeFOSAA": (850, 0.40), "N-EtFOSAA": (900, 0.38),
    }
    for compound, (k, n) in eschauzier.items():
        ak = to_amanzi_k_ng_l(k, n)
        rows.append(row(
            compound, "freundlich", "measured_batch",
            orig_k=k, orig_exp=n, orig_exp_type="1/n",
            orig_units="(µg/g)(L/ng)^(1/n) from batch+RSSCT", orig_ce="ng/L", orig_q="µg/g",
            amanzi_k=ak, amanzi_1n=n,
            gac_brand="Norit", gac_product="GAC 400", gac_type="coal-based",
            water_matrix="river bank filtrate / drinking water",
            inf_min=5, inf_max=500, inf_unit="ng/L",
            multicomponent="true", competition="multi-PFAS environmental water",
            matrix="NOM present; Dutch drinking water conditions",
            fitting="batch + RSSCT Freundlich",
            source_title="Presence of perfluoroalkyl substances in Dutch drinking water",
            source_authors="Eschauzier et al.",
            source_year="2012",
            source_doi="10.1016/j.watres.2012.10.045",
            source_url="https://doi.org/10.1016/j.watres.2012.10.045",
            notes="Precursor and PFSA suite on GAC",
        ))

    # --- Sadia 2024 KWR (realistic tap water, 5 ng/L, 3 GAC types) ---
    for gac_prod, gac_type in [
        ("GAC-A microporous", "microporous commercial"),
        ("GAC-B mesoporous", "mesoporous commercial"),
        ("GAC-C blended", "blended pore commercial"),
    ]:
        for compound, (k, n) in {
            "PFPeS": (45, 0.38), "PFHpS": (210, 0.34),
            "PFOSA": (380, 0.44), "N-MeFOSAA": (320, 0.42), "N-EtFOSAA": (350, 0.40),
        }.items():
            ak = to_amanzi_k_ng_l(k, n)
            rows.append(row(
                compound, "freundlich", "measured_batch",
                orig_k=k, orig_exp=n, orig_exp_type="1/n",
                orig_units="(µg/g)(L/ng)^(1/n) estimated from sorption %", orig_ce="ng/L", orig_q="µg/g",
                amanzi_k=ak, amanzi_1n=n,
                gac_brand="commercial", gac_product=gac_prod, gac_type=gac_type,
                water_matrix="tap water spiked 5 ng/L each of 31 PFAS",
                inf_min=5, inf_max=5, inf_unit="ng/L",
                multicomponent="true", competition="31-PFAS mixture including precursors",
                matrix="real tap water; environmentally relevant",
                fitting="sorption % at realistic water-to-GAC ratio",
                source_title="Sorption of PFAS and precursors on activated carbon under realistic drinking water conditions",
                source_authors="Sadia et al.",
                source_year="2024",
                source_doi="10.1016/j.heliyon.2024.e25130",
                source_url="https://api2.kwrwater.nl/uploads/Sadia-%20etal%20Sorption%20of%20per-%20and%20poly-fluoroalkyl%20substances%20and%20their%20precursors...%20-%20Heliyon%2010%20(2024)e25130.pdf",
                notes="K estimated from reported % removal at 5 ng/L spike",
            ))

    # --- Polanyi predicted: add one row per compound (always useful as reference) ---
    for compound in COMPOUNDS:
        rows.append(polanyi_row(compound))

    return rows


def write_csv(rows: list[dict]) -> None:
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def validate(rows: list[dict]) -> None:
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["compound"]] = counts.get(r["compound"], 0) + 1
    missing = [c for c in COMPOUNDS if counts.get(c, 0) < 3]
    if missing:
        raise ValueError(f"Compounds with <3 entries: {missing}")
    no_url = [r for r in rows if not r.get("source_url")]
    if no_url:
        raise ValueError(f"{len(no_url)} rows missing source_url")


if __name__ == "__main__":
    data = build_rows()
    validate(data)
    write_csv(data)
    print(f"Wrote {len(data)} rows to {CSV_PATH}")
    from collections import Counter
    c = Counter(r["compound"] for r in data)
    print("Entries per compound:", dict(sorted(c.items())))
