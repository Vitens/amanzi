from ..components import Connection
import sys
import pandas as pd
from .. import categories

CATEGORY_MODULES = sys.modules['amanzi.categories']

class Model:
    def __init__(self, config, pp):
        self.config = config
        self.uid = config['uid']
        self.type = config["type"]
        self.name = self.type.capitalize()
        self.process = self.type
        self.emitter = False
        self.connections = []
        self.costfuncs = None
        self.init_categories()

        self.solution = None
        self.inflows = {}

        self.pp = pp
        # self.iteration = 0

    def init_categories(self) -> None:
        """Uses the configuration categorial settings
        to initialize all categories via their respective instances"""

        self.categories = {}
        
        # for cat, settings in self.config['categories'].items():
        for cat, settings in self.config.setdefault('categories', {}).items():
            cat_instance = getattr(CATEGORY_MODULES, cat.capitalize())
            self.categories[cat] = cat_instance(self.process, settings)
    
    def is_ready(self, type):
        # a model is ready when all it's upstream connections have a solution assigned
        return all([c.solution is not False for c in self.upstream_connections.get(type, [])])
    
    def run(self, type):

        if type in self.emitter_solutions:
            solution = self.emitter_solutions[type]

        else:
            # run model for type
            # get influent,
            try:
                total_inflow = sum([c.flow for c in self.upstream_connections.get(type,[]) if c.solution is not None])
                self.inflows[type] = total_inflow
                mixture = {c.solution : c.flow/total_inflow for c in self.upstream_connections.get(type,[]) if c.solution is not None}
                solution = self.pp.mix_solutions(mixture)

                if type == 'product':
                    self.influent = solution.copy()

                solution = self.run_model(type, total_inflow, solution)
            except:
                # print("IN EXCEPTION")
                # for c in self.upstream_connections.get(type, []):
                #     print("c.flow")
                #     print(c.name, c.flow)
                # print(self.upstream_connections)
                # print(mixture)
                raise Exception('Model {} failed to run for type {}'.format(self.uid, type))
        
        self.solution = solution

        return solution
    
    def run_model(self, type, total_inflow, solution):
        return solution

    # calculate minor loss, either as percentage of inflow or as a fixed value
    @property
    def minorloss(self):
        if self.config.get('configuration', {}).get('minorloss_method', 'percentage') != 'percentage':
            return float(self.config.get('configuration', {}).get('minorloss', 0))
        return 0
    
    @property
    def minorloss_percentage(self):
        if self.config.get('configuration', {}).get('minorloss_method', 'percentage') == 'percentage':
            return 1-float(self.config.get('configuration', {}).get('minorloss', 0))
        return 1

        
        


    @property
    def emitter_solutions(self):
        return {}

    @property
    def upstream_connections(self):
        upstream = {}
        for c in self.connections:
            if(c.to_model == self):
                upstream.setdefault(c.type, []).append(c)
        return upstream
    
    @property
    def downstream_connections(self):
        downstream = {}
        for c in self.connections:
            if(c.from_model == self):
                downstream.setdefault(c.type, []).append(c)
        return downstream
    
    @property
    def anchors_connections(self):
        anchors = {}
        for c in self.connections:
            anchor = c.from_anchor if c.from_model == self else c.to_anchor
            anchors.setdefault(anchor, []).append(c)

        return anchors


    @property
    def mass(self):
        """
        Calculates the mass balance of the model.

        Returns:
            A dictionary where the keys are element symbols (e.g. 'C', 'H', 'O')
            and the values are the total mass balance for each element in the model
            in millimoles (mmol).
        """
        balance = {}

        # Iterate over all connections in the model
        for connection in self.connections:
            if not connection.solution:
                continue

            # Iterate over all elements and their mass fractions in the solution
            for element, mass_fraction in connection.solution.elements.items():
                # Determine the direction of the flow for the current connection
                flow_direction = 1 if connection.from_model == self else -1

                # Extract the element name by ignoring the parenthesis part
                # enables correct handling of redox states
                element_name = element.split('(')[0]

                # Update the balance for the current element
                balance[element_name] = balance.get(element_name, 0) + flow_direction * mass_fraction * connection.flow * 1e3

        # Round small values to zero
        for element, mass_balance in balance.items():
            if abs(mass_balance) < 0.00001:
                balance[element] = 0

        return balance