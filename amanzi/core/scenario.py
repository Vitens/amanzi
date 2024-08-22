import phreeqpython
from collections import OrderedDict
from ..components.solvers import QuantitySolver, QualitySolver, HydraulicSolver, EnergySolver
from .. import models
from ..components import Connection, solution

import sys

MODULES = sys.modules['amanzi.models']

class Scenario:
    def __init__(self, project, config):
        self.config = config
        self.pp = phreeqpython.PhreeqPython()
        # loading
        self.models = self.load_models()  
        self.connections = self.load_connections()

        # list of solvers
        self.solvers = OrderedDict({
            'quantity': QuantitySolver(self),
            'quality': QualitySolver(self),
            'hydraulics': HydraulicSolver(self),
            'energy': EnergySolver(self)
        })

    def run_scenario(self, until=None):
        # run all solvers in order
        for _,solver in self.solvers.items():
            solver.solve(until)

    def load_models(self):
        models = {}
        for model in self.config['models']:
            modeltype = model['type'].capitalize()
            model_class = getattr(MODULES, modeltype, "Model")
            models[model["uid"]] = model_class(model, self.pp)
            models[model["uid"]].scenario = self.config # please make a more consistent way of accessing the whole file from a model!
        return models

    def load_connections(self):
        connections = {}
        for id, conn in enumerate(self.config["connections"]):
            connection = Connection(id, conn, self.models)
            connection.assign_to_models()
            connections[id] = connection
        return connections