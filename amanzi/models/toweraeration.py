from .model import Model
from .submodels.balance import Balance
from math import log
import numpy as np

class Toweraeration(Model, Balance):

    def aerate(self, solution):
        ## Aeration implementation
        return solution

    def run_model(self, type, total_inflow, solution):
        effluent = self.aerate(solution)
        return effluent


    def design(self):

        ## Charts
        ph = []
        co2 = []

        ## flooding and operating charts
        xx = np.linspace(0, 0.1, 50)
        flooding = [{'x': x, 'y': 0.1-10*x**2} for x in xx]
        operating = [{'x': x, 'y': 0.08-11*x**2} for x in xx]

        ## Efficiency loading and height charts
        xx = np.linspace(10,100, 50)

        heights = [1, 2, 3, 4, 5]

        loading_charts = []
        height_charts = []

        for h in heights:
            pass



        return {
            'influent': {
                'pH': 7,
                'O2': 0,
                'CO2': 15,
                'CH4': 5,
            },
            'effluent': {
                'pH': 7,
                'O2': 0,
                'CO2': 15,
                'CH4': 5
            },
            'model': {
                'F': 1.4,
                'liquid_load': 88,
                'flooding_factor': 61,
                'liquid_holdup': 15,
                'pressure_drop': 1.5,
            },
            'charts': {
                'flooding': flooding,
                'operating': operating,
                'working_point': [{'x': 0.04, 'y': 0.05}],
                'efficiency_loading': loading_charts,
                'efficiency_height': height_charts
            }
        }

