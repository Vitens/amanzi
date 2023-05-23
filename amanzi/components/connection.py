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
        self.from_model.connections.append(self)
        self.to_model.connections.append(self)

    def reset_solution(self):
        self.solution = False

    def eq(self,factor):
        return [self, factor]        
    
    def chem(self, key):
        return self.solution.total(key)

    @property
    def cid(self):
        return "{} ({}) -> {} ({})".format(self.from_model.uid, self.from_anchor, self.to_model.uid, self.to_anchor)

    @property
    def name(self):
        return "{} -> {} ({})".format(self.from_model.uid, self.to_model.uid, self.type)
    
    def __repr__(self):
        # return "<connection {} -> {} ({})>".format(self.from_model.uid, self.to_model.uid, self.type)
        return "<connection {} -> {} ({})>".format(self.from_model.name, self.to_model.name, self.type)
