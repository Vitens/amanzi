# from phreeqpython import PhreeqPython as pp
from dataclasses import dataclass

class ChemicalSolver:
    def __init__(self, scenario):
        self.scenario = scenario
        self.models = scenario.models

    def solve(self):
        
        pass

    # def solve(self):
    #     for model in self.scenario.models.values():
    #         model.solve(self.pp)
    #         print(model.type, model.name)
    #         print(model.effluent)

