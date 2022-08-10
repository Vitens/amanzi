from .solver import Solver
from .. import models
from ..components import Connection
import sys 

class Scenario:
    def __init__(self, config):
        self.config = config
        
        self.name = config["name"]
        self.scenario_version = config["scenario_version"]
        
           
        
        #loading
        self.models = self.load_models()  
        self.connections = self.load_connections()
        
        self.solver = Solver(self)
        
        
    def load_models(self):
        models = {}
        for model in self.config['models']:
            uid = model["uid"]
            try:
                model_class = getattr(sys.modules['designer.models'], model['type'].capitalize())
            except:
                # no python model class found (charts etc.)
                print(f"Model {model['type']} has unknown type/template ")
                model_class = getattr(sys.modules['designer.models'], "Model")
      
            models[uid] = model_class(model)
            
        return models
            
        # return {model_config["uid"]: model_class(model_config) for model_config in self.config["models"]}
    
    def load_connections(self):
        connections = []
        for config in self.config["connections"]:
            conn = Connection(config, self.models)
            connections.append(conn)
            conn.assign_connections()
        return connections
  


    
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
        
        