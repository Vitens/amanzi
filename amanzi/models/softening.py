from .model import Model
from .submodels.balance import Balance
import numpy as np

class Softening(Model, Balance):
    def __init__(self, config, pp) -> None:
        super().__init__(config, pp)
        config = config.get('configuration', {})

        self.base_chemical = config.get('base_chemical', 'Ca(OH)2')
        self.acid_chemical = config.get('acid_chemical', 'CO2')
        self.base_dosing = float(config.get('base_dosage', 0))
        self.acid_dosing = float(config.get('acid_dosage', 0))

        self.acid_position = config.get('acid_position', 'effluent')
        self.bypass = float(config.get('bypass', 0.2))

    
    def soften(self, solution, base_chemical, base_dosing, acid_chemical, acid_dosing, bypass):


        reactor_in = solution.copy() # reactor influent

        bypass_in = solution.copy() # bypass influent

        # dose chemical
        dosed = reactor_in.copy().add(base_chemical, base_dosing, 'mmol')

        softened = dosed.copy().desaturate('Calcite', to_si=0.6)

        # if acid_position is product or bypass, then acidify
        if self.acid_position == 'product':
            neutralized = softened.copy().add(acid_chemical, acid_dosing, 'mmol')
        elif self.acid_position == 'bypass':
            neutralized = bypass_in.copy().add(acid_chemical, acid_dosing, 'mmol')

        bypass_solution = bypass_in if self.acid_position != 'bypass' else neutralized
        softened_solution = softened if self.acid_position != 'product' else neutralized

        # effluent is mixture of softened and bypass
        mixed = softened_solution * (1-bypass) + bypass_solution * (bypass)

        if self.acid_position == 'effluent':
            neutralized = mixed.copy().add(acid_chemical, acid_dosing, 'mmol')
        
        effluent = mixed if self.acid_position != 'effluent' else neutralized
        
        return effluent, [dosed, softened, mixed, neutralized]

    def run_model(self, type, total_inflow, solution):
        s, _ = self.soften(solution, self.base_chemical, self.base_dosing, self.acid_chemical, self.acid_dosing, self.bypass)
        return s

    def design(self):

        effluent, steps = self.soften(self.influent, self.base_chemical, self.base_dosing, self.acid_chemical, self.acid_dosing, self.bypass)

        steps = [self.influent] + steps + [effluent]

        values = {
            'pH': lambda s: s.pH,
            'HCO3': lambda s: s.total('HCO3', 'mg'),
            'CO2': lambda s: s.total('CO2', 'mg'),
            'Ca': lambda s: s.total('Ca', 'mg'),
            'Mg': lambda s: s.total('Mg', 'mg'),
            'hardness': lambda s: s.hardness,
            'ccpp90': lambda s: s.ccpp(90),
            'si': lambda s: s.si('Calcite'),
            'sc': lambda s: s.sc20/10,
        }
        names = ['influent', 'dosed', 'softened', 'mixed', 'neutralized', 'effluent']

        resp = {}

        for i, s in enumerate(steps):
            step_results = {}
            for n, v in values.items():
                step_results[n] = v(s)
            resp[names[i]] = step_results
        
        # sweep dosage for naoh and caoh
        dosage = np.linspace(0, 4, 40)

        ## generate charts
        charts = {}

        for chemical in ['NaOH', 'Ca(OH)2']:

            chemcharts = {'dosed_pH': [], 'softened_pH': [], 'softened_hh': [], 'softened_hco3': [], 'softened_sc': []}

            for d in dosage:
                effluent, [dosed, softened, mixed, neutralized] = self.soften(self.influent, chemical, d, self.acid_chemical, self.acid_dosing, self.bypass)

                chemcharts['dosed_pH'].append({'x': d, 'y': dosed.pH})
                chemcharts['softened_pH'].append({'x': d, 'y': softened.pH})

                chemcharts['softened_hh'].append({'x': d, 'y': softened.hardness})
                chemcharts['softened_hco3'].append({'x': d, 'y': softened.total('HCO3', 'mg')})
                
                chemcharts['softened_sc'].append({'x': d, 'y': softened.sc20/10})

            charts[chemical] = chemcharts
        
        resp['charts'] = charts
        
        return resp




