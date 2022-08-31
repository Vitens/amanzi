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

        # self.blocked = False # options: False, block-level 1, block-level 2, block-level 3
        self.mass_flow = 0
        self.solution = False

    def assign_to_models(self):
        self.from_model.connections.setdefault(self.from_anchor, []).append(self)
        self.to_model.connections.setdefault(self.to_anchor, []).append(self)

    def reset_solution(self):
        self.previous_solution = self.solution
        self.solution = False

    def eq(self,factor):
        return [self, factor]        

    @property
    def name(self):
        return "{} -> {}".format(self.from_model.uid, self.to_model.uid)
    
    def __repr__(self):
        return "<connection {} -> {} >".format(self.from_model.uid, self.to_model.uid)

# class Solution:
#     def __init__(self)
