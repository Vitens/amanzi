from .output import Output
class Waste(Output):
    @property
    def waste(self):
        return round(self.inflow, 2)

    @property
    def mass(self):
        inflow = sum([c.flow for c in self.upstream_connections['waste']])
        return -self.solution.total('Na') * inflow