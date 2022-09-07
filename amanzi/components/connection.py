class Connection:
    def __init__(self, id, config, models):
        self.id = id
        self.from_uid = config['src']
        self.from_model = models[config['src']]
        self.from_anchor = config['srcAnchor']
        
        self.to_uid = config['tgt']
        self.to_model = models[config['tgt']]
        self.to_anchor = config['tgtAnchor']

        self.type = config['type']

        self.iteration = 0

        self.flow = 0
        self.solution = False



    def assign_to_models(self):
        self.from_model.connections.setdefault(self.from_anchor, []).append(self)
        self.to_model.connections.setdefault(self.to_anchor, []).append(self)

    def reset_solution(self):
        try:
            print(f"{self.id} - {self.type} - {self.solution.total('Na')}")
        except:
            pass
        self.iteration += 1
        self.previous_solution = self.solution
        self.solution = False

    def eq(self,factor):
        return [self, factor]        

    @property
    def name(self):
        return "{} -> {}".format(self.from_model.uid, self.to_model.uid)
    
    def __repr__(self):
        return "<connection {} -> {} >".format(self.from_model.uid, self.to_model.uid)

    @property
    def blocked(self):
        """Blocks connections for calculations in ChemicalSolver"""
        if self.type == 'product':
            return False
        elif self.type == 'flush' and self.iteration > 0:
            return False
        elif self.type == 'waste' and self.iteration > 1:
            return False
        else:
            return True

class Solution:
    """Replaces conn.solution. This class contains a phreeqpython solution and/or Reststoffen and such"""
    def __init__(self):
        pass
