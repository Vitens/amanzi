from ..components import Connection
import sys
import pandas as pd
from .. import categories

CATEGORY_MODULES = sys.modules['amanzi.categories']

class Model:
    def __init__(self, config):
        self.config = config
        self.uid = config['uid']
        self.type = config["type"]
        self.name = self.type.capitalize()
        self.process = self.type
        self.emitter = False
        self.connections = {'top': [], 'bottom': [], 'left': [], 'right': []}
        self.costfuncs = None
        self.init_categories()

        self.previous_inflow = None
        self.previous_mixture = None
        # self.iteration = 0

    def init_categories(self) -> None:
        """Uses the configuration categorial settings
        to initialize all categories via their respective instances"""

        self.categories = {}
        
        # for cat, settings in self.config['categories'].items():
        for cat, settings in self.config.setdefault('categories', {}).items():
            cat_instance = getattr(CATEGORY_MODULES, cat.capitalize())
            self.categories[cat] = cat_instance(self.process, settings)

    def mix_upstream_connections(self):
        mixture = {}
        for conn in self.upstream_connections:
            normalized_flow = conn.mass_flow / self.flow
            if conn.solution.number in mixture.keys():
                mixture[conn.solution.number] += normalized_flow
            else:
                mixture[conn.solution.number] = normalized_flow

        # print("mixture")
        # print(mixture)

        # cache mixture to enhance performance during iterations
        # (e.g. during flushing the system during start-up)
        if mixture != self.previous_mixture:
            influent = self.pp.mix_solutions(mixture)
            self.previous_inflow = influent
            self.previous_mixture = mixture
        else:
            influent = self.previous_inflow    

        return influent

        

    def run(self):
        if self.emitter:
            for conn in self.downstream_connections:
                conn.solution = self.emitter_solution
            return

        # prepare  the model inputs
        if not self.ready:
            raise ValueError("Model run before inputs ready")

        influent = self.mix_upstream_connections()

        effluent = self.run_model(influent)

        for conn in self.downstream_connections:
            # print(f"{conn.id} - {conn.type} - {conn.blocked}")            
            if not conn.blocked:
                conn.solution = effluent

    def run_model(self, influent):
        # print(f"Running model {self.name}")
        effluent = influent.copy()
        return effluent

    def solve(self):
        pass

    @property
    def upstream_connections(self):
        upstream = []
        upstream.extend(self.connections.get("left", []))
        upstream.extend(self.connections.get("top", []))
        return upstream
    
    @property
    def downstream_connections(self):
        downstream = []
        downstream.extend(self.connections.get("right", []))
        downstream.extend(self.connections.get("bottom", []))
        return downstream

    @property
    def flow(self):
        return sum([conn.mass_flow for conn in self.upstream_connections])

    @property
    def ready(self):
        """ check if the model is ready for calculation """
        # filtered_connections = []
        # for conn in self.upstream_connections:
        #     if not conn.blocked:
        #         filtered_connections.append(conn.solution)

        relevant_connections = [conn for conn in self.upstream_connections if not conn.blocked]
        return all(conn.solution is not False for conn in relevant_connections)




        return all(conn.solution is not False for conn in self.upstream_connections)