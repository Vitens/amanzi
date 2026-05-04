from __future__ import annotations

from dataclasses import dataclass, field
import logging
import math
import sys
from typing import Any
import numpy as np
import pandas as pd


SUM4_PFAS = {"PFOA", "PFOS", "PFHxS", "PFHpS"}
SUM20_PFAS = {
    "PFBA",
    "PFPeA",
    "PFHxA",
    "PFHpA",
    "PFOA",
    "PFNA",
    "PFDA",
    "PFUnDA",
    "PFDoDA",
    "PFTrDA",
    "PFTeDA",
    "PFBS",
    "PFPeS",
    "PFHxS",
    "PFHpS",
    "PFOS",
    "PFDS",
    "PFOSA",
    "N-MeFOSAA",
    "N-EtFOSAA",
}

logging.basicConfig(level=logging.DEBUG)

DEFAULT_PFAS_FREUNDLICH_PARAMETERS = {
    "PFBS": {"freundlich_k": 456.94, "freundlich_1n": 0.411, "initial_loading_q": 1},
    "PFPeS": {"freundlich_k": 1521, "freundlich_1n": 0.3521, "initial_loading_q": 1},
    "PFHxS": {"freundlich_k": 3840, "freundlich_1n": 0.3134, "initial_loading_q": 1},
    "PFHpS": {"freundlich_k": 4588.9, "freundlich_1n": 0.286, "initial_loading_q": 1},
    "PFOS": {"freundlich_k": 7222, "freundlich_1n": 0.2525, "initial_loading_q": 1},
    "PFDS": {"freundlich_k": 0.1, "freundlich_1n": 1, "initial_loading_q": 1},
    "TFA": {"freundlich_k": 2.3 * (1000 / (1000 ** 0.343)), "freundlich_1n": 0.343, "initial_loading_q": 1},
    "PFBA": {"freundlich_k": 255, "freundlich_1n": 0.4942, "initial_loading_q": 1},
    "PFPeA": {"freundlich_k": 1160, "freundlich_1n": 0.4252, "initial_loading_q": 1},
    "PFHxA": {"freundlich_k": 4179, "freundlich_1n": 0.3607, "initial_loading_q": 1},
    "PFHpA": {"freundlich_k": 498, "freundlich_1n": 0.3144, "initial_loading_q": 1},
    "PFOA": {"freundlich_k": 1718, "freundlich_1n": 0.2808, "initial_loading_q": 1},
    "PFDA": {"freundlich_k": 6371, "freundlich_1n": 0.2415, "initial_loading_q": 1},
    "PFUnDA": {"freundlich_k": 14603, "freundlich_1n": 0.2233, "initial_loading_q": 1},
    "PFDoDA": {"freundlich_k": 18106, "freundlich_1n": 0.2076, "initial_loading_q": 1},
    "PFTrDA": {"freundlich_k": 25862, "freundlich_1n": 0.1972, "initial_loading_q": 1},
    "PFTeDA": {"freundlich_k": 30582, "freundlich_1n": 0.1858, "initial_loading_q": 1},
}


