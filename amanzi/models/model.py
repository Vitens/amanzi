from dotmap import DotMap
from .parametric import ParametricModel
import logging

class Model(ParametricModel):
    parametric_model = [] # default to no parametric model

    def __init__(self, config, pp):
        super().__init__(config)
        self.uid = config.get('uid', "")
        self.type = config.get("type", "")
        self.name = config.get("name", "")
        self.category = config.get("category", "")
        self.emitter = False

        self.config = config

        self.connections = []

        self.pp = pp

        self.index = None # index of the model in the scenario, set by quality solver during solve pass
        self.database = None # database object, set by scenario during initialization

        """ Solver namespace parameters """
        self.quantity = DotMap({
            'inflow': { 'product': 0, 'waste': 0, 'flush': 0 },
            'outflow': { 'product': 0, 'waste': 0, 'flush': 0 }
        })
        self.quality = DotMap({
            'influent': { 'product': None, 'waste': None, 'flush': None },
            'effluent': { 'product': None, 'waste': None, 'flush': None }
        })
        self.hydraulics = DotMap({
            'head_in': 0, # head at the inlet
            'head_out': 0, # head at the outlet
            'integrated_booster': False, # whether the model has an integrated booster
            'booster_head': 0, # head supplied by the integrated booster pump
            'efficiency': 0, # efficiency of the booster pump
        })
        self.energy = DotMap({
            'model_specific_consumption': 0, # energy consumption per m3 produced by model (kWh/m3)
            'specific_consumption': 0, # energy consumption per m3 produced by the treatment plant (kWh/m3)
            'total_consumption': 0 # total energy consumption per year (kWh/year)
        })
        self.sustainability = DotMap({
            'model_specific_emission': 0, # energy consumption per m3 produced by model (gCO2-eq/m3)
            'specific_emission': 0, # energy consumption per m3 produced by the treatment plant (gCO2-eq/m3)
            'total_emission': 0 # total energy consumption per year (gCO2-eq/year)
        })
        self.chemicals = DotMap({
            # dotmap with chemical consumptions in gAS/m3
            'lye': 0,
            'lime': 0,
        }, _dynamic=False)
    
    # placeholder for model quality run
    def run_quality(self, type, total_inflow, solution):
        logging.warning(f'Quality not implemented for {self.type}')
        return solution

    # calculate minor loss, either as percentage of inflow or as a fixed value
    @property
    def minorloss(self):
        if self.config.get('configuration', {}).get('minorloss_method', 'percentage') != 'percentage':
            return float(self.config.get('configuration', {}).get('minorloss', 0))
        return 0
    
    @property
    def minorloss_percentage(self):
        if self.config.get('configuration', {}).get('minorloss_method', 'percentage') == 'percentage':
            return 1-float(self.config.get('configuration', {}).get('minorloss', 0))
        return 1

    @property
    def emitter_solutions(self):
        return {}

    @property
    def upstream_connections(self):
        upstream = {}
        for c in self.connections:
            if(c.to_model == self):
                upstream.setdefault(c.type, []).append(c)
        return upstream
    
    @property
    def downstream_connections(self):
        downstream = {}
        for c in self.connections:
            if(c.from_model == self):
                downstream.setdefault(c.type, []).append(c)
        return downstream
    
    @property
    def anchors_connections(self):
        anchors = {}
        for c in self.connections:
            anchor = c.from_anchor if c.from_model == self else c.to_anchor
            anchors.setdefault(anchor, []).append(c)

        return anchors

    def design(self):
        # boilerplate
        return {}

    def run_design(self):
        # run model for design
        designData = self.design()
        designData['parameters'] = self.parameters
        designData['tables'] = self.generate_tables()
        # get all outputs
        designData['outputs'] = {o.name: {'precision': o.precision, 'value': o.calculate(self.context), 'uom': o.uom, 'order': i, 'equation': o.equation, 'section': o.section, 'category': o.category, 'namespace': o.namespace} for i,o in enumerate(self.output_parameters.values())}

        quality = {}
        # gather quality data
        for direction, solutions in self.quality.items():
            for solution_type, solution in solutions.items():
                if solution:
                    quality[f'{direction}_{solution_type}'] = solution.summary

        designData['quality'] = quality

        return designData


