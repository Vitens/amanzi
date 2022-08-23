import numpy as np
from ..components.solvers import MassSolver, ChemicalSolver, CategorySolver


class Solver:
    def __init__(self, scenario):
        self.models = scenario.models
        self.connections = scenario.connections

        # init solvers
        self.mass_solver = MassSolver(scenario)
        self.chemical_solver = ChemicalSolver(scenario)
        self.category_solver = CategorySolver(scenario)        
        # self.cost_solver = CostSolver
        # self.emission_solver = EmissionSolver
        # self.energy_solver = EnergySolver

    def solve(self):

        # 1 - solve mass balance
        mass_flows = self.mass_solver.solve()
        
        # assign mass flows to connection
        for conn, flow in zip(self.connections.values(), mass_flows):
            setattr(conn, "flow", flow)

        
        # 2 - solve chemistry
        self.chemical_solver.solve()

        # 3 - solve cost funcs
        self.category_solver.solve()

    