DEFAULT_PFAS_COMPOUND_PROPERTIES = {
    "PFBS": {"MW": 300.1, "MolarVol": 163.9, "BP": 198, "Density": 1.83, "Solubility": 0, "VaporPress": 0},
    "PFPeS": {"MW": 350, "MolarVol": 190.2, "BP": 225, "Density": 1.84, "Solubility": 0, "VaporPress": 0},
    "PFHpS": {"MW": 450, "MolarVol": 238, "BP": 226, "Density": 1.89, "Solubility": 0, "VaporPress": 0},
    "PFOS": {"MW": 500, "MolarVol": 237, "BP": 189, "Density": 1.8, "Solubility": 0, "VaporPress": 0},
    "PFHxS": {"MW": 400, "MolarVol": 217, "BP": 239, "Density": 1.84, "Solubility": 0, "VaporPress": 0},
    "PFDS": {"MW": 600, "MolarVol": 310.9, "BP": 255, "Density": 1.93, "Solubility": 0, "VaporPress": 0},
    "TFA": {"MW": 114, "MolarVol": 129.7, "BP": 72, "Density": 1.489, "Solubility": 0, "VaporPress": 0},
    "PFBA": {"MW": 214, "MolarVol": 129.72, "BP": 121, "Density": 1.65, "Solubility": 0, "VaporPress": 0},
    "PFPeA": {"MW": 264, "MolarVol": 154, "BP": 139, "Density": 1.71, "Solubility": 0, "VaporPress": 0},
    "PFHxA": {"MW": 314, "MolarVol": 182, "BP": 157, "Density": 1.69, "Solubility": 0, "VaporPress": 0},
    "PFHpA": {"MW": 364, "MolarVol": 212.9, "BP": 175, "Density": 1.71, "Solubility": 0, "VaporPress": 0},
    "PFOA": {"MW": 500, "MolarVol": 217, "BP": 145, "Density": 1.84, "Solubility": 0, "VaporPress": 0},
    "PFDA": {"MW": 514, "MolarVol": 292, "BP": 184, "Density": 1.79, "Solubility": 0, "VaporPress": 0},
    "PFUnDA": {"MW": 564.1, "MolarVol": 304.8, "BP": 238.4, "Density": 1.85, "Solubility": 0, "VaporPress": 0},
    "PFDoDA": {"MW": 614.1, "MolarVol": 328.3, "BP": 249, "Density": 1.87, "Solubility": 0, "VaporPress": 0},
    "PFTrDA": {"MW": 664.1, "MolarVol": 345.8, "BP": 261, "Density": 1.92, "Solubility": 0, "VaporPress": 0},
    "PFTeDA": {"MW": 714.1, "MolarVol": 368, "BP": 270, "Density": 1.94, "Solubility": 0, "VaporPress": 0},
}


def freundlich_parameters(compound: str, configured: dict[str, Any] | None = None) -> dict[str, Any]:
    defaults = DEFAULT_PFAS_FREUNDLICH_PARAMETERS.get(compound, {})
    return defaults | (configured or {})


