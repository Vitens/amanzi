import numpy as np
from ..components.solvers import MassSolver, ChemicalSolver, CategorySolver

class Solver:
    def __init__(self, scenario):
        self.scenario = scenario
        self.models = scenario.models
        self.connections = scenario.connections

        # init solvers
        self.mass_solver = MassSolver(scenario)
        self.chemical_solver = ChemicalSolver(scenario)
        self.category_solver = CategorySolver(scenario)

    def solve(self):

        # 1 - solve mass balance
        mass_flows = self.mass_solver.solve()
        
        # assign mass flows to connection
        for conn, flow in zip(self.connections.values(), mass_flows):
            setattr(conn, "mass_flow", flow)

        print("NU PAS CHEMISCH BEREKENEN")
        print("""CHANGES: ONLY BLOCK A WASTE STREAM IF ITS DEPENDENT ON A FLUSH STEP (LIKE A SANDFILTER).
                ELSE THE WASTE STREAM KAN ALREADY BECALCULATED IN ITERATION STEP=0""")
        
        # 2 - solve chemistry
        self.chemical_solver.solve()

        # 3 - solve cost funcs
        # self.scenario.costfuncs = self.category_solver.solve()
        self.category_solver.solve()

    

