import numpy as np
from scipy.optimize import fmin
from .model import Model
from .submodels.balance import Balance

class Dosing(Model, Balance):
    parametric_model = ['dosing']
    def __init__(self, config, pp) -> None:
        super().__init__(config, pp)
        config = config.get('configuration', {})
        config = config.get('parameters', {})

        self.dosing_values = {
          'ph': lambda s: s.pH,
          'o2': lambda s: 32*(s.total('O2', 'mmol') + s.total('Oxg', 'mmol')),
          'agco2': lambda s: -1 * min(0, s.ccpp()) * 44.01,
          'si': lambda s: s.si('Calcite'),
          'ccpp90': lambda s: s.ccpp90
        }

        self.chemical = config.get('chemical', 'NaOH')
        self.dosing = float(config.get('dosage', 1))
        self.mode = config.get('mode', 'constant')
        self.parameter = config.get('setpoint_parameter', 'pH')
        self.setpoint = float(config.get('setpoint', 7))
        self.calculated_dosage = None
        self.warning = False
    
    def dose(self, solution, chemical, dosing):

        dosed = solution.copy().add(chemical, dosing, 'mmol')
        return dosed

    def run_quality(self, type, total_inflow, solution):

      if self.mode == 'constant':
        return self.dose(solution, self.chemical, self.dosing)
      ## try to find right dosage for the given setpoint and parameter

      def optfun(x):
        ## bound x between 0 and 5
        x = min(5, max(0, x[0]))

        dosed = self.dose(solution, self.chemical, x)
        val = self.dosing_values[self.parameter.lower()](dosed)
        dosed.forget() # cleanup dosed function
        return abs(val - self.setpoint)
      
      opt = fmin(optfun, [0], disp=False, full_output=True)

      if(opt[1] > 0.1):
        self.calculated_dosage = 0
        self.warning = True
        return solution.copy()
      else:
        self.calculated_dosage = opt[0][0]
      
      return self.dose(solution, self.chemical, self.calculated_dosage)


    def design(self):

      ## generate dosing charts
      charts = {k: [] for k in self.dosing_values.keys()}

      for dosage in np.linspace(0,2,30):
        eff = self.dose(self.quality.influent.product, self.chemical, dosage)
        for k,v in self.dosing_values.items():
          charts[k].append({'x': dosage, 'y': v(eff)})

      return {
        'influent': {n: v(self.quality.influent.product) for n,v in self.dosing_values.items()},
        'effluent': {n: v(self.quality.effluent.product) for n,v in self.dosing_values.items()},
        'charts': charts,
        'calculated_dosage': self.calculated_dosage,
        'warning': self.warning
      }