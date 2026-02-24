import numpy as np
from .solver import Solver

class QuantitySolver(Solver):
    """
    A class to solve all linear equations in a scenario.

    ...

    Attributes
    ----------
    scenario : dict
        config of a scenario containing all models and connections

    Methods
    -------
    solve():
        Solve the linear matrix equation.
    """

    def solve(self, until=None) -> list: 
        """
        Solve the linear matrix equation.

        Computes the "exact" solution, `x`, of the well-determined, i.e., full
        rank, linear matrix equation `ax = b`.

        Parameters
        ----------
        a : (..., M, M) array_like
            Coefficient matrix.
        b : {(..., M,), (..., M, K)}, array_like
            Ordinate or "dependent variable" values.

        Returns
        -------
        x : {(..., M,), (..., M, K)} ndarray
            Solution to the system a x = b.  Returned shape is identical to `b`.

        Raises
        ------
        LinAlgError
            If `a` is singular or not square.

        """        

        all_equations = []
        results = []
        
        # collect equations from models
        counter = 0
        for model in self.scenario.models.values():
            for eq, mass in model.equations:
                all_equations.append(eq)
                results.append(mass)
                counter += 1

        print(len(all_equations))
        print(len(results))
        
        # construct matrix
        matrix = np.zeros((len(all_equations), len(results)))
        # fill matrix
        for row, eq in enumerate(all_equations):
            for conn, weight in eq:
                print(row, conn.id, conn)
                matrix[row, conn.id] = weight  

        # solve matrix
        mass_flows = np.linalg.solve(matrix, results)
        
        # assign mass flows to connection
        for conn, flow in zip(self.scenario.connections.values(), mass_flows):
            conn.quantity.flow = flow
            # setattr(conn, "flow", flow)
            # update inflow and outflow of models
            conn.from_model.quantity.outflow[conn.type] += flow
            conn.to_model.quantity.inflow[conn.type] += flow
        
    
    def summary(self):
        """
        generate a summary of the solver
        """

        production = sum([m.quantity.outflow.get('product', 0) for _,m in self.scenario.models.items() if m.upstream_connections == {}])

        distribution = sum([m.quantity.inflow.get('product', 0) for _,m in self.scenario.models.items() if m.downstream_connections == {}])

        return {
            'total_production': production,
            'total_distribution': distribution,
            'metrics': [
                {'name': 'total_production', 'value': production, 'uom': 'Mm3/y', 'precision': 2, 'positive': True},
                {'name': 'total_distribution', 'value': distribution, 'uom': 'Mm3/y', 'precision': 2, 'positive': True},
                {'name': 'loss', 'value': production-distribution, 'uom': 'Mm3/y', 'precision': 2, 'positive': False, 'group': 'loss'},
                {'name': 'loss_percentage', 'value': (production-distribution)/production * 100, 'uom': '%', 'precision': 2, 'positive': False, 'group': 'loss'},
            ]
        }