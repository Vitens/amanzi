from dataclasses import dataclass
import numpy as np

@dataclass
class MassSolver:
    """
    A class to solve all linear equations in a process.

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

    scenario: dict

    def solve(self) -> list: 
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

        See Also
        --------
        scipy.linalg.solve : Similar function in SciPy.
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

        
        # construct matrix
        matrix = np.zeros((len(all_equations), len(results)))
        # fill matrix
        for row, eq in enumerate(all_equations):
            for conn, weight in eq:
                matrix[row, conn.id] = weight  

        # solve matrix
        mass_flows = np.linalg.solve(matrix, results)
        
        return mass_flows