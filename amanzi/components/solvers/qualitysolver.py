import logging
from typing import Dict, List, Optional, Union
from .solver import Solver

class QualitySolver(Solver):
    """
    A solver class for running quality simulations in a given scenario.

    Attributes:
        max_iterations (int): The maximum number of iterations to run the solver.
        precision (float): The precision required for the solution to be considered converged.
        stop_at_model (Optional[str]): The model ID at which to stop the solver.
        interrupted (bool): A flag indicating whether the solver was interrupted.
    """

    def __init__(self, scenario):
        """
        Initializes the QualitySolver with a scenario.

        Args:
            scenario: The scenario to be solved.
        """
        super().__init__(scenario)
        self.max_iterations = 100
        self.precision = 0.0001
        self.stop_at_model = None
        self.interrupted = False
    
    def run_trace(self, model, stream_type: str) -> None:
        """
        Runs the quality trace for a given model and stream type.

        Args:
            model: The model to run the trace on.
            stream_type (str): The type of stream to consider (e.g., 'product', 'flush', 'waste').
        """
        if not self._is_model_ready(model, stream_type):
            return

        logging.debug(f'Running trace for model {model.uid} with stream type {stream_type}')
        
        total_inflow = model.quantity.inflow[stream_type]
        influent = self._calculate_influent(model, stream_type, total_inflow)

        solution = model.run_quality(stream_type, total_inflow, influent)
        model.quality['effluent'][stream_type] = solution

        if self.stop_at_model and model.uid == self.stop_at_model:
            logging.info(f'Interrupted at model {model.uid}')
            self.interrupted = True
            return
        
        self._propagate_solution(model, stream_type, solution)

    def solve(self, until: Optional[str] = None) -> None:
        """
        Solves the scenario until the specified model.

        Args:
            until (Optional[str]): The model ID at which to stop the solver.
        """
        self.stop_at_model = until
        self.interrupted = False

        for connection in self.scenario.connections.values():
            connection.solution = False
            
        order = ['product', 'flush', 'waste']
        
        for i in range(self.max_iterations):
            for stream_type in order:
                for model in self.emitters.get(stream_type, []):
                    self.run_trace(model, stream_type)
                if self.interrupted:
                    return
                    
            if not self._has_convergence_failed():
                logging.info(f'Quality converged in {i} iterations')
                return

        raise Exception(f'Model did not converge in {self.max_iterations} iterations. Mass balance is {self.error}')
    
    def summary(self) -> Dict:
        """
        Provides a summary of the solution.

        Returns:
            Dict: A dictionary summarizing the solution.
        """
        for _,m in self.scenario.models.items():
            if m.type == 'output':
                return m.quality.influent.product.summary

    @property
    def error(self) -> Dict[str, float]:
        """
        Calculates the error in the mass balance for the scenario.

        Returns:
            Dict[str, float]: A dictionary where the keys are element symbols and the values are the mass balance errors for each element.
        """
        balance = {}
        for model in self.scenario.models.values():
            for element, mass_balance in self.mass(model).items():
                balance[element] = balance.get(element, 0) + mass_balance
        return balance
        
    @property
    def emitters(self) -> Dict[str, List]:
        """
        Identifies all emitters in the scenario.

        Returns:
            Dict[str, List]: A dictionary where the keys are stream types and the values are lists of models that emit that stream type.
        """
        emitters = {}
        for model in self.scenario.models.values():
            for etype in model.emitter_solutions.keys():
                emitters.setdefault(etype, []).append(model)
        return emitters
    
    @staticmethod
    def mass(model) -> Dict[str, float]:
        """
        Calculates the mass balance of the model.

        Args:
            model: The model to calculate the mass balance for.

        Returns:
            Dict[str, float]: A dictionary where the keys are element symbols (e.g., 'C', 'H', 'O')
                              and the values are the total mass balance for each element in the model
                              in millimoles (mmol).
        """
        balance = {}

        for connection in model.connections:
            if not connection.solution:
                continue

            for element, mass_fraction in connection.solution.elements.items():
                flow_direction = 1 if connection.from_model == model else -1
                element_name = element.split('(')[0]
                balance[element_name] = balance.get(element_name, 0) + flow_direction * mass_fraction * connection.flow * 1e3

        for element in balance.keys():
            if abs(balance[element]) < 0.00001:
                balance[element] = 0

        return balance

    def _is_model_ready(self, model, stream_type: str) -> bool:
        """
        Checks if all upstream connections have a solution set.

        Args:
            model: The model to check.
            stream_type (str): The type of stream to consider.

        Returns:
            bool: True if the model is ready, False otherwise.
        """
        return all(connection.solution is not False for connection in model.upstream_connections.get(stream_type, []))

    def _calculate_influent(self, model, stream_type: str, total_inflow: float) -> Optional[Dict]:
        """
        Calculates the influent solution mixture for the model.

        Args:
            model: The model to calculate the influent for.
            stream_type (str): The type of stream to consider.
            total_inflow (float): The total inflow for the stream type.

        Returns:
            Optional[Dict]: The calculated influent solution mixture or None if no influent.
        """
        if total_inflow > 0:
            mixture = {connection.solution: connection.flow / total_inflow for connection in model.upstream_connections.get(stream_type, [])}
            influent = model.pp.mix_solutions(mixture)
            model.quality['influent'][stream_type] = influent.copy()
            return influent
        return None

    def _propagate_solution(self, model, stream_type: str, solution: Dict) -> None:
        """
        Propagates the solution to downstream connections.

        Args:
            model: The model to propagate the solution from.
            stream_type (str): The type of stream to consider.
            solution (Dict): The solution to propagate.
        """
        for connection in model.downstream_connections.get(stream_type, []):
            connection.solution = solution
            if connection.flow > 0:
                self.run_trace(connection.to_model, stream_type)

    def _has_convergence_failed(self) -> bool:
        """
        Checks if the convergence has failed based on the precision.

        Returns:
            bool: True if convergence has failed, False otherwise.
        """
        return any(abs(mass_balance) > self.precision for mass_balance in self.error.values())
