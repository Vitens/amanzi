<<<<<<< HEAD
from .output import Output

class Waste(Output):
    @property
    def waste(self):
        return round(self.inflow, 2)
=======
from .model import Model

class Waste(Model):
    @property
    def equations(self):
        return []
>>>>>>> main
