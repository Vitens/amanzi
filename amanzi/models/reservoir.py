from .model import Model

class Reservoir(Model):
    @property
    def equations(self):
        # all ingoing streams must match all outgoing streams
        return [[[c.eq(1) for c in self.connections['left']]+ 
                 [c.eq(-1) for c in self.connections['right']] + 
                 [c.eq(-1) for c in self.connections['top']] 
                 , 0]]