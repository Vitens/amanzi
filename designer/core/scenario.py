from .solver import Solver
from .. import models
from ..components import Connection
from ..components import solvers
import sys 


MODULES = sys.modules['designer.models']

class Scenario:
    def __init__(self, config):
        self.config = config
        
        # parse metadata
        self.name = config["name"]
        self.scenario_version = config["scenario_version"]
 
        # loading
        self.models = self.load_models()  
        self.connections = self.load_connections()
        
        # init solver
        self.solver = Solver(self)
        
        
    def load_models(self):
        models = {}
        for model in self.config['models']:
            modeltype = model['type'].capitalize()
            model_class = getattr(MODULES, modeltype , "Model")
            models[model["uid"]] = model_class(model)
            
        return models

    def load_connections(self):
        connections = {}
        for i, conn in enumerate(self.config["connections"]):
            connection = Connection(i, conn, self.models)
            connection.assign_to_models()
            connections[id] = connection
        return connections
  

    def outputs(self):
        pass

    def emitters(self):
        pass

    def mass_loss(self):
        pass

    @property
    def from_uids(self):
        return [conn.from_uid for conn in self.connections.values()]
    
    @property
    def to_uids(self):
        return [conn.to_uid for conn in self.connections.values()]

    @property
    def flows(self):
        return sum([conn.mass_flow for conn in self.connections.values()])
    
    @property
    def cost(self):
        """Sum all costs, if available."""
        return sum([getattr(model, 'cost', 0) for model in self.models.values()])

    @property
    def emission(self):
        """Sum all emissions, if available."""
        return sum([getattr(model, 'emission', 0) for model in self.models.values()])

    @property    
    def energy(self):
        """Sum all energy, if available."""
        return sum([getattr(model, 'energy', 0) for model in self.models.values()])
        
        