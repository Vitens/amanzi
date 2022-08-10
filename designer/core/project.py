from .scenario import Scenario
# from .components import ProjectManager
import json


class Project:
    def __init__(self, slm = "projectA.slm", debug=True):        
        self.config = self.load_file(slm)
        
#         self.ui_version = config["metadata"]["ui_version"]
#         self.version = config["metadata"]["version"]        
        # self.manager = ProjectManager(self.config)
        self.scenarios = self.load_scenarios()
         
    def load_scenarios(self):
        return {s: Scenario(scenario_config) for s, scenario_config in enumerate(self.config['scenarios'], 1)}
        
    def load_file(self, file):
        with open(file) as slm:
            output = json.load(slm)
#         print(json.dumps(output, indent=2, sort_keys=True))
        return output

# project = Project("../../projectA.slm")
