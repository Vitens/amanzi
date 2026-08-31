from .model import Model
from .submodels.balance import Balance
import math
from .tower.compounds import Chemical
import bisect
import warnings
warnings.simplefilter("ignore")
from .submodels.loss import Loss
# import os
# srt_dir = os.getcwd()
# import bisect
# import pandas as pd
import logging
import numpy as np
from dataclasses import dataclass, field
from typing import Any
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


def _as_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


@dataclass
class BreakthroughResult:
    breakthrough: dict[str, list[dict[str, float]]] = field(default_factory=dict)
    peq_pfas: list[dict[str, float]] = field(default_factory=list)
    sum4_pfas: list[dict[str, float]] = field(default_factory=list)
    sum20_pfas: list[dict[str, float]] = field(default_factory=list)






logging.basicConfig(level=logging.DEBUG)


class Activatedcarbon(Model, Loss):
    parametric_model = ['base','model','activatedcarbon', 'filtration', 'pfas', 'micropollutants']

    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)
        self.configurations = config.get('configuration', {})
        
        config = config.get('configuration', {})
        config = config.get('parameters', {})

        self.loss = self.get_output('backwash_loss')
        self.sprayaeration = config.get('spray', False)
        self.packing_height = float(config.get('bed_height', 2.5))
        self.dimension = float(config.get('diameter', 2))
        self.packing_type = config.get('packing_type', 'NORA Supra 0.8')
        self.volumeflow = float(config.get('nominal_capacity', 100))
        self.capacity = float(config.get('nominal_capacity', 100))
        self.surface_area = float(config.get('surface_area', 100))
        self.compoundList = self.configurations.get('compound', {'x':0})
        self.advanced = config.get('advanced', False)
        self.fixed_replacement = config.get('fixed_replacement', True)
        self.renewal = int(config.get('replacement_interval', 1000))
        self.replacement_loading = float(config.get('replacement_loading', 0.5))
        self.filternumber = int(config.get('units', 1))
        self.staggered_replacement = config.get('staggered_replacement', 'no_staggering')
        self.fixed_staggering_interval = float(config.get('fixed_staggering_interval', 500))
        self.apparent_density = float(config.get('apparent_density', 0.5))
        self.particle_density = float(config.get('particle_density', 0.5))
        self.particle_diameter = float(config.get('particle_diameter', 0.04))
        self.bed_porosity = float(config.get('bed_porosity', 0.4))
        self.particle_porosity = float(config.get('particle_porosity', 0.5))
        self.waste_solution = None
        self.OMV_capacity = config.get('OMV_capacity',{})
        self.competition_coefficients = {}
        self.design_limit = config.get('design_limit', 'sum20PFAS_limit')
        self.mass_transfer_coefficient = float(config.get('mass_transfer_coefficient', 0.005))
    @property
    def backwash_programme(self):

        programme = self.parameters.get('backwash_programme', [])
        return programme
    @property
    def compound_removal_rates(self):
        removal_rates={}
        for PFAS in self.scenario['metaData']['customMicroComponents']['PFAS']:
            removal_rates[PFAS['name']] = PFAS['removalAKF']
        for Other in self.scenario['metaData']['customMicroComponents']['Other']:
            removal_rates[Other['name']] = Other['removalAKF']
        return removal_rates

    @property
    def _backwash_duration(self):
        return sum([p['time'] for p in self.backwash_programme]) / 60

    @property
    def _backwash_volume(self):
        surface = self.output_parameters['surface_area'].calculate(super().context)
        return sum([p['water'] * surface * p['time']/3600 for p in self.backwash_programme])

    @property
    def _backwash_max_rate(self):
        return max([p['water'] for p in self.backwash_programme] + [0])
        
    @staticmethod
    def kozeny_carman(p, v, d):
        d /= 1e3 # convert to mm
        v /= 3600 # convert to m/s
        return 180 * 1.3e-6 / 9.81 * (1-p)**2 / p**3 * v/d**2
    @property
    def packing_volume(self):
        return self.output_parameters['volume'].calculate(super().context)
    @property
    def context(self):
        ctx = super().context
        ctx['_backwash_duration'] = self._backwash_duration
        ctx['_backwash_volume'] = self._backwash_volume
        ctx['_backwash_max_rate'] = self._backwash_max_rate
        ctx['kozeny_carman'] = self.kozeny_carman
        ctx['aerated'] = self.aerated if hasattr(self, 'aerated') else self.quality.influent.product

        return ctx
    
    def wastestream_calculation(self, solution):
        return solution

    def compound_removal_efficiency(self, group, name, metadata_item):
        configured = next(
            (item for item in self.scenario['metaData']['customMicroComponents'][group] if item['name'] == name),
            metadata_item
        )
        return configured['removalAKF']

    def simpleExtraneousRemoval(self, solution):  
        components = getattr(self, 'scenario', {}).get('metaData', {}).get('customMicroComponents', {})
        for i in components.get('PFAS', []):
            name= i['name']
            removal_efficiency = self.compound_removal_efficiency('PFAS', name, i)
            if name in solution.extraneous['PFAS']:
                solution.extraneous['PFAS'][name]=solution.extraneous['PFAS'][name]*(1-(float(removal_efficiency)/100))
        for i in components.get('Other', [])  :
            name= i['name']
            removal_efficiency = self.compound_removal_efficiency('Other', name, i)
            if name in solution.extraneous['Other']:
                solution.extraneous['Other'][name]=solution.extraneous['Other'][name]*(1-(float(removal_efficiency)/100))    
        return solution
    


    @staticmethod
    def _breakthrough_series(x_values, y_values):
        return [
            {'x': float(x), 'y': float(y)}
            for x, y in zip(x_values, y_values)
        ]

    @staticmethod
    def _breakthrough_dict(breakthrough_result):
        if hasattr(breakthrough_result, 'breakthrough'):
            return breakthrough_result.breakthrough
        return breakthrough_result
    def breakthrough_calculation(self, solution):
        ##### Simple breakthrough calculation #####
        ##### assuming stationary flow and constant influent concentration, no dispersion or axial mixing, constant overall mass transfer coefficient#####

        solution = self.unitcheck(solution)
        influent_pfas = {
            compound: float(concentration or 0)
            for compound, concentration in solution.extraneous.get('PFAS', {}).items()
            if float(concentration or 0) > 0
        }
        if not influent_pfas:
            return BreakthroughResult()

        ebct = self.packing_volume/(self.volumeflow)  # hours
        mass_transfer_coefficient = self.mass_transfer_coefficient
        components = getattr(self, 'scenario', {}).get('metaData', {}).get('customMicroComponents', {})
        metadata = {
            str(item['name']): item
            for item in components.get('PFAS', [])
            if item.get('name')
        }

        density = self.parameters.get('apparent_density', self.apparent_density)
        filterruntime = np.linspace(0, 365*24, 200)
        bedvolumes = filterruntime / ebct
        breakthrough = {}
        peq = np.zeros(len(bedvolumes))
        sum4 = np.zeros(len(bedvolumes))
        sum20 = np.zeros(len(bedvolumes))
        compound_parameters = self._mixture_compound_parameters(influent_pfas)
        freundlich_capacity = self.multicomponent_freundlich_capacity(
            influent_pfas,
            compound_parameters=compound_parameters,
            competition=self.competition_coefficients,
            extra_competitors_ug_l=self._doc_extra_competitors_ug_l(solution),
        )

        for compound, inlet_concentration in influent_pfas.items():  # inlet_concentration: ng/l
            per_compound_capacity = freundlich_capacity['per_compound'].get(compound, 0)  # µg/g GAC
            capacity_term = max(per_compound_capacity * 1000 * density, 0)  # ng/lGAC; µg/g × kg/m³ × 1000
            exponent = mass_transfer_coefficient * ebct* 3600 * (  # k: 1/s; 30×60: s (characteristic EBCT)
                1 - (bedvolumes * inlet_concentration / (capacity_term))  # BV × ng/l / ng/l → dimensionless
            )
            eq_concentration = inlet_concentration / (1 + np.exp(exponent))  # ng/l
            c_over_c0 = np.clip(eq_concentration / inlet_concentration, 0, 1)  # -
            breakthrough[compound] = self._breakthrough_series(bedvolumes, c_over_c0)  # x: BV; y: -

            peq_factor = float(metadata.get(compound, {}).get('PEQ', 1) or 1)  # -
            effluent = inlet_concentration * c_over_c0 * peq_factor  # ng/l
            peq += effluent  # ng/l
            if compound in SUM4_PFAS:
                sum4 += effluent  # ng/l
            if compound in SUM20_PFAS:
                sum20 += effluent  # ng/l

        return BreakthroughResult(
            breakthrough=breakthrough,
            peq_pfas=self._breakthrough_series(bedvolumes, peq),
            sum4_pfas=self._breakthrough_series(bedvolumes, sum4),
            sum20_pfas=self._breakthrough_series(bedvolumes, sum20),
        )
    def multicomponent_freundlich_capacity(
        self,
        influent_ng_l: dict[str, float],
        compound_parameters: dict[str, dict[str, Any]] | None = None,
        competition: dict[str, float] | None = None,
        extra_competitors_ug_l: dict[str, float] | None = None,
    ) -> dict[str, Any]:
        """Closed-form competitive (Sheindorf-Rebhun-Sheintuch) Freundlich capacity."""
        concentrations_ug_l: dict[str, float] = {}
        for compound, c_ng_l in (influent_ng_l or {}).items():
            c_ug_l = max(_as_float(c_ng_l, 0), 0) / 1000
            if c_ug_l > 0:
                concentrations_ug_l[compound] = c_ug_l

        extra_ug_l: dict[str, float] = {}
        for name, c_ug_l in (extra_competitors_ug_l or {}).items():
            c_ug = max(_as_float(c_ug_l, 0), 0)
            if c_ug > 0:
                extra_ug_l[name] = c_ug

        per_compound: dict[str, float] = {}
        total_ug_g = 0.0
        weights = competition or {}

        extra_sum = sum(
            self._competition_weight(name, weights, compound_parameters) * c_j
            for name, c_j in extra_ug_l.items()
        )
        for compound, c_i in concentrations_ug_l.items():
            k_f, one_over_n = self._compound_freundlich_params(compound, compound_parameters)
            competition_sum = extra_sum + sum(
                self._competition_weight(other, weights, compound_parameters) * c_j
                for other, c_j in concentrations_ug_l.items()
            )
            if competition_sum <= 0:
                continue

            q_i = k_f * c_i * competition_sum ** (one_over_n - 1)
            per_compound[compound] = q_i
            total_ug_g += q_i

        return {"per_compound": per_compound, "total_ug_g": total_ug_g}

    def _affinity_weight(self, compound: str, compound_parameters: dict[str, dict[str, Any]] | None = None) -> float:
        k_i, _ = self._compound_freundlich_params(compound, compound_parameters)
        k_pfoa, _ = self._compound_freundlich_params('PFOA', compound_parameters)
        return k_i / max(k_pfoa, 1e-12)

    def _competition_weight(
        self,
        compound: str,
        weights: dict[str, float] | None = None,
        compound_parameters: dict[str, dict[str, Any]] | None = None,
    ) -> float:
        if weights and compound in weights and weights[compound] is not None:
            return max(_as_float(weights[compound], 0), 0)
        return self._affinity_weight(compound, compound_parameters)

    def _toc_mg_l(self, solution) -> float:
        toc = getattr(solution, 'extraneous', {}).get('TOC', 0)
        if toc is None or toc == {}:
            return 0.0
        return max(_as_float(toc, 0), 0)

    def _doc_competition_enabled(self) -> bool:
        include = self.parameters.get('include_doc_competition', True)
        return include is not False and include not in (0, 'false', 'False')

    def _doc_extra_competitors_ug_l(self, solution) -> dict[str, float]:
        if not self._doc_competition_enabled():
            return {}
        toc_mg = self._toc_mg_l(solution)
        if toc_mg <= 0:
            return {}
        # TOC is mg/L; SRS mixture uses µg/L (same basis as PFAS after ng/L → µg/L).
        return {'DOC': toc_mg * 1000}

    def _is_user_edited_coefficient(self, compound: str) -> bool:
        scenario = getattr(self, 'scenario', None)
        if scenario is None:
            return False
        try:
            meta = scenario['metaData']
        except (TypeError, KeyError):
            meta = {}
        if not isinstance(meta, dict):
            return False
        edited = ((meta.get('activatedcarbon') or {}).get('userEditedCoefficients') or {})
        return bool(edited.get(compound))

    def _compound_freundlich_params(self,
        compound: str,
        compound_parameters: dict[str, dict[str, Any]] | None = None,
    ) -> tuple[float, float]:
        configured = (compound_parameters or {}).get(compound, {})
        k = self.parameters.get(f"{compound}_Freundlich_k", self.parameters.get(f"{compound}_freundlich_k"))
        default_k = 250 if compound == 'DOC' else 100
        default_1n = 0.45 if compound == 'DOC' else 0.4
        if k is None:
            k = configured.get("freundlich_k", default_k)
        one_over_n = self.parameters.get(f"{compound}_Freundlich_1n", self.parameters.get(f"{compound}_freundlich_1n"))
        if one_over_n is None:
            one_over_n = configured.get("freundlich_1n", default_1n)
        return max(_as_float(k, default_k), 1e-12), max(_as_float(one_over_n, default_1n), 1e-12)

    def _mixture_compound_parameters(self, compounds) -> dict[str, dict[str, Any]]:
        parameters = {}
        for compound in compounds:
            k, one_over_n = self._compound_freundlich_params(compound)
            parameters[compound] = {'freundlich_k': k, 'freundlich_1n': one_over_n}
        if self._doc_competition_enabled():
            k, one_over_n = self._compound_freundlich_params('DOC')
            parameters['DOC'] = {'freundlich_k': k, 'freundlich_1n': one_over_n}
        return parameters
    def _bedvolumes_per_day(self):
        volume = self.output_parameters['volume'].calculate(super().context)
        flow_m3_h = float(self.parameters.get('nominal_capacity', self.capacity))
        return flow_m3_h * 24 / max(volume, 1e-9)




    def _bed_volumes_at_replacement(self):
        volume = self.output_parameters['volume'].calculate(super().context)
        flow_m3_h = float(self.parameters.get('nominal_capacity', self.capacity))
        replacement_interval_days = float(self.parameters.get('replacement_interval', self.renewal))
        return flow_m3_h * 24 * replacement_interval_days / max(volume, 1e-9)

    @staticmethod
    def _interpolate_curve(series, x_value):
        if not series:
            return 0
        if x_value <= series[0]['x']:
            return series[0]['y']
        for index in range(1, len(series)):
            left = series[index - 1]
            right = series[index]
            if x_value <= right['x']:
                span = right['x'] - left['x']
                if span == 0:
                    return right['y']
                fraction = (x_value - left['x']) / span
                return left['y'] + (right['y'] - left['y']) * fraction
        return series[-1]['y']

    def _uses_staggering(self):
        return (
            self.staggered_replacement in ('fixed_staggering', 'limit_staggering')
            and max(self.filternumber, 1) > 1
        )

    @staticmethod
    def _staggered_filter_age(x, index, interval, n):
        """Cyclic age from first renewal: (x + i·Δ) % (N·Δ). At x=0 ages are 0, Δ, …, (N-1)Δ."""
        if interval <= 0:
            return max(x, 0)
        lifetime = n * interval
        if lifetime <= 0:
            return max(x, 0)
        return (x + index * interval) % lifetime

    def _blend_at_ages(self, series, ages):
        if not ages:
            return 0
        return sum(self._interpolate_curve(series, age) for age in ages) / len(ages)

    def _peak_blend(self, series, interval, n):
        """Blend just before replacement: ages Δ, 2Δ, …, N·Δ (do not wrap the oldest to 0)."""
        interval = max(float(interval), 0)
        if interval <= 0:
            return self._interpolate_curve(series, 0)
        ages = [(index + 1) * interval for index in range(n)]
        return self._blend_at_ages(series, ages)

    def _stagger_interval_at_limit(self, series, limit_value):
        n = max(self.filternumber, 1)
        if not series:
            return 0.0
        if n <= 1:
            y_values = [point['y'] for point in series]
            closest_index = self.find_closest(y_values, limit_value)
            return series[closest_index]['x']

        x_max = series[-1]['x']
        delta_hi = x_max / n
        if delta_hi <= 0:
            return 0.0

        y_lo = self._peak_blend(series, delta_hi * 1e-9, n)
        y_hi = self._peak_blend(series, delta_hi, n)
        if y_lo >= limit_value:
            return delta_hi * 1e-9
        if y_hi < limit_value:
            return delta_hi

        lo, hi = 0.0, delta_hi
        for _ in range(40):
            mid = (lo + hi) / 2
            if self._peak_blend(series, mid, n) < limit_value:
                lo = mid
            else:
                hi = mid
        return hi

    def _limit_curve_and_value(self, peq, sum4, sum20):
        design_limit = self.parameters.get('design_limit', self.design_limit)
        limit_curves = {
            'sum20PFAS_limit': (sum20, self.database.sum20PFAS_limit),
            'sum4PFAS_limit': (sum4, self.database.sum4PFAS_limit),
            'PEQ_limit': (peq, self.database.PEQ_limit),
        }
        return limit_curves.get(design_limit, limit_curves['sum20PFAS_limit'])

    def _resolved_stagger_interval_bv(self, breakthrough_result=None):
        if not self._uses_staggering():
            return None
        if self.staggered_replacement == 'fixed_staggering':
            return self.fixed_staggering_interval * self._bedvolumes_per_day()
        peq = getattr(breakthrough_result, 'peq_pfas', None) or []
        sum4 = getattr(breakthrough_result, 'sum4_pfas', None) or []
        sum20 = getattr(breakthrough_result, 'sum20_pfas', None) or []
        curve, limit_value = self._limit_curve_and_value(peq, sum4, sum20)
        return self._stagger_interval_at_limit(curve, limit_value)

    def _staggered_value(self, series, interval_bed_volumes):
        n = max(self.filternumber, 1)
        if self.staggered_replacement == 'no_staggering' or n <= 1:
            return self._interpolate_curve(series, interval_bed_volumes)
        return self._peak_blend(series, interval_bed_volumes, n)

    def _staggered_series(self, series, interval_bed_volumes):
        if not series:
            return series
        n = max(self.filternumber, 1)
        if self.staggered_replacement == 'no_staggering' or n <= 1:
            return series
        interval = max(float(interval_bed_volumes), 0)
        return [
            {
                'x': point['x'],
                'y': sum(
                    self._interpolate_curve(
                        series,
                        self._staggered_filter_age(point['x'], index, interval, n),
                    )
                    for index in range(n)
                ) / n,
            }
            for point in series
        ]

    def advancedExtraneousRemoval(self, solution, breakthrough_result=None, interval_bed_volumes=None):
        effluent = solution.copy()
        source = breakthrough_result if breakthrough_result is not None else self.breakthrough_calculation(solution)
        result = self._breakthrough_dict(source)

        if interval_bed_volumes is None:
            interval_bed_volumes = self._resolved_stagger_interval_bv(source)
        if interval_bed_volumes is None:
            interval_bed_volumes = self._bed_volumes_at_replacement()

        for compound, series in result.items():
            if compound not in effluent.extraneous.get('PFAS', {}):
                continue
            ratio = self._staggered_value(series, interval_bed_volumes)
            effluent.extraneous['PFAS'][compound] = solution.extraneous['PFAS'][compound] * ratio

        return effluent


    
    def spray_aeration(self, solution):
        solution = solution.copy()
        co2_removal_efficiency = self.parameters['co2_removal_efficiency']
        ch4_removal_efficiency = self.parameters['ch4_removal_efficiency']
        o2_saturation = self.parameters['o2_saturation']

        # calculate oxygen saturation and CO2 removal
        air = self.pp.add_gas({f'O2(g)': 0.21, 'Ntg(g)': 0.79, 'CO2(g)': 0.043/100}, fixed_pressure=True, fixed_volume=False, volume=1000, pressure=1)

        saturated = solution.copy().interact(air)

        max_o2 = saturated.total('O2')
        min_co2 = saturated.total('CO2')
        saturated.forget()
        o2_to_add = max(0, max_o2 * o2_saturation - solution.total('O2'))
        co2_to_remove = (solution.total('CO2')-min_co2) * co2_removal_efficiency
        ch4_to_remove = solution.total('Mtg') * ch4_removal_efficiency

        solution.change({ "O2": o2_to_add, "CO2": -co2_to_remove, "Mtg": -ch4_to_remove })

        # replace inert oxygen with free oxygen

        # effciency_co2 = self.calculate_efficiency('CO2', RQ , fall_height)
        # effciency_ch4 = self.calculate_efficiency('Mtg', RQ , fall_height)
        # effciency_O2 = self.calculate_efficiency('Oxg', RQ , fall_height)

        # max Oxygen saturation linear interpolation dependend on water temperature (5-20 Celsius)
        # mg/l to mmol/l
        return solution


    def unitcheck(self,solution):
        # ng/l is the default unit for PFAS influent and effluent
        components = getattr(self, 'scenario', {}).get('metaData', {}).get('customMicroComponents', {})
        pfas = getattr(solution, 'extraneous', {}).get('PFAS', {})
        for i in components.get('PFAS', []):
            name = i.get('name')
            if name not in pfas:
                continue
            unit = i.get('unit')
            if unit == 'mg/l':
                pfas[name] = _as_float(pfas[name], 0) * 1000000
            elif unit in ('μg/l', 'µg/l', 'ug/l'):
                pfas[name] = _as_float(pfas[name], 0) * 1000
        return solution
    def check_competition_coefficient(self):
        self.competition_coefficients = {}
        try:
            pfas_keys = list((self.quality.influent.product.extraneous.get('PFAS') or {}).keys())
        except (AttributeError, TypeError):
            pfas_keys = []
        for pfas in pfas_keys:
            stored = self.parameters.get(pfas + '_competition_coefficient')
            if self._is_user_edited_coefficient(pfas) and stored is not None:
                self.competition_coefficients[pfas] = max(_as_float(stored, 0), 0)
            else:
                auto = self._affinity_weight(pfas)
                self.competition_coefficients[pfas] = auto
                self.parameters[pfas + '_competition_coefficient'] = auto
        if self._doc_competition_enabled():
            stored = self.parameters.get('DOC_competition_coefficient')
            if self._is_user_edited_coefficient('DOC') and stored is not None:
                self.competition_coefficients['DOC'] = max(_as_float(stored, 0), 0)
            else:
                auto = self._affinity_weight('DOC')
                self.competition_coefficients['DOC'] = auto
                self.parameters['DOC_competition_coefficient'] = auto
        return self.competition_coefficients


    def run_quality(self, type, total_inflow,solution):

        if(type == 'flush'):
            # add load to waste solution
            self.waste_solution = self.wastestream_calculation(solution.copy())
            return self.waste_solution

        if (type == 'product'):
            solution = solution.copy()
            self.check_competition_coefficient()
            if(self.sprayaeration):
                solution = self.spray_aeration(solution)
                self.aerated = solution.copy()
            effluent = solution.copy()
            # if self.advanced:
            #     effluent = self.advancedExtraneousRemoval(solution)
            # else:
            #     effluent = self.simpleExtraneousRemoval(solution)

            return effluent
               
        return solution
    
    

    def find_closest(self,nums, target):
        # Find the position where target should be inserted to maintain sorted order
        pos = bisect.bisect_left(nums, target)

        # If the target is the first element or exactly matches an element in the list
        if pos == 0:
            return 0
        if pos == len(nums):
            return len(nums) - 1

        # If target is not in nums, check the closest number (either before or after)
        before = nums[pos - 1]
        after = nums[pos]

        if after - target < target - before:
            return pos
        else:
            return pos - 1

    def design(self):
        influent = self.unitcheck(self.quality.influent.product.copy())
        self.check_competition_coefficient()
        eff = {}
        peqPFAS = []
        sum4 = []
        sum20 = []
        interval_bv = None
        volumeGAC = self.output_parameters['volume'].calculate(super().context) # m³

        if(self.sprayaeration):
            influent = self.spray_aeration(influent.copy())
            self.aerated = influent.copy()
        if True:
            breakthrough_result = self.breakthrough_calculation(influent.copy())
            interval_bv = self._resolved_stagger_interval_bv(breakthrough_result)
            effluent = self.advancedExtraneousRemoval(influent.copy(), breakthrough_result, interval_bv)
            eff = breakthrough_result.breakthrough
            if interval_bv is not None:
                peqPFAS = self._staggered_series(breakthrough_result.peq_pfas, interval_bv)
                sum4 = self._staggered_series(breakthrough_result.sum4_pfas, interval_bv)
                sum20 = self._staggered_series(breakthrough_result.sum20_pfas, interval_bv)
            else:
                peqPFAS = breakthrough_result.peq_pfas
                sum4 = breakthrough_result.sum4_pfas
                sum20 = breakthrough_result.sum20_pfas
        else:
            effluent = self.simpleExtraneousRemoval(influent.copy())
            interval_bv = None

        # choose the design limit
        sum20_concentration_influent = sum(influent.extraneous['PFAS'][pfas] for pfas in influent.extraneous['PFAS'] if pfas in SUM20_PFAS)
        sum4_concentration_influent = sum(influent.extraneous['PFAS'][pfas] for pfas in influent.extraneous['PFAS'] if pfas in SUM4_PFAS)
        peq_concentration_influent = sum(influent.extraneous['PFAS'][pfas]*self.parameters.get(pfas + '_PEQ', 1) for pfas in influent.extraneous['PFAS'])
        sum20_concentration_effluent = sum(effluent.extraneous['PFAS'][pfas] for pfas in effluent.extraneous['PFAS'] if pfas in SUM20_PFAS)
        sum4_concentration_effluent = sum(effluent.extraneous['PFAS'][pfas] for pfas in effluent.extraneous['PFAS'] if pfas in SUM4_PFAS)
        peq_concentration_effluent = sum(effluent.extraneous['PFAS'][pfas]*self.parameters.get(pfas + '_PEQ', 1) for pfas in effluent.extraneous['PFAS'])
        design_limit = self.parameters.get('design_limit', 'sum20PFAS_limit')
        limit_breakers = {}
        if design_limit == 'sum20PFAS_limit':
            # find PFAS over limit
            for pfas in influent.extraneous['PFAS']:
                if sum20_concentration_influent > self.database.sum20PFAS_limit:
                    limit_breakers[pfas] = influent.extraneous['PFAS'][pfas]
        elif design_limit == 'sum4PFAS_limit':
            # find PFAS over limit
            for pfas in influent.extraneous['PFAS']:
                if sum4_concentration_influent > self.database.sum4PFAS_limit:
                    limit_breakers[pfas] = influent.extraneous['PFAS'][pfas] 
        elif design_limit == 'PEQ_limit':
            if peq_concentration_influent > self.database.PEQ_limit:
                limit_breakers['PEQ'] = sum(influent.extraneous['PFAS'].values())
        else:
            #self set limit
            limit_breakers = {pfas: 1 for pfas in influent.extraneous['PFAS']}

        # Mixture equilibrium capacity via closed-form competitive (SRS) Freundlich.
        # Accounts for inter-compound competition instead of assuming an equal,
        # independent carbon share per compound.

        volumeGAC =self.output_parameters['volume'].calculate(super().context) # m³
        compound_parameters = self._mixture_compound_parameters(influent.extraneous['PFAS'])
        mixture_capacity = self.multicomponent_freundlich_capacity(
            influent.extraneous['PFAS'],
            compound_parameters=compound_parameters,
            competition=self.competition_coefficients,
            extra_competitors_ug_l=self._doc_extra_competitors_ug_l(influent),
        )
        total_capacity = mixture_capacity['total_ug_g'] #mg/kgGAC (1 ug/g == 1 mg/kg)

        capacityFactor = self.apparent_density*total_capacity #mg/m³GAC

        n = max(self.filternumber, 1)
        stagger_interval_BV = interval_bv if interval_bv is not None else 0
        if interval_bv is not None:
            regeneration_BV = n * interval_bv
            bv_per_day = self._bedvolumes_per_day()
            regeneration = regeneration_BV / max(bv_per_day, 1e-9)
        elif self.fixed_replacement:
            regeneration = self.renewal
            regeneration_BV = self.renewal
        else:
            curve, limit_value = self._limit_curve_and_value(peqPFAS, sum4, sum20)
            if curve:
                y_values = [point['y'] for point in curve]
                closest_index = self.find_closest(y_values, limit_value)
                bedvolume_closest_value = curve[closest_index]['x']
            else:
                bedvolume_closest_value = 0
            regeneration = bedvolume_closest_value / self.capacity / self.surface_area * 60/60/24 # BV to days
            regeneration_BV = bedvolume_closest_value

        color_removal_efficiency = 0
        toc_removal_efficiency = 0

        for i in self.scenario['metaData']['customMicroComponents']['Other']:
            if i['name'] == 'Color':
                color_removal_efficiency = i['removalAKF']
            if i['name'] == 'TOC':
                toc_removal_efficiency = i['removalAKF']

        if 'Color' in self.quality.influent.product.extraneous and self.quality.influent.product.extraneous['Color'] != {}:
            color_removal_efficiency = self.quality.influent.product.extraneous['Color']*color_removal_efficiency
        if 'TOC' in self.quality.influent.product.extraneous and self.quality.influent.product.extraneous['TOC'] != {}:
            toc_removal_efficiency = self.quality.influent.product.extraneous['TOC']*toc_removal_efficiency

        influentOMV = {}
        influentOMV['Color'] = self.quality.influent.product.extraneous['Color']
        influentOMV['TOC'] = self.quality.influent.product.extraneous['TOC']
        influentOMV['Sum20PFAS'] = sum20_concentration_influent
        influentOMV['Sum4PFAS'] = sum4_concentration_influent
        influentOMV['PEQ'] = peq_concentration_influent

        effluentOMV = {}
        effluentOMV['Color'] = self.quality.effluent.product.extraneous['Color']*color_removal_efficiency
        effluentOMV['TOC'] = self.quality.effluent.product.extraneous['TOC']*toc_removal_efficiency
        effluentOMV['Sum20PFAS'] = sum20_concentration_effluent
        effluentOMV['Sum4PFAS'] = sum4_concentration_effluent
        effluentOMV['PEQ'] = peq_concentration_effluent
        ebct = self.packing_volume/(self.volumeflow)
        bedvolumes = 365 * 24 / ebct

        return {
            'influent': influentOMV
            ,
            'effluent': effluentOMV
            ,
            'model': {
                'regeneration': regeneration,
                'regeneration_BV': regeneration_BV,
                'stagger_interval_BV': stagger_interval_BV,
                'EBCT' : self.packing_volume/(self.volumeflow/60),
                'peqPFAS':peqPFAS,
                'sum4PFAS': sum4,
                'sum20PFAS': sum20,
                'Volume': self.packing_volume,
                'bedvolume_jaar': bedvolumes,
                'breakthrough': eff,
                'PFAS': self.quality.influent.product.extraneous['PFAS']
            },
            'competition_coefficients': self.competition_coefficients
        }
    @property
    def emitter_solutions(self):
        return {'waste': self.waste_solution}