import numpy as np

class Solver:
    def __init__(self, scenario):
        self.scenario = scenario
        self.connect_models()
        
        # self.solve_mass_balance()

    def solve_mass_balance(self):
        matrix = []
        connections = list(range(self.scenario.connections))
        all_equations = []
        results = []
        
        # collect equations 
        for uid, model in self.scenario.models.items():
            for eq, mass in model.equations:
                all_equations.append(eq)
                results.append(mass)
        
        # construct matrix
        matrix = np.zeros((len(all_equations), len(results)))
        
        # fill matrix
        row = 0
        for eq in all_equations:
            for c,weight in eq:
                connections[c.num] = c
                matrix[row,c.num] = weight
            row+=1   

        # solve matrix
        solved = np.linalg.solve(matrix, results)

        #assign massflows to connections
        

        return solved

    def connect_models(self):
        # connect models and connections        
        for conn in self.scenario.connections:
            from_model = self.scenario.models[conn['src']]
            from_anchor = conn['srcAnchor']
            to_model = self.scenario.models[conn['tgt']]
            to_anchor = conn['tgtAnchor']

            from_model.connect(from_anchor, to_model, to_anchor)
            

    
    def energy_solver(self):
        for ui, model in self.scenario.models.items():
            value = model.__dict__.get("energy")
        
       
        
        