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
        return self.config["connections"]
        # return [Connection(conn) for conn in self.config["connections"]]
  


    
    @property
    def cost(self):
        return sum([model.cost for model in self.models.values()])

    @property
    def emission(self):
        return sum([model.emission for model in self.models.values()])

    @property    
    def energy(self):
        return sum([model.energy for model in self.models.values()])
        
        