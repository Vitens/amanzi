from .solver import Solver
from .. import models
from ..components import Connection
from ..components import solvers
import sys 


MODULES = sys.modules['amanzi.models']

class Scenario:
    def __init__(self, project, config):
        self.config = config
        
        project.assistant.parse_metadata(self)

        # loading
        self.models = self.load_models()  
        self.connections = self.load_connections()
        
        # init solver
        self.solver = Solver(self)

        self.solver.solve()
        
        
    def load_models(self):
        models = {}
        for model in self.config['models']:
            modeltype = model['type'].capitalize()
            model_class = getattr(MODULES, modeltype , "Model")
            models[model["uid"]] = model_class(model)
            
        return models

    def load_connections(self):
        connections = {}
        for id, conn in enumerate(self.config["connections"]):
            connection = Connection(id, conn, self.models)
            connection.assign_to_models()
            connections[id] = connection
        return connections

    @property
    def water_efficiency(self):
        return round((((self.inflow - self.waste) / self.inflow)*100), 2)

    @property
    def inflow(self):
        """Sum all incoming flows, if available."""
        return sum([getattr(model, 'inflow', 0) for model in self.models.values()])

    @property
    def outflow(self):
        """Sum all outgoing flows (including waste), if available."""
        return sum([getattr(model, 'inflow', 0) for model in self.models.values()])

    @property
    def waste(self):
        """Sum all waste flows, if available."""
        return sum([getattr(model, 'waste', 0) for model in self.models.values()])

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
        """Sum all energy consumptions, if available."""
        return sum([getattr(model, 'energy', 0) for model in self.models.values()])        
  

    # def outputs(self):
    #     pass

    # def emitters(self):
    #     pass

    # def mass_loss(self):
    #     pass

    # @property
    # def from_uids(self):
    #     return [conn.from_uid for conn in self.connections.values()]
    
    # @property
    # def to_uids(self):
    #     return [conn.to_uid for conn in self.connections.values()]

    # @property
    # def flows(self):
    #     return sum([conn.mass_flow for conn in self.connections.values()])
    
