import numpy as np


class Solver:
    def __init__(self, scenario):
        # self.scenario = scenario
        self.models = scenario.models
        self.connections = scenario.connections
        
        self.solve_mass_balance()

    def solve_mass_balance(self):
        all_equations = []
        matrix = []
        results = []
        
        # collect equations 
        for model in self.models.values():
            for eq, mass in model.equations:
                all_equations.append(eq)
                results.append(mass)
        
        # construct matrix
        matrix = np.zeros((len(all_equations), len(results)))
        
        # fill matrix
        for row, eq in enumerate(all_equations):
            for conn, weight in eq:
                matrix[row, conn.num] = weight  

        # solve matrix
        solved = np.linalg.solve(matrix, results)

        #assign massflows to connections
        for conn, result in zip(self.connections.values(), solved):
            conn.mass_flow = result

        # return solved

