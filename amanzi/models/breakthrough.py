from __future__ import annotations

from dataclasses import dataclass, field
import importlib
import logging
import math
import sys
import tempfile
from typing import Any
import numpy as np


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


class CadetBreakthroughSolver:
    """CADET-Python entry point kept optional because CADET-Core is native."""

    def __init__(self, allow_fallback: bool = False):
        self.allow_fallback = allow_fallback

    def run(self, inputs: BreakthroughInput) -> BreakthroughResult:
        try:
            Cadet = importlib.import_module("cadet").Cadet
        except ImportError as exc:
            raise RuntimeError("CADET-Python is not installed") from exc

        try:
            logging.debug(f"CADET Solver running")
            return self._run_cadet(Cadet, inputs)
        except Exception as exc:
            if self.allow_fallback:
                logging.exception("CADET breakthrough simulation failed; using fallback solver.")
                return PyodideBreakthroughSolver().run(inputs)
            raise RuntimeError(
                "CADET breakthrough simulation failed. Check that CADET-Core is installed "
                f"and that cadet.Cadet.cadet_path points to the CADET executable. Original error: {exc}"
            ) from exc

    def _run_cadet(self, cadet_cls, inputs: BreakthroughInput) -> BreakthroughResult:
        logging.info(f"Influent PFA: {inputs.influent_pfas}")

        fallback = PyodideBreakthroughSolver()
        metadata = {str(item["name"]): item for item in inputs.metadata_pfas if item.get("name")}
        compounds = [
            compound
            for compound, c0_ng_l in inputs.influent_pfas.items()
            if float(c0_ng_l or 0) > 0
        ]
        if not compounds:
            return BreakthroughResult()
        logging.info(f"Compounds: {compounds}")
        print(f"Compounds: {compounds}")
        x_values = breakthrough_x_values(inputs)
        outlet = self._run_multicomponent(cadet_cls, inputs, compounds, x_values)

        breakthrough = {}
        peq = np.zeros(len(x_values))
        sum4 = np.zeros(len(x_values))
        sum20 = np.zeros(len(x_values))

        for index, compound in enumerate(compounds):
            c0_ng_l = float(inputs.influent_pfas[compound])
            y_values = outlet[:, index]
            breakthrough[compound] = fallback._series(x_values, y_values)

            peq_factor = float(metadata.get(compound, {}).get("PEQ", 1) or 1)
            effluent = float(c0_ng_l) * y_values * peq_factor
            peq += effluent
            if compound in SUM4_PFAS:
                sum4 += effluent
            if compound in SUM20_PFAS:
                sum20 += effluent

        return BreakthroughResult(
            breakthrough=breakthrough,
            peq_pfas=fallback._series(x_values, peq),
            sum4_pfas=fallback._series(x_values, sum4),
            sum20_pfas=fallback._series(x_values, sum20),
        )

    def _run_multicomponent(
        self,
        cadet_cls,
        inputs: BreakthroughInput,
        compounds: list[str],
        x_values: np.ndarray,
    ) -> np.ndarray:
        model = cadet_cls()
        logging.debug("Running CADET breakthrough simulation.")

        ncomp = len(compounds)
        metadata = {str(item["name"]): item for item in inputs.metadata_pfas if item.get("name")}
        influent_pfas_ng_l = [float(inputs.influent_pfas[compound]) for compound in compounds]
        influent_pfas_mol_m3 = [
            self._influent_mol_m3(compound, concentration, inputs, metadata)
            for compound, concentration in zip(compounds, influent_pfas_ng_l)
        ]
        residence_time_h = inputs.bed_volume_m3 / max(inputs.flow_m3_h, 1e-12)
        solution_times = x_values * residence_time_h * 3600
        t_end = max(float(solution_times[-1]), 1)
        flow_m3_s = max(inputs.flow_m3_h / 3600, 1e-12)
        mass_transfer = max(inputs.mass_transfer_coefficient_s, 1e-9)
        freundlich_k = []
        freundlich_n = []
        initial_loading = []

        for compound in compounds:
            params = freundlich_parameters(compound, inputs.compound_parameters.get(compound, {}))
            freundlich_k.append(float(params.get("freundlich_k", 100) or 100))
            one_over_n = float(params.get("freundlich_1n", 0.4) or 0.4)
            freundlich_n.append(1 / max(one_over_n, 1e-12))
            initial_loading.append(float(params.get("initial_loading_q", 0) or 0))

        model.root.input.model.nunits = 3
        model.root.input.model.unit_000.unit_type = "INLET"
        model.root.input.model.unit_000.ncomp = ncomp
        model.root.input.model.unit_000.inlet_type = "PIECEWISE_CUBIC_POLY"
        model.root.input.model.unit_000.sec_000.const_coeff = influent_pfas_mol_m3


        column = model.root.input.model.unit_001
        column.unit_type = "GENERAL_RATE_MODEL"
        column.ncomp = ncomp
        column.nbound = [1] * ncomp
        column.col_length = max(inputs.column_length, 1e-9)
        column.cross_section_area = max(inputs.bed_volume_m3 / max(inputs.column_length, 1e-9), 1e-9)
        column.col_porosity = inputs.bed_porosity
        column.par_porosity = inputs.particle_porosity
        column.par_radius = max(inputs.particle_diameter_mm / 2000, 1e-9)
        column.col_dispersion = ncomp*[0]#inputs.axial_dispersion_m2_s
        column.film_diffusion = [mass_transfer] * ncomp
        column.par_diffusion = [mass_transfer] * ncomp
        column.adsorption_model = "FREUNDLICH_LDF"
        column.adsorption.is_kinetic = 1
        column.adsorption.fldf_kkin = [mass_transfer] * ncomp
        column.adsorption.fldf_kf = freundlich_k
        column.adsorption.fldf_n = freundlich_n
        column.init_cp = [0.0] * ncomp
        column.init_cs = [0.0] * ncomp
        column.discretization.spatial_method = "DG"
        column.discretization.polydeg = 3
        column.discretization.nelem = 1
        column.discretization.npar = 5

        particle = column.particle_type_000
        particle.film_diffusion = [mass_transfer] * ncomp
        particle.adsorption_model = "FREUNDLICH_LDF"
        particle.nbound = [1] * ncomp
        particle.adsorption.is_kinetic = 1
        particle.adsorption.fldf_kkin = [mass_transfer] * ncomp
        particle.adsorption.fldf_kf = freundlich_k
        particle.adsorption.fldf_n = freundlich_n
        particle.init_cp = [0.0] * ncomp
        particle.init_cs = [0.0] * ncomp
        particle.discretization.spatial_method = "DG"
        particle.discretization.par_polydeg = 3
        particle.discretization.par_nelem = 1

        if column.unit_type == "GENERAL_RATE_MODEL":
            self._set_general_rate_discretization(column, [1] * ncomp)

        model.root.input.model.unit_002.unit_type = "OUTLET"
        model.root.input.model.unit_002.ncomp = ncomp
        model.root.input.solver.sections.nsec = 1
        model.root.input.solver.sections.section_times = [0.0, t_end]
        model.root.input.solver.sections.section_continuity = []
        model.root.input.model.connections.nswitches = 1
        model.root.input.model.connections.switch_000.section = 0
        model.root.input.model.connections.switch_000.connections = [
            0, 1, -1, -1, flow_m3_s,
            1, 2, -1, -1, flow_m3_s,
        ]
        model.root.input.model.solver.gs_type = 1
        model.root.input.model.solver.max_krylov = 0
        model.root.input.model.solver.max_restarts = 10
        model.root.input.model.solver.schur_safety = 1.0e-8

        model.root.input.solver.nthreads = 1
        model.root.input.solver.time_integrator.abstol = 1e-6
        model.root.input.solver.time_integrator.algtol = 1e-10
        model.root.input.solver.time_integrator.reltol = 1e-6
        model.root.input.solver.time_integrator.init_step_size = 1e-6
        model.root.input.solver.time_integrator.max_steps = 1000000
        model.root.input["return"].unit_001.write_solution_outlet = 1
        model.root.input.solver.user_solution_times = solution_times

        with tempfile.NamedTemporaryFile(suffix=".h5") as file:
            model.filename = file.name
            model.save()
            data = model.run()
            if data.return_code != 0:
                raise RuntimeError(data)
            model.load()

        outlet = np.array(model.root.output.solution.unit_001.solution_outlet)
        outlet = outlet.reshape(len(solution_times), ncomp)
        if outlet.shape[0] != len(x_values):
            interpolated = [
                np.interp(solution_times, model.root.output.solution.solution_times, outlet[:, index])
                for index in range(ncomp)
            ]
            outlet = np.column_stack(interpolated)
        c0 = np.array(influent_pfas_mol_m3)
        return np.clip(outlet / np.maximum(c0, 1e-30), 0, 1)

    def _set_general_rate_discretization(self,model, n_bound=None, n_col=100) -> None:
        columns = {'GENERAL_RATE_MODEL'}

        for unit_name, unit in model.root.input.model.items():
            if 'unit_' in unit_name and unit.unit_type in columns:
                unit.discretization.ncol = n_col
                unit.discretization.npar = 5 # discretization resolution of the particle
                
                if n_bound is None:
                    n_bound = unit.ncomp*[0]
                unit.discretization.nbound = n_bound
                
                unit.discretization.par_disc_type = 'EQUIDISTANT_PAR'
                unit.discretization.use_analytic_jacobian = 1
                unit.discretization.reconstruction = 'WENO'
                unit.discretization.gs_type = 1
                unit.discretization.max_krylov = 0
                unit.discretization.max_restarts = 10
                unit.discretization.schur_safety = 1.0e-8

                unit.discretization.weno.boundary_model = 0
                unit.discretization.weno.weno_eps = 1e-10
                unit.discretization.weno.weno_order = 1 

    def _influent_mol_m3(
        self,
        compound: str,
        concentration_ng_l: float,
        inputs: BreakthroughInput,
        metadata: dict[str, dict[str, Any]],
    ) -> float:
        try:
            properties = compound_properties(
                compound,
                inputs.compound_parameters.get(compound, {}),
                metadata.get(compound, {}),
            )
            molecular_weight = molecular_weight_g_mol(properties)
        except ValueError as exc:
            raise ValueError(f"Missing molecular weight for {compound}; cannot convert ng/l to mol/m3") from exc
        return ng_l_to_mol_m3(concentration_ng_l, molecular_weight)


def select_breakthrough_solver(preferred: str | None = None):
    logging.debug(f"Selecting breakthrough solver: {preferred}")
    if sys.platform == "emscripten":
        return PyodideBreakthroughSolver()

    if preferred == "cadet":
        try:
            importlib.import_module("cadet")
        except ImportError:
            logging.debug(f"cadet not installed")
            return PyodideBreakthroughSolver()
        return CadetBreakthroughSolver(allow_fallback=False)

    return PyodideBreakthroughSolver()
