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
        self.connections = {}
        self.costfuncs = None
        self.init_categories()
        self.connections = {'top': [], 'bottom': [], 'left': [], 'right': []}

    def init_categories(self) -> None:
        """Uses the configuration categorial settings
        to initialize all categories via their respective instances"""

        self.categories = {}
        for cat, settings in self.config['categories'].items():
            cat_instance = getattr(CATEGORY_MODULES, cat.capitalize())
            self.categories[cat] = cat_instance(self.process, settings)

    def solve(self):
        pass
    # def solve(self, influent = None):
    #     influent = pp.add_solution({})
    #     self.effluent = influent

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
    def inflow(self):
        return sum([conn.flow for conn in self.upstream_connections])

    @property
    def outflow(self):
        """all outgoing flows, including waste flows"""
        return sum([conn.flow for conn in self.downstream_connections])

    @property
    def equations(self):
        return []
