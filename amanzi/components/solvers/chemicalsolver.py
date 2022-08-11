# from phreeqpython import PhreeqPython as pp
from dataclasses import dataclass

class ChemicalSolver:
    def __init__(self, scenario):
        self.scenario = scenario
        # self.pp = pp

    def solve(self):
        pass
