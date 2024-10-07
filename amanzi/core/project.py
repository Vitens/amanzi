from .database import Database
from .scenario import Scenario
import json

class Project:
    def __init__(self, slm = "", debug=True):                

        self.config = self.load_file(slm)

        # self.database = Database()
        # # overwrite key figures for the whole project
        # self.database.overwrite(self.config['key_figure_overwrites'])

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
    
    def report(self):

        return {
            'scenarios': [s.name for _,s in self.scenarios.items()],
            'results': [self.scenarios[s].report() for s in self.scenarios]
        }