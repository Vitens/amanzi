from dotmap import DotMap

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

        # flow in the connection, set by quantity solver
        self.quantity = DotMap({
            'flow': 0
        })
        self.quality = DotMap({
            'solution': False
        })
        self.hydraulics = DotMap({
            'booster': False,
            'booster_head': 0,
            'efficiency': None,
            'headloss': 0
        })

    def assign_to_models(self):
        self.from_model.connections.append(self)
        self.to_model.connections.append(self)

    def eq(self,factor):
        return [self, factor]        
    
    """ connection id 
    composed of from_model.uid, from_anchor, to_model.uid, to_anchor
    """
    @property
    def cid(self):
        return "{} ({}) -> {} ({})".format(self.from_model.uid, self.from_anchor, self.to_model.uid, self.to_anchor)

    @property
    def name(self):
        return "{} -> {} ({})".format(self.from_model.uid, self.to_model.uid, self.type)
    
    def __repr__(self):
        # return "<connection {} -> {} ({})>".format(self.from_model.uid, self.to_model.uid, self.type)
        return "<connection {} -> {} ({})>".format(self.from_model.name, self.to_model.name, self.type)
