import numpy as np
from ..components.solvers import MassSolver, ChemicalSolver


class Solver:
    def __init__(self, scenario):
        self.models = scenario.models
        self.connections = scenario.connections

        # init solvers
        self.mass_solver = MassSolver(scenario)
        self.chemical_solver = ChemicalSolver(scenario)
        # self.cost_solver = CostSolver
        # self.emission_solver = EmissionSolver
        # self.energy_solver = EnergySolver
        

    def solve(self):
        self.mass_solver.solve()
        # self.solve_mass_balance()

    # def solve_mass_balance(self):
    #     all_equations = []
    #     matrix = []
    #     results = []
        
    #     # collect equations from models
    #     for model in self.models.values():
    #         for eq, mass in model.equations:
    #             all_equations.append(eq)
    #             results.append(mass)
        
    #     # construct matrix
    #     matrix = np.zeros((len(all_equations), len(results)))
        
    #     # fill matrix
    #     for row, eq in enumerate(all_equations):
    #         for conn, weight in eq:
    #             matrix[row, conn.id] = weight  

    #     # solve matrix
    #     mass_flows = np.linalg.solve(matrix, results)

    #     #assign massflows to connections
    #     for conn, flow in zip(self.connections.values(), mass_flows):
    #         conn.mass_flow = flow

    #     # return solved

