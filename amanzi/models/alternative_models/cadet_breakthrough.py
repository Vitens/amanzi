from __future__ import annotations

import importlib
import logging
import tempfile

import numpy as np

from .breakthrough import (
    BreakthroughInput,
    BreakthroughResult,
    PyodideBreakthroughSolver,
    SUM4_PFAS,
    SUM20_PFAS,
    breakthrough_x_values,
    compound_properties,
    freundlich_parameters,
    molecular_weight_g_mol,
    ng_l_to_mol_m3,
)


class CadetBreakthroughSolver:
    """CADET-Python entry point, isolated for optional use."""

    def __init__(self, allow_fallback: bool = False):
        self.allow_fallback = allow_fallback

    def run(self, inputs: BreakthroughInput) -> BreakthroughResult:
        try:
            Cadet = importlib.import_module("cadet").Cadet
        except ImportError as exc:
            raise RuntimeError("CADET-Python is not installed") from exc

        try:
            logging.debug("CADET solver running")
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
        fallback = PyodideBreakthroughSolver()
        metadata = {str(item["name"]): item for item in inputs.metadata_pfas if item.get("name")}
        compounds = [
            compound
            for compound, c0_ng_l in inputs.influent_pfas.items()
            if float(c0_ng_l or 0) > 0
        ]
        if not compounds:
            return BreakthroughResult()

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

        for compound in compounds:
            params = freundlich_parameters(compound, inputs.compound_parameters.get(compound, {}))
            freundlich_k.append(float(params.get("freundlich_k", 100) or 100))
            one_over_n = float(params.get("freundlich_1n", 0.4) or 0.4)
            freundlich_n.append(1 / max(one_over_n, 1e-12))

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
        column.col_dispersion = ncomp * [0]
        column.film_diffusion = [mass_transfer] * ncomp
        column.par_diffusion = [mass_transfer] * ncomp
        column.adsorption_model = "FREUNDLICH_LDF"
        column.adsorption.is_kinetic = 1
        column.adsorption.fldf_kkin = [mass_transfer] * ncomp
        column.adsorption.fldf_kf = freundlich_k
        column.adsorption.fldf_n = freundlich_n
        column.init_c = [0] * ncomp
        column.init_q = [0] * ncomp
        column.discretization.spatial_method = "FV"
        column.discretization.ncol = 100
        column.discretization.npar = 5
        if column.unit_type == "GENERAL_RATE_MODEL":
            self._set_general_rate_discretization(model, [1] * ncomp)

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
        particle.discretization.spatial_method = "FV"
        particle.discretization.par_disc_type = "EQUIDISTANT"

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

    def _set_general_rate_discretization(self, model, n_bound=None, n_col=100) -> None:
        columns = {"GENERAL_RATE_MODEL"}

        for unit_name, unit in model.root.input.model.items():
            if "unit_" in unit_name and unit.unit_type in columns:
                unit.discretization.ncol = n_col
                unit.discretization.npar = 5

                if n_bound is None:
                    n_bound = unit.ncomp * [0]
                unit.discretization.nbound = n_bound

                unit.discretization.par_disc_type = "EQUIDISTANT_PAR"
                unit.discretization.use_analytic_jacobian = 1
                unit.discretization.reconstruction = "WENO"
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
        metadata: dict[str, dict[str, float]],
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
