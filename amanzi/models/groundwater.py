import pprint
import numpy as np
from .model import Model



class Groundwater(Model):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        configuration = config.get('configuration', {})
        self.constant = float(configuration.get("production", 10))

        # modify production for minorloss
        if self.minorloss_percentage < 1:
            self.constant *= self.minorloss_percentage
        else:
            self.constant -= self.minorloss


        c = configuration.get('solution', {}) 

        # pprint.pprint(c)

        oxg = c.get('Zuurstof', 0) if c.get('Zuurstof', 0) > 0 else 0.00001
        h2s = 'Sg' if c.get('Zuurstof', 0) == 0 else 'S(-2)'
        fe = '[Fe+2]' if c.get('Zuurstof', 0) == 0 else 'Fe'
        mn = '[Mn+2]' if c.get('Zuurstof', 0) == 0 else 'Mn'
        nh4 = '[N-3]' if c.get('Zuurstof', 0) == 0 else 'N(-3)'
        no2 = '[N+3]' if c.get('Zuurstof', 0) == 0 else 'N(3)'

        h2s_value = max(c.get('Waterstofsulfide', 0), 0.0000001)

        # create solution
        # print("SOLUTION")
        # print ({
        #     'pH': c.get('pH', 7),
        #     'temp': c.get('temp', 10),
        #     'units': 'mg/l',
        #     'pe': 4, # phreeqc default
        #     'redox': 'O(-2)/O(0)',
        #     'O(0)': oxg,
        #     'Oxg': 0.0000001, # prevent phreeqc from crashing
        #     'Ntg': c.get('Stikstof', 0),
        #     'Mtg': c.get('Methaan', 0),
        #     h2s: '{} as H2S'.format(h2s_value),
        #     fe: '{} as Fe'.format(c.get('IJzer', 0)),
        #     mn: '{} as Mn'.format(c.get('Mangaan', 0)),
        #     nh4: '{} as NH4'.format(c.get('Ammonium', 0)),
        #     'Ca': c.get('Calcium', 0),
        #     'Mg': c.get('Magnesium', 0),
        #     'Na': c.get('Natrium', 0),
        #     'K': c.get('Kalium', 0),
        #     'Alkalinity': '{} as HCO3'.format(c.get('Bicarbonaat', 0)),
        #     'Cl': c.get('Chloride', 0),
        #     'N(5)': '{} as NO3'.format(c.get('Nitraat', 0)),
        #     no2: '{} as NO2'.format(c.get('Nitriet', 0)),
        #     'S(6)': '{} as SO4'.format(c.get('Sulfaat', 0)),
        #     'P': '{} as PO4'.format(c.get('Fosfaat', 0)),
        # })

        self.solution = self.pp.add_solution({
            'pH': c.get('pH', 7),
            'temp': c.get('Temperatuur', 10),
            'units': 'mg/l',
            'pe': 4, # phreeqc default
            'redox': 'O(-2)/O(0)',
            'O(0)': oxg,
            'Oxg': 0.0000001, # prevent phreeqc from crashing
            'Ntg': c.get('Stikstof', 0),
            'Mtg': c.get('Methaan', 0),
            h2s: '{} as H2S'.format(h2s_value),
            fe: '{} as Fe'.format(c.get('IJzer', 0)),
            mn: '{} as Mn'.format(c.get('Mangaan', 0)),
            nh4: '{} as NH4'.format(c.get('Ammonium', 0)),
            'Ca': c.get('Calcium', 0),
            'Mg': c.get('Magnesium', 0),
            'Na': c.get('Natrium', 0),
            'K': c.get('Kalium', 0),
            'Alkalinity': '{} as HCO3'.format(c.get('Bicarbonaat', 0)),
            'Cl': c.get('Chloride', 0),
            'N(5)': '{} as NO3'.format(c.get('Nitraat', 0)),
            no2: '{} as NO2'.format(c.get('Nitriet', 0)),
            'S(6)': '{} as SO4'.format(c.get('Sulfaat', 0)),
            'P': '{} as PO4'.format(c.get('Fosfaat', 0)),
        })
        ## equalize solution
        self.solution.equalize('Calcite', 1000, 0)

        self.emitter = True

    @property
    def equations(self):
        return [ [ [self.downstream_connections['product'][0].eq(1)], self.constant] ]

    @property
    def emitter_solutions(self):
        return {'product': self.solution}

    @property
    def flow(self):
        """override model-flow with constant"""
        return self.constant


    def design(self):
        # return dict with design parameters
        cat,an = self.solution.calculate_total_charge()

        oxygen_consumption_ions = self.solution.total('[Fe+2]') * 0.25 + self.solution.total('[Mn+2]') * 0.5 + self.solution.total('[N-3]') * 2
        oxygen_consumption_gas = self.solution.total('Mtg') * 2 + self.solution.total('[S-2]') * 2
        oxygen_consumption = oxygen_consumption_ions + oxygen_consumption_gas

        si = self.solution.si('Calcite') if self.solution.si('Calcite') != -999 else 0

        resp = {
            'sc20': self.solution.sc20 / 10,
            'm': self.solution.m,
            'p': self.solution.p,
            'pe': self.solution.pe,
            'h_activity': -np.log10(self.solution.activity('H+', 'mol')),
            'osmotic_pressure': self.solution.osmotic_pressure,
            'anions': an,
            'cations': cat,
            'charge_balance': self.solution.charge_balance,
            'balance_error': self.solution.balance_error,
            'CO2': self.solution.total('CO2', 'mg'),
            'HCO3': self.solution.total('HCO3', 'mg'),
            'CO3': self.solution.total('CO3', 'mg'),
            'hardness': self.solution.hardness,
            'SI': si,
            'CCPP': self.solution.ccpp(),
            'CCPP90': self.solution.ccpp90,
            'oxygen_consumption': oxygen_consumption * 32,
            'oxygen_consumption_ions': oxygen_consumption_ions * 32,
            'oxygen_consumption_gas': oxygen_consumption_gas * 32,
        }

        return resp