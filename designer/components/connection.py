class Connection:
    num = 0
    def __init__(self, config, models):
        self.num = Connection.num
        Connection.num+=1

        self.from_model = models[config['src']]
        self.from_anchor = config['srcAnchor']
        
        self.to_model = models[config['tgt']]
        self.to_anchor = config['tgtAnchor']

        print(f"Going from {self.from_model} <-> {self.to_model}")

    def assign_connections(self):
        self.from_model.connections.setdefault(self.from_anchor, []).append(self)
        self.to_model.connections.setdefault(self.to_anchor, []).append(self)

    @property
    def name(self):
        return "{} -> {}".format(self.from_model.uid, self.to_model.uid)
    
    def __repr__(self):
        return "<connection {} -> {} >".format(self.from_model.uid, self.to_model.uid)
    
    def eq(self,factor):
        return [self, factor]