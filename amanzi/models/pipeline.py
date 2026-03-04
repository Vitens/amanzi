from .model import Model
from .submodels.balance import Balance

class Pipeline(Model, Balance):
    parametric_model = ['base', 'transport', 'pipeline']