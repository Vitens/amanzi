from dotmap import DotMap
from .parametric import ParametricModel

class Model(ParametricModel):
    parametric_model = [] # default to no parametric model

    def __init__(self, config, pp):
        super().__init__(config)
        self.uid = config['uid']
        self.type = config["type"]
        self.name = self.type.capitalize()
        self.emitter = False

        self.connections = []

        self.pp = pp

        """ Solver namespace parameters """
        self.quantity = DotMap({
            'inflow': { 'product': 0, 'waste': 0, 'flush': 0 },
            'outflow': { 'product': 0, 'waste': 0, 'flush': 0 }
        })
        self.quality = DotMap({
            'influent': { 'product': None, 'waste': None, 'flush': None },
            'effluent': { 'product': None, 'waste': None, 'flush': None }
        })
    
    # placeholder for model quality run
    def run_quality(self, type, total_inflow, solution):
        return solution
    

    # calculate minor loss, either as percentage of inflow or as a fixed value
    @property
    def minorloss(self):
        if self.config.get('configuration', {}).get('minorloss_method', 'percentage') != 'percentage':
            return float(self.config.get('configuration', {}).get('minorloss', 0))
        return 0
    
    @property
    def minorloss_percentage(self):
        if self.config.get('configuration', {}).get('minorloss_method', 'percentage') == 'percentage':
            return 1-float(self.config.get('configuration', {}).get('minorloss', 0))
        return 1

    @property
    def emitter_solutions(self):
        return {}

    @property
    def upstream_connections(self):
        upstream = {}
        for c in self.connections:
            if(c.to_model == self):
                upstream.setdefault(c.type, []).append(c)
        return upstream
    
    @property
    def downstream_connections(self):
        downstream = {}
        for c in self.connections:
            if(c.from_model == self):
                downstream.setdefault(c.type, []).append(c)
        return downstream
    
    @property
    def anchors_connections(self):
        anchors = {}
        for c in self.connections:
            anchor = c.from_anchor if c.from_model == self else c.to_anchor
            anchors.setdefault(anchor, []).append(c)

        return anchors

    def design(self):
        # boilerplate
        return {}

    def run_design(self):
        # run model for design
        designData = self.design()
        designData['parameters'] = self.parameters
        designData['tables'] = {'design': self.generate_tables()}
        return designData

