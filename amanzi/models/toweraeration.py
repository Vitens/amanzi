from .model import Model
from .submodels.balance import Balance
from math import log
import numpy as np

from .tower.onda import run_onda
from .tower.engelstichlmair import engelstichlmair


class Toweraeration(Model, Balance):

    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)

        self.configuration = config.get('configuration', {})

        self.rq = float(self.configuration.get('RQ', 50))
        self.diameter = self.configuration.get('diameter', 2)
        self.packing_type = self.configuration.get('packing_type', 'raflux50')
        self.packing_height = self.configuration.get('packing_height', 2.5)
        self.capacity = self.configuration.get('nominal_capacity', 100)

        print('RQ is', self.rq)


    def calculate_efficiency(method='Onda', flow=150, packing_height=5, packing='RAFLUX50', RQ=50, component='CO2', c_in=10, c_gas=0):
        ## run onda model
        efficiency = run_onda(flow, packing_height, packing, RQ, component, c_in, c_gas)

        return efficiency




    def run_model(self, type, total_inflow, solution):
        ## gets called by solver
        co2_removal = self.calculate_efficiency(component='CO2', c_in=solution.total('CO2', 'mmol'), c_gas=0, flow=self.capacity, packing_height=self.packing_height, packing=self.packing_type, RQ=self.rq)
        ch4_removal = self.calculate_efficiency(component='CH4', c_in=solution.total('Mtg', 'mmol'), c_gas=0, flow=self.capacity, packing_height=self.packing_height, packing=self.packing_type, RQ=self.rq)

        solution.remove_fraction('CO2', co2_removal)
        solution.remove_fraction('Mtg', ch4_removal)

        return solution



    def design(self):
        ## gets called by design GUI

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
                'pH': self.influent.pH,
                'O2': 0,
                'CO2': self.influent.total('CO2', 'mg'),
                'CH4': self.influent.total('Mtg') * 16,
            },
            'effluent': {
                'pH': self.solution.pH,
                'O2': 0,
                'CO2': self.solution.total('CO2', 'mg'),
                'CH4': self.solution.total('Mtg') * 16 
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

