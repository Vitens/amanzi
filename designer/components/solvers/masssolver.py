from dataclasses import dataclass
import numpy as np

@dataclass
class MassSolver:
    scenario: dict

    def solve(self):        
        mass_flows = self.solve_mass_balance()
        self.assign_to_connections(mass_flows)

    def solve_mass_balance(self):
        all_equations = []
        matrix = []
        results = []
        
        # collect equations from models
        for model in self.scenario.models.values():
            for eq, mass in model.equations:
                all_equations.append(eq)
                results.append(mass)
        
        # construct matrix
        matrix = np.zeros((len(all_equations), len(results)))
        
        # fill matrix
        for row, eq in enumerate(all_equations):
            for conn, weight in eq:
                matrix[row, conn.id] = weight  

        # solve matrix
        mass_flows = np.linalg.solve(matrix, results)
        
        return mass_flows


    def assign_to_connections(self, mass_flows):
        for conn, flow in zip(self.scenario.connections.values(), mass_flows):
            conn.mass_flow = flow