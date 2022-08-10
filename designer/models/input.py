from .model import Model
class Input(Model):
    def __init__(self, config, constant=10):
        super().__init__(config)
        self.constant = constant
    
    @property
    def equations(self):
        return [ [ [self.connections['right'][0].eq(1)], self.constant] ]