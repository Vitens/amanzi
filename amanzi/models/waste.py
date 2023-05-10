from .output import Output
class Waste(Output):
    @property
    def waste(self):
        return round(self.inflow, 2)