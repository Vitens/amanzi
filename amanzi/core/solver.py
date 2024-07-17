import numpy as np
from ..components.solvers import MassSolver, ChemicalSolver

class Solver:
    def __init__(self, scenario):
        self.scenario = scenario
        self.models = scenario.models
        self.connections = scenario.connections

        # init solvers
        self.mass_solver = MassSolver(scenario)
        self.chemical_solver = ChemicalSolver(scenario)

    def solve(self, until=None):

        # 1 - solve mass balance
        mass_flows = self.mass_solver.solve()
        
        # assign mass flows to connection, also ugly, revise needed
        for conn, flow in zip(self.connections.values(), mass_flows):
            setattr(conn, "flow", flow)

        # 2 - solve chemistry
        self.chemical_solver.solve(until)