import numpy as np
from scipy.optimize import fmin
from .model import Model
from .submodels.balance import Balance

class Dosing(Model, Balance):
    def __init__(self, config, pp) -> None:
        super().__init__(config, pp)
        config = config.get('configuration', {})

        self.values = {
          'pH': lambda s: s.pH,
          'O2': lambda s: 32*(s.total('O2', 'mmol') + s.total('Oxg', 'mmol')),
          'AgCO2': lambda s: -1 * min(0, s.ccpp()) * 44.01,
          'si': lambda s: s.si('Calcite'),
          'ccpp90': lambda s: s.ccpp90
        }

        self.chemical = config.get('chemical', 'NaOH')
        self.dosing = float(config.get('dosage', 1))
        self.mode = config.get('mode', 'constant')
        self.parameter = config.get('parameter', 'pH')
        self.setpoint = float(config.get('setpoint', 7))
        self.calculated_dosage = None
    
    def dose(self, solution, chemical, dosing):

        dosed = solution.copy().add(chemical, dosing, 'mmol')
        return dosed

    def run_model(self, type, total_inflow, solution):

      if self.mode == 'constant':
        return self.dose(solution, self.chemical, self.dosing)
      ## try to find right dosage for the given setpoint and parameter

      def optfun(x):
        ## bound x between 0 and 5
        x = min(5, max(0, x[0]))

        dosed = self.dose(solution, self.chemical, x)
        val = self.values[self.parameter](dosed)
        dosed.forget() # cleanup dosed function
        return abs(val - self.setpoint)
      
      opt = fmin(optfun, [0], disp=False)
      self.calculated_dosage = opt[0]

      return self.dose(solution, self.chemical, opt[0])


    def design(self):

      ## generate dosing charts
      charts = {k: [] for k in self.values.keys()}

      for dosage in np.linspace(0,2,30):
        eff = self.dose(self.influent, self.chemical, dosage)
        for k,v in self.values.items():
          charts[k].append({'x': dosage, 'y': v(eff)})

      return {
        'influent': {n: v(self.influent) for n,v in self.values.items()},
        'effluent': {n: v(self.solution) for n,v in self.values.items()},
        'charts': charts,
        'calculated_dosage': self.calculated_dosage
      }
      


