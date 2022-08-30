from .model import Model
class Groundwater(Model):
    def __init__(self, config):
        super().__init__(config)
        self.constant = config['configuration'].get("production", 0)
    
    @property
    def equations(self):
        return [ [ [self.connections['right'][0].eq(1)], self.constant] ]