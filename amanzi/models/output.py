from .model import Model

class Output(Model):
    @property
    def equations(self):
        return []
    
    @property
    def mass(self):
        inflow = sum([c.flow for c in self.upstream_connections['product']])
        return -self.solution.total('Na') * inflow
