from phreeqpython import PhreeqPython
from dataclasses import dataclass


class ChemicalSolver:
    def __init__(self, scenario):
        self.scenario = scenario
        self.connections = scenario.connections
        self.models = scenario.models
        self.pp = PhreeqPython()

    def solve(self):
        ########################
        #ugly, but temporarely
        for model in self.models.values():
            setattr(model, 'pp', self.pp) 
        ########################

        # emitters =  [model for model in self.models.values() if model.emitter]
        
        # run trace
        flush_cycles = 3
        for i in range(flush_cycles):  
            print("Run step", i)
            self.step()

    def step(self):
        for model in self.emitters:
            self.run_trace(model)

        # reset connections loop
        for conn in self.connections.values():
            try:
                print(f"Conn.id: {conn.id} -  'pH': {conn.solution.pH}")
            except:
                pass
            conn.reset_solution()

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
        for conn in model.downstream_connections:
            if not conn.blocked:
                self.run_trace(conn.to_model)

    @property
    def emitters(self):
        return [model for model in self.models.values() if model.emitter]
