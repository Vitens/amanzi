import logging
import math
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
    
    def run_trace(self, model, stream_type: str, idx=0) -> None:
        """
        Runs the quality trace for a given model and stream type.

        Args:
            model: The model to run the trace on.
            stream_type (str): The type of stream to consider (e.g., 'product', 'flush', 'waste').
        """
        if not self._is_model_ready(model, stream_type):
            return

        # set model index
        model.index = idx if not model.index else model.index

        logging.debug(f'Running trace for model {model.uid} with stream type {stream_type}')
        
        total_inflow = model.quantity.inflow[stream_type]
        influent = self._calculate_influent(model, stream_type, total_inflow)

        solution = model.run_quality(stream_type, total_inflow, influent)
        model.quality['effluent'][stream_type] = solution

        if self.stop_at_model and model.uid == self.stop_at_model:
            logging.info(f'Interrupted at model {model.uid}')
            self.interrupted = True
            return
        
        self._propagate_solution(model, stream_type, solution, idx)

    def solve(self, until: Optional[str] = None) -> None:
        """
        Solves the scenario until the specified model.

        Args:
            until (Optional[str]): The model ID at which to stop the solver.
        """
        self.stop_at_model = until
        self.interrupted = False

        for connection in self.scenario.connections.values():
            connection.quality.solution = False
            
        order = ['product', 'flush', 'waste']
        idx_start = {'product': 0, 'flush': 100, 'waste': 200}
        
        for i in range(self.max_iterations):
            for stream_type in order:
                idx = idx_start[stream_type]
                for model in self.emitters.get(stream_type, []):
                    # set model index if not set
                    model.index = idx if not model.index else model.index
                    # set model effluent quality
                    model.quality['effluent'][stream_type] = model.emitter_solutions[stream_type].copy()
                    if stream_type == 'waste':
                        print(model, model.quality['effluent']['waste'])
    
                    if until and model.uid == until:
                        logging.info(f'Interrupted at model {model.uid}')
                        self.interrupted = True
                        return


                    self._propagate_solution(model, stream_type, model.emitter_solutions[stream_type], idx)
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
        qualities = []

        for _,m in self.scenario.models.items():
            if m.type == 'output':
                effluent = m.quality.influent.product.summary
                plant_effluent = m.quality.influent.product.summary
                qualities.append([m.uid, m.name, m.index, effluent])
            else:
                if m.quality.effluent.product:
                    effluent = m.quality.effluent.product.summary
                    qualities.append([m.uid, m.name, m.index, effluent])
        
        order = sorted(qualities, key=lambda x: x[2])
        models = [x[0] for x in order]
        names = [x[1] for x in order]
        # sort qualities based on order
        qualities = [x[3] for x in order]

        return {
            'order': models,
            'names': names,
            'models': qualities,
            'effluent': plant_effluent,
            'metrics': self.grade_quality(plant_effluent)
        }

    def grade_quality(self, quality):
        """
        Grades the quality based on the given quality metrics.

        Args:
            quality (Dict[str, Union[str, float]]): A dictionary of quality metrics.
        """
        db = self.scenario.database

        for component in quality:
            # get threshold and limits from database
            nm = component['name'].lower()
            ll = db.get(nm+'_lower_limit', -math.inf)
            lt = db.get(nm+'_lower_threshold', -math.inf)
            ut = db.get(nm+'_upper_threshold', math.inf)
            ul = db.get(nm+'_upper_limit', math.inf)
            
            value = component['value']

            # set color based on thresholds and limits
            if value < ll or value > ul:
                component['color'] = 'red'
            elif value < lt or value > ut:
                component['color'] = 'orange'
            else:
                component['color'] = 'green'
        
        return quality
    

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
            if not connection.quality.solution:
                continue

            for element, mass_fraction in connection.quality.solution.elements.items():
                flow_direction = 1 if connection.from_model == model else -1
                element_name = element.split('(')[0]
                balance[element_name] = balance.get(element_name, 0) + flow_direction * mass_fraction * connection.quantity.flow * 1e3

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
        return all(connection.quality.solution is not False for connection in model.upstream_connections.get(stream_type, []))

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
            mixture = {connection.quality.solution: connection.quantity.flow / total_inflow for connection in model.upstream_connections.get(stream_type, [])}
            influent = model.pp.mix_solutions(mixture)
            model.quality['influent'][stream_type] = influent.copy()
            return influent
        return None

    def _propagate_solution(self, model, stream_type: str, solution: Dict, idx: int) -> None:
        """
        Propagates the solution to downstream connections.

        Args:
            model: The model to propagate the solution from.
            stream_type (str): The type of stream to consider.
            solution (Dict): The solution to propagate.
        """
        for connection in model.downstream_connections.get(stream_type, []):
            connection.quality.solution = solution
            if connection.quantity.flow > 0:
                self.run_trace(connection.to_model, stream_type, idx+1)

    def _has_convergence_failed(self) -> bool:
        """
        Checks if the convergence has failed based on the precision.

        Returns:
            bool: True if convergence has failed, False otherwise.
        """
        return any(abs(mass_balance) > self.precision for mass_balance in self.error.values())
