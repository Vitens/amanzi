import phreeqpython
import copy
from collections import OrderedDict
from ..components.solvers import QuantitySolver, QualitySolver, HydraulicSolver, EnergySolver, SustainabilitySolver, ChemicalSolver
from .. import models
from ..components import Connection, solution
from .database import Database

import sys

MODULES = sys.modules['amanzi.models']

class Scenario:
    def __init__(self, project, config):
        self.config = config
        self.name = config['name']
        self.pp = phreeqpython.PhreeqPython()

        # load database and apply overwrites for this scenario during initialization
        self.database = Database()
        self.database.overwrite(project.config['key_figure_overwrites'])
        self.database.overwrites = self.config['key_figure_overwrites']

        # load models and connections
        self.models = self.load_models()  
        self.connections = self.load_connections()
        self.metaData = config.get('metaData', {})


        # list of solvers
        self.solvers = OrderedDict({
            'quantity': QuantitySolver(self),
            'quality': QualitySolver(self),
            'hydraulics': HydraulicSolver(self),
            'energy': EnergySolver(self),
            'chemicals': ChemicalSolver(self),
            'sustainability': SustainabilitySolver(self)
        })

    def run_scenario(self, until=None):
        # run all solvers in order
        for _,solver in self.solvers.items():
            solver.solve(until)

    def report(self):
        # solve the scenario
        self.run_scenario()
        # model indices
        order = {m.name: m.index for i,m in self.models.items()}
        # transform to list ordered by index:
        order = [name for name, index in sorted(order.items(), key=lambda item: item[1])]



        return {
            'summaries': {s: self.solvers[s].summary() for s in self.solvers},
            'order': order
            }

    def load_models(self):
        models = {}
        for model in self.config['models']:
            modeltype = model['type'].capitalize()
            model_class = getattr(MODULES, modeltype, "Model")
            models[model["uid"]] = model_class(model, self.pp)
            models[model["uid"]].scenario = self.config # please make a more consistent way of accessing the whole file from a model!
            models[model["uid"]].database = self.database

        return models

    def load_connections(self):
        connections = {}
        for id, conn in enumerate(self.config["connections"]):
            connection = Connection(id, conn, self.models)
            connection.assign_to_models()
            connections[id] = connection
        return connections