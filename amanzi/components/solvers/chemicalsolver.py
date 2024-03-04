from phreeqpython import PhreeqPython
from dataclasses import dataclass

class ChemicalSolver:
    # For debugging purposes
    parent_loop_count = 0

    def __init__(self, scenario):
        self.scenario = scenario
        self.max_iterations = 100
        self.precision = 0.0001
        self.data = {}
        self.stop_at_model = None
        self.interrupted = False
    
    def run_trace(self, model, stream_type):
    
        if not model.is_ready(stream_type):
            return
        solution = model.run(stream_type)
        if self.stop_at_model and model.uid == self.stop_at_model:
            print('Interrupted at model {}'.format(model.uid))
            self.interrupted = True # interrupt the solver
            return
        
        for c in model.downstream_connections.get(stream_type, []):
            c.solution = solution
            if(c.flow > 0):
                self.run_trace(c.to_model, stream_type)
    
    def solve(self, until=None):

        self.stop_at_model = until
        self.interrupted = False

        for _,c in self.scenario.connections.items():
            c.solution = False
            
        order = ['product', 'flush', 'waste']
        
        for i in range(self.max_iterations):
            for o in order:
                for m in self.emitters.get(o, []):
                    self.run_trace(m, o)
                if self.interrupted:
                    return
                    
            # check convergence for all elements
            failed = False

            for e,c in self.error.items():
                 if abs(c) > self.precision:
                    failed = True
            
            if not failed:
                print('Converged in {} iterations'.format(i))
                return

        raise Exception('Model did not converge in {} iterations. Mass balance is {}'.format(self.max_iterations, self.error))
    
    @property
    def error(self):
        # gather all mass in the system
        balance = {}
        for m in self.scenario.models.values():
            for e, c in m.mass.items():
                balance[e] = balance.get(e, 0) + c
        
        return balance
        
    @property
    def emitters(self):
        
        emitters = {}
        
        for uid,m in self.scenario.models.items():
            for etype, e in m.emitter_solutions.items():
                emitters.setdefault(etype, []).append(m)
                
        return emitters