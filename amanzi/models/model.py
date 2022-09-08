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
            total_inflow = sum([c.flow for c in self.upstream_connections.get(type,[]) if c.solution is not None])
            mixture = {c.solution : c.flow/total_inflow for c in self.upstream_connections.get(type,[]) if c.solution is not None}
            solution = self.pp.mix_solutions(mixture)

            solution = self.run_model(type, total_inflow, solution)
        
        self.solution = solution

        return solution
    
    def run_model(self, type, total_inflow, solution):
        return solution

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
        return 0