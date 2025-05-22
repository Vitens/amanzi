import numpy as np
import logging
from .model import Model

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Groundwater(Model):
    parametric_model = ['base', 'groundwater', 'quality']

    def __init__(self, config, pp):
        super().__init__(config, pp)

        if not pp:
            # if no phreeqpython instance is passed, we can't do anything
            # this happens when the model is instantiated for input parameter generation
            return

        configuration = config.get('configuration', {})
        self.constant = self.parameters['yearly_production']

        # modify production for minorloss
        if self.minorloss_percentage < 1:
            self.constant *= self.minorloss_percentage
        else:
            self.constant -= self.minorloss

        

        # pprint.pprint(c)
        c = self.parameters

        oxg = c.get('oxygen', 0) if c.get('oxygen', 0) > 0 else 0.00001
        h2s = 'Sg' if c.get('oxygen', 0) == 0 else 'S(-2)'
        fe = '[Fe+2]' if c.get('oxygen', 0) == 0 else 'Fe'
        # fe = 'Fe'
        mn = '[Mn+2]' if c.get('oxygen', 0) == 0 else 'Mn'
        # mn = 'Mn'
        nh4 = '[N-3]' if c.get('oxygen', 0) == 0 else 'N(-3)'
        no2 = '[N+3]' if c.get('oxygen', 0) == 0 else 'N(3)'

        h2s_value = max(c.get('hydrogen-sulfide', 0), 0.0000001)


        self.solution = self.pp.add_solution({
            'pH': c.get('pH', 7),
            'temp': c.get('temperature', 10),
            'units': 'mg/l',
            'pe': 4, # phreeqc default
            'redox': 'O(-2)/O(0)',
            'O(0)': oxg,
            'Oxg': 0.0000001, # prevent phreeqc from crashing
            'Ntg': c.get('nitrogen', 0),
            'Mtg': c.get('methane', 0),
            h2s: '{} as H2S'.format(h2s_value),
            fe: '{} as Fe'.format(c.get('iron', 0)),
            mn: '{} as Mn'.format(c.get('manganese', 0)),
            nh4: '{} as NH4'.format(c.get('ammonium', 0)),
            'Ca': c.get('calcium', 0),
            'Mg': c.get('magnesium', 0),
            'Na': c.get('sodium', 0),
            'K': c.get('potassium', 0),
            'Alkalinity': '{} as HCO3'.format(c.get('bicarbonate', 0)),
            'Cl': c.get('chloride', 0),
            'N(5)': '{} as NO3'.format(c.get('nitrate', 0)),
            no2: '{} as NO2'.format(c.get('nitrite', 0)),
            'S(6)': '{} as SO4'.format(c.get('sulfate', 0)),
            'P': '{} as PO4'.format(c.get('phosphate', 0)),
            'Si': '{} as SiO2'.format(c.get('silica', 0)),
            'B': c.get('boron', 0),
            'Sr': c.get('strontium', 0),
            'Ba': c.get('barium', 0),
            'F': c.get('fluoride', 0),
        },
        # extraneous properties (i.e. untracked by PHREEQC)
        {'Color': c.get('color', 0),
         'TOC': c.get('total-organic-carbon', 0),
            'PFAS':{}, 'VOC':{}, 'Other':{}}
           )

        c = configuration.get('solution', {}) 

        for key,value in c.get('PFAS', {}).items():
            if key != "" and key != '':
                self.solution.extraneous['PFAS'].update({key: value})
            if value == 0:
                del self.solution.extraneous['PFAS'][key]
        # implement a catch for error when a custom PFAS is added but not named. 

        for key,value in c.get('VOC', {}).items():
            if key != "":
                self.solution.extraneous['VOC'].update({key: value})
            if value == 0:
                del self.solution.extraneous['VOC'][key]
        
        for key,value in c.get('Other', {}).items():
            if key != "":
                self.solution.extraneous['Other'].update({key: value})
            
        #     if value == 0:
        #         del self.solution.extraneous['Other'][key]


        ## equalize solution to ensure all mass balances are solved
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
    
    def run_quality(self, stream_type, total_inflow, solution):
        return self.solution


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
            'tds': self.solution.tds,
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