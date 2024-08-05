import numpy as np
from ..components.solvers import MassSolver, ChemicalSolver, HydraulicSolver

class Solver:
    def __init__(self, scenario):
        self.scenario = scenario
        self.models = scenario.models
        self.connections = scenario.connections

        # init solvers
        self.mass_solver = MassSolver(scenario)
        self.chemical_solver = ChemicalSolver(scenario)
        self.hydraulic_solver = HydraulicSolver(scenario)

    def solve(self, until=None):

        # 1 - solve mass balance
        mass_flows = self.mass_solver.solve()
        
        # assign mass flows to connection, also ugly, revise needed
        for conn, flow in zip(self.connections.values(), mass_flows):
            setattr(conn, "flow", flow)

        # 2 - solve chemistry
        self.chemical_solver.solve(until)

        # # 3 - Run design calculations
        # for m in self.models.values():
        #     m.run_design()

        # # 4 - Run hydraulic calculations
        self.hydraulic_solver.solve()
        
