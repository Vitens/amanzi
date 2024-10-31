from .model import Model
from .submodels.balance import Balance
import math

class Sandtrap(Model, Balance):
    parametric_model = ['sandtrap']

    @property
    def context(self):
        ctx = super().context
        ctx['dynamic_viscosity'] = self.dyn_viscosity
        return ctx

    def dyn_viscosity(self, temperature):
        # Viswanath, D.S.; Natarajan, G. (1989). Data Book on the Viscosity of Liquids.
        temperature_in_K = temperature + 273.15
        A= 0.02939 #mPa*s
        B= 507.88 #K
        C = 149.3 #K
        dynamic_viscosity= 1e-3*A*math.exp(B/(temperature_in_K-C)) #[Pa*s] 
        return dynamic_viscosity