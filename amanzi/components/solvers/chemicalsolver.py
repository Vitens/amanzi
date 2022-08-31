from phreeqpython import PhreeqPython
from dataclasses import dataclass


class ChemicalSolver:
    def __init__(self, scenario):
        self.scenario = scenario
        self.connections = scenario.connections
        self.models = scenario.models
        self.pp = PhreeqPython()

    def solve(self):
        emitters = []
        for model in self.models.values():
            setattr(model, 'pp', self.pp) #ugly, but temporarely
            emitters.append(model)

        # emitters =  [model for model in self.models.values() if model.emitter]
        
        # run trace
        for model in emitters:
            self.run_trace(model)

        # reset connections loop
        for connection in self.connections.values():
            connection.reset_solution()
        pass

    def run_trace(self, model):
        # wait for all upstream nodes to be calculated
        if not model.ready:
            self.last_model = model
            return

        # run model
        try:
            model.run()
        except:
            print("Run failed in model", model.uid)
            raise

        # run downstream models
        for connection in model.downstream_connections:
            self.run_trace(connection.to_model)    

    # @property
    # def emitters(self):
    #     return [model for model in self.models.values() if model.emitter]

    # def solve(self):
    #     for model in self.scenario.models.values():
    #         model.solve(self.pp)
    #         print(model.type, model.name)
    #         print(model.effluent)

