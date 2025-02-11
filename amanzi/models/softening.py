from .model import Model
from .submodels.balance import Balance
import numpy as np
from scipy.optimize import fmin

class Softening(Model, Balance):

    parametric_model = ['base', 'model', 'softening']

    def __init__(self, config, pp) -> None:
        super().__init__(config, pp)

        self.base_chemical = self.parameters['base_chemical']
        self.to_si = self.parameters['soften_to_si']
        self.acid_chemical = self.parameters['acid_chemical']
        self.base_dosing = float(self.parameters['base_dosage'])
        self.acid_dosing = float(self.parameters['acid_dosage'])

        self.acid_position = self.parameters['acid_position']

        bypass_open = float(self.parameters['bypass_open'])
        reactor_capacity = float(self.parameters['nominal_capacity'])
        bypass_capacity = float(self.parameters['bypass_capacity'])

        bypass_flow = bypass_open * bypass_capacity

        self.fe_capture = float(self.parameters['fe_capture'])
        self.mn_capture = float(self.parameters['mn_capture'])

        self.total_flow = reactor_capacity + bypass_flow
        self.bypass = bypass_flow / self.total_flow

    def soften(self, solution, base_chemical, base_dosing, acid_chemical, acid_dosing, bypass):

        reactor_in = solution.copy() # reactor influent

        bypass_in = solution.copy() # bypass influent

        # dose chemical
        dosed = reactor_in.copy().add(base_chemical, base_dosing, 'mmol')

        if self.fe_capture > 0 and dosed.total('[Fe+2]','mmol') > 0:
            dosed.remove('[Fe+2]CO3', dosed.total('[Fe+2]','mmol') * self.fe_capture, 'mmol')
        if self.mn_capture > 0 and dosed.total('[Mn+2]','mmol') > 0:
            dosed.remove('[Mn+2]CO3', dosed.total('[Mn+2]','mmol') * self.mn_capture, 'mmol')

        softened = dosed.copy().desaturate('Calcite', to_si=self.to_si)

        # if acid_position is product or bypass, then acidify
        if self.acid_position == 'reactor-outlet':
            neutralized = softened.copy().add(acid_chemical, acid_dosing, 'mmol')
        elif self.acid_position == 'bypass':
            neutralized = bypass_in.copy().add(acid_chemical, acid_dosing, 'mmol')

        bypass_solution = bypass_in if self.acid_position != 'bypass' else neutralized
        softened_solution = softened if self.acid_position != 'reactor-outlet' else neutralized

        # effluent is mixture of softened and bypass
        mixed = softened_solution * (1-bypass) + bypass_solution * (bypass)

        if self.acid_position == 'after-bypass':
            neutralized = mixed.copy().add(acid_chemical, acid_dosing, 'mmol')
        
        effluent = mixed if self.acid_position != 'after-bypass' else neutralized

        return effluent, [dosed, softened, mixed, neutralized]

    def run_quality(self, type, total_inflow, solution):
        s, _ = self.soften(solution, self.base_chemical, self.base_dosing, self.acid_chemical, self.acid_dosing, self.bypass)
        return s

    @property
    def methods(self):
        return super().methods | {
            'porosity': self.porosity
        }
    
    @staticmethod
    def porosity(pellet_diameter, pellet_density, velocity):
        g = 9.81 # gravity constant m/s^2
        v = velocity # m/s
        u = 1.3e-6 # m^2/s
        dp = pellet_diameter # m
        rho_w = 1000 # water density kg/m^3
        rho_p = pellet_density # pellet density kg/m^3

        def fn(x):
            return abs(130 * (v**1.2) / g * (u**0.8)/(dp**1.8) * (rho_w / (rho_p - rho_w)) - (x**3 / (1-x)**0.8))


        resp = fmin(fn, 0.5, disp=False)

        return resp[0]

    def design(self):

        influent = self.quality.influent.product

        effluent, steps = self.soften(influent, self.base_chemical, self.base_dosing, self.acid_chemical, self.acid_dosing, self.bypass)

        steps = [influent] + steps + [effluent]

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
                effluent, [dosed, softened, mixed, neutralized] = self.soften(influent, chemical, d, self.acid_chemical, self.acid_dosing, self.bypass)

                chemcharts['dosed_pH'].append({'x': d, 'y': dosed.pH})
                chemcharts['softened_pH'].append({'x': d, 'y': softened.pH})

                chemcharts['softened_hh'].append({'x': d, 'y': softened.hardness})
                chemcharts['softened_hco3'].append({'x': d, 'y': softened.total('HCO3', 'mg')})
                
                chemcharts['softened_sc'].append({'x': d, 'y': softened.sc20/10})

            charts[chemical] = chemcharts
        
        resp['charts'] = charts
        
        resp['massbalance'] = {
            'influent': { 'Na': 123, 'Ca': 100, 'Mg': 20},
            'effluent': { 'Na': 120, 'Ca': 100, 'Mg': 20},
        }

        return resp