def compound_properties(
    compound: str,
    configured: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    defaults = DEFAULT_PFAS_COMPOUND_PROPERTIES.get(compound, {})
    return defaults | (configured or {}) | (metadata or {})


def molecular_weight_g_mol(properties: dict[str, Any]) -> float:
    value = properties.get("MW", properties.get("molecular_weight", properties.get("molecularWeight")))
    try:
        molecular_weight = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Missing molecular weight for compound") from exc
    if molecular_weight <= 0:
        raise ValueError("Molecular weight must be positive")
    return molecular_weight


def ng_l_to_mol_m3(concentration_ng_l: float, molecular_weight: float) -> float:
    return float(concentration_ng_l) * 1e-6 / molecular_weight


@dataclass
class BreakthroughInput:
    influent_pfas: dict[str, float]
    metadata_pfas: list[dict[str, Any]]
    compound_parameters: dict[str, dict[str, Any]]
    bed_volume_m3: float
    flow_m3_h: float
    apparent_density_kg_m3: float
    particle_density_kg_m3: float
    bed_porosity: float
    particle_diameter_mm: float
    replacement_interval_days: float
    replacement_loading: float
    max_bed_volumes: float | None = None
    points: int = 200
    axial_dispersion_m2_s: float = 1e-8
    mass_transfer_coefficient_s: float = 0.002
    particle_porosity: float = 0.6
    column_length: float = 1.0


@dataclass
class BreakthroughResult:
    breakthrough: dict[str, list[dict[str, float]]] = field(default_factory=dict)
    peq_pfas: list[dict[str, float]] = field(default_factory=list)
    sum4_pfas: list[dict[str, float]] = field(default_factory=list)
    sum20_pfas: list[dict[str, float]] = field(default_factory=list)


def breakthrough_x_values(inputs: BreakthroughInput) -> np.ndarray:
    points = max(2, int(inputs.points or 200))
    if inputs.max_bed_volumes:
        max_bed_volumes = max(float(inputs.max_bed_volumes), 1)
    else:
        bed_volumes_per_day = inputs.flow_m3_h * 24 / max(inputs.bed_volume_m3, 1e-9)
        interval_bed_volumes = bed_volumes_per_day * max(float(inputs.replacement_interval_days or 1), 1)
        max_bed_volumes = max(interval_bed_volumes * 1.25, 1)
    return np.linspace(0, max_bed_volumes, points)


class PyodideBreakthroughSolver:
    """Small deterministic breakthrough approximation that avoids native solvers."""

    def run(self, inputs: BreakthroughInput) -> BreakthroughResult:
        x_values = breakthrough_x_values(inputs)
        points = len(x_values)

        metadata = {str(item["name"]): item for item in inputs.metadata_pfas if item.get("name")}
        breakthrough: dict[str, list[dict[str, float]]] = {}
        peq = np.zeros(points)
        sum4 = np.zeros(points)
        sum20 = np.zeros(points)

        for compound, c0_ng_l in inputs.influent_pfas.items():
            c0_ng_l = max(float(c0_ng_l or 0), 0)
            if c0_ng_l <= 0:
                continue

            params = freundlich_parameters(compound, inputs.compound_parameters.get(compound, {}))
            c_over_c0 = self._compound_curve(x_values, c0_ng_l, params, inputs)
            breakthrough[compound] = [
                {"x": float(x), "y": float(y)}
                for x, y in zip(x_values, c_over_c0)
            ]

            peq_factor = float(metadata.get(compound, {}).get("PEQ", 1) or 1)
            effluent = c0_ng_l * c_over_c0 * peq_factor
            peq += effluent
            if compound in SUM4_PFAS:
                sum4 += effluent
            if compound in SUM20_PFAS:
                sum20 += effluent

        return BreakthroughResult(
            breakthrough=breakthrough,
            peq_pfas=self._series(x_values, peq),
            sum4_pfas=self._series(x_values, sum4),
            sum20_pfas=self._series(x_values, sum20),
        )

    def _compound_curve(
        self,
        x_values: np.ndarray,
        c0_ng_l: float,
        params: dict[str, Any],
        inputs: BreakthroughInput,
    ) -> np.ndarray:
        c0_ug_l = c0_ng_l / 1000
        k = self._positive(params.get("freundlich_k"), params.get("adsorptionCapacity_simple", 100))
        one_over_n = self._positive(params.get("freundlich_1n"), 0.4)
        initial_q = max(float(params.get("initial_loading_q", 0) or 0), 0)

        q_equilibrium_ug_g = max(k * (max(c0_ug_l, 1e-12) ** one_over_n), 1e-9)
        available_q_ug_g = max(q_equilibrium_ug_g - initial_q, q_equilibrium_ug_g * 0.05)

        carbon_mass_g = max(inputs.bed_volume_m3 * inputs.apparent_density_kg_m3 * 1000, 1e-9)
        bed_volume_l = max(inputs.bed_volume_m3 * 1000, 1e-9)
        capacity_bed_volumes = available_q_ug_g * carbon_mass_g / max(c0_ug_l * bed_volume_l, 1e-12)
        capacity_bed_volumes *= max(float(inputs.replacement_loading or 1), 0.01)

        half_saturation = min(max(capacity_bed_volumes, 1), x_values[-1] * 1.5)
        hydraulics_width = max(half_saturation * 0.08, x_values[-1] / 80, 1)
        dispersion_width = math.sqrt(max(float(inputs.axial_dispersion_m2_s or 0), 0)) * 1000
        transfer_width = 1 / max(float(inputs.mass_transfer_coefficient_s or 0.002), 1e-6) / 100
        width = max(hydraulics_width + dispersion_width + transfer_width, 1)

        leakage = self._leakage(params)
        exponent = np.clip(-(x_values - half_saturation) / width, -80, 80)
        sigmoid = 1 / (1 + np.exp(exponent))
        return np.clip(leakage + (1 - leakage) * sigmoid, 0, 1)

    def _leakage(self, params: dict[str, Any]) -> float:
        removal = params.get("removalAKF_simple", params.get("removal_AKF_simple"))
        if removal is None:
            return 0
        return float(np.clip(1 - float(removal) / 100, 0, 1))

    def _positive(self, value: Any, default: float) -> float:
        try:
            value = float(value)
        except (TypeError, ValueError):
            value = default
        return max(value, 1e-12)

    def _series(self, x_values: np.ndarray, y_values: np.ndarray) -> list[dict[str, float]]:
        return [
            {"x": float(x), "y": float(y)}
            for x, y in zip(x_values, y_values)
        ]


class PsdmBreakthroughSolver:
    """PSDM-backed breakthrough simulation for advanced activated carbon modeling."""

    def __init__(self, allow_fallback: bool = True):
        self.allow_fallback = allow_fallback

    def run(self, inputs: BreakthroughInput) -> BreakthroughResult:
        compounds = [
            compound
            for compound, concentration in inputs.influent_pfas.items()
            if float(concentration or 0) > 0
        ]
        if not compounds:
            return BreakthroughResult()

        try:
            return self._run_psdm(inputs, compounds)
        except Exception as exc:
            if self.allow_fallback:
                logging.exception("PSDM breakthrough simulation failed; using fallback solver.")
                return PyodideBreakthroughSolver().run(inputs)
            raise RuntimeError(f"PSDM breakthrough simulation failed. Original error: {exc}") from exc

    def _run_psdm(self, inputs: BreakthroughInput, compounds: list[str]) -> BreakthroughResult:
        from .psdm.PSDM import PSDM

        metadata = {str(item["name"]): item for item in inputs.metadata_pfas if item.get("name")}
        x_values = breakthrough_x_values(inputs)
        time_days = self._bed_volumes_to_days(x_values, inputs)

        column_data = self._column_data(inputs)
        compound_data = self._compound_data(compounds, inputs, metadata)
        rawdata = self._raw_data(compounds, time_days, inputs)
        k_data = self._k_data(compounds, inputs, time_days)
        print("K_data: ", k_data)
        print("Compound data: ", compound_data)
        print("Raw data: ", rawdata)
        print("Column data: ", column_data)

        column = PSDM(
            column_data,
            compound_data,
            rawdata,
            nr=8,
            nz=13,
            ne=2,
            chem_type="PFAS",
            water_type="Organic Free",
            k_data=k_data,
            optimize=False,
            solver="BDF",
        )
        model_results = column.run_psdm()
        print("Model results: ", model_results)

        breakthrough: dict[str, list[dict[str, float]]] = {}
        peq = np.zeros(len(x_values))
        sum4 = np.zeros(len(x_values))
        sum20 = np.zeros(len(x_values))

        for compound in compounds:
            c0_ng_l = float(inputs.influent_pfas.get(compound, 0) or 0)
            if c0_ng_l <= 0:
                continue

            effluent_ng_l = np.asarray(model_results[compound](time_days), dtype=float)
            ratio = np.clip(effluent_ng_l / max(c0_ng_l, 1e-12), 0, 1)
            breakthrough[compound] = self._series(x_values, ratio)

            peq_factor = float(metadata.get(compound, {}).get("PEQ", 1) or 1)
            weighted_effluent = effluent_ng_l * peq_factor
            peq += weighted_effluent
            if compound in SUM4_PFAS:
                sum4 += weighted_effluent
            if compound in SUM20_PFAS:
                sum20 += weighted_effluent

        return BreakthroughResult(
            breakthrough=breakthrough,
            peq_pfas=self._series(x_values, peq),
            sum4_pfas=self._series(x_values, sum4),
            sum20_pfas=self._series(x_values, sum20),
        )

    def _bed_volumes_to_days(self, bed_volumes: np.ndarray, inputs: BreakthroughInput) -> np.ndarray:
        bed_volumes_per_day = inputs.flow_m3_h * 24 / max(inputs.bed_volume_m3, 1e-9)
        return bed_volumes / max(bed_volumes_per_day, 1e-9)

    def _column_data(self, inputs: BreakthroughInput) -> pd.Series:
        bed_porosity = float(np.clip(inputs.bed_porosity, 0.05, 0.95))
        particle_porosity = float(np.clip(inputs.particle_porosity, 0.05, 0.95))
        length_cm = max(float(inputs.column_length), 1e-9) * 100
        bed_volume_cm3 = max(float(inputs.bed_volume_m3), 1e-12) * 1e6
        diameter_cm = math.sqrt(4 * (bed_volume_cm3 / length_cm) / math.pi)
        mass_g = max(float(inputs.bed_volume_m3) * float(inputs.apparent_density_kg_m3) * 1000, 1e-9)
        apparent_density_g_cm3 = float(inputs.apparent_density_kg_m3) / 1000
        particle_density_g_cm3 = float(inputs.particle_density_kg_m3) / 1000
        rhop = particle_density_g_cm3
        rhof = apparent_density_g_cm3
        flow_ml_min = max(float(inputs.flow_m3_h), 1e-12) * 1e6 / 60

        return pd.Series(
            data=[
                max(float(inputs.particle_diameter_mm), 1e-9) / 20,  #radius in cm 
                flow_ml_min,  #flow rate in ml/min
                particle_porosity,  #particle porosity
                5.0,  #pore to surface diffusion ratio
                rhop,  #particle density in g/cm3
                rhof,  #apparent density in g/cm3
                length_cm,  #Column length in cm
                mass_g,  #Fixed bed mass in g
                diameter_cm,  #Column diameter in cm
                1.0,  #tortuosity
                "influent",  #influent identifier
                "effluent",  #effluent identifier
                "ng",  #units
                "days",  #time units
            ],
            index=[
                "rad",
                "flrt",
                "epor",
                "psdfr",
                "rhop",
                "rhof",
                "L",
                "wt",
                "diam",
                "tortu",
                "influentID",
                "effluentID",
                "units",
                "time",
            ],
            name="F400",
        )

    def _compound_data(
        self,
        compounds: list[str],
        inputs: BreakthroughInput,
        metadata: dict[str, dict[str, Any]],
    ) -> pd.DataFrame:
        rows = ["MW", "MolarVol", "BP", "Density", "Solubility", "VaporPress"]
        data: dict[str, list[float]] = {}
        for compound in compounds:
            props = compound_properties(
                compound,
                inputs.compound_parameters.get(compound, {}),
                metadata.get(compound, {}),
            )
            data[compound] = [
                float(props.get("MW", 500)),
                float(props.get("MolarVol", 200)),
                float(props.get("BP", 200)),
                float(props.get("Density", 1.8)),
                float(props.get("Solubility", 0)),
                float(props.get("VaporPress", 0)),
            ]
        return pd.DataFrame(data, index=pd.Index(rows))

    def _raw_data(
        self,
        compounds: list[str],
        time_days: np.ndarray,
        inputs: BreakthroughInput,
    ) -> pd.DataFrame:
        columns = [
            (phase, compound)
            for phase in ("influent", "F400")
            for compound in compounds
        ]
        raw = pd.DataFrame(
            0.0,
            index=np.asarray(time_days, dtype=float),
            columns=pd.MultiIndex.from_tuples(columns, names=["type", "compound"]),
        )
        for compound in compounds:
            c0_ng_l = max(float(inputs.influent_pfas.get(compound, 0) or 0), 1e-9)
            raw[("influent", compound)] = c0_ng_l
            raw[("F400", compound)] = 0.0
        return raw

    def _k_data(
        self,
        compounds: list[str],
        inputs: BreakthroughInput,
        time_days: np.ndarray,
    ) -> pd.DataFrame:
        k_data = pd.DataFrame(
            index=pd.Index(["K", "1/n", "q", "brk", "AveC"]),
            columns=pd.Index(compounds),
            dtype=float,
        )
        for compound in compounds:
            params = freundlich_parameters(compound, inputs.compound_parameters.get(compound, {}))
            k_data.loc["K", compound] = self._positive(params.get("freundlich_k"), 100)
            k_data.loc["1/n", compound] = self._positive(params.get("freundlich_1n"), 0.4)
            k_data.loc["q", compound] = max(float(params.get("initial_loading_q", 1) or 1), 1e-9)
            k_data.loc["brk", compound] = max(float(time_days[-1]), 1)
            k_data.loc["AveC", compound] = max(float(inputs.influent_pfas.get(compound, 0) or 0), 1e-9)
        return k_data

    def _positive(self, value: Any, default: float) -> float:
        try:
            value = float(value)
        except (TypeError, ValueError):
            value = default
        return max(value, 1e-9)

    def _series(self, x_values: np.ndarray, y_values: np.ndarray) -> list[dict[str, float]]:
        return [
            {"x": float(x), "y": float(y)}
            for x, y in zip(x_values, y_values)
        ]


def select_breakthrough_solver(preferred: str | None = None):
    logging.debug(f"Selecting breakthrough solver: {preferred}")
    if sys.platform == "emscripten":
        return PyodideBreakthroughSolver()

    selected = (preferred or "psdm").lower()
    if selected == "pyodide":
        return PyodideBreakthroughSolver()

    if selected == "psdm":
        return PsdmBreakthroughSolver(allow_fallback=True)

    logging.warning("Unknown breakthrough solver '%s', defaulting to PSDM", selected)
    return PsdmBreakthroughSolver(allow_fallback=True)
