from phreeqpython import PhreeqPython
from dataclasses import dataclass

class ChemicalSolver:
    def __init__(self, scenario):
        self.scenario = scenario
        self.max_iterations = 10
        self.precision = 0.0001
    
    def run_trace(self, model, stream_type):
    
        if not model.is_ready(stream_type):
            return
        solution = model.run(stream_type)
        
        for c in model.downstream_connections.get(stream_type, []):
            c.solution = solution
            self.run_trace(c.to_model, stream_type)
    
    def solve(self):

        for _,c in self.scenario.connections.items():
            c.solution = False
            
        order = ['product', 'flush', 'waste']
        
        for i in range(self.max_iterations):
            for o in order:
                for m in self.emitters[o]:
                    self.run_trace(m, o)
                    
            if self.error < self.precision:
                return
        
        raise Exception('Model did not converge')
    
    @property
    def error(self):
        return sum([m.mass for _,m in self.scenario.models.items()])
        
    @property
    def emitters(self):
        
        emitters = {}
        
        for uid,m in self.scenario.models.items():
            for etype, e in m.emitter_solutions.items():
                emitters.setdefault(etype, []).append(m)
                
        return emitters
