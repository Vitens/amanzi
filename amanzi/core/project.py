from .scenario import Scenario
from ..components.assistant import Assistant
import json


class Project:
    def __init__(self, slm = "inputs/projectC.slm", debug=True):                
        self.config = self.load_file(slm)
        #self.assistant = Assistant(self)
        self.scenarios = self.load_scenarios()
         
    def load_scenarios(self):
        return {s: Scenario(self, scenario) 
            for s, scenario in enumerate(self.config['scenarios'], 0)}
        
    def load_file(self, file):
        if isinstance(file, dict):
            return file
        with open(file) as slm:
            output = json.load(slm)
        return output