from .model import Model
from .submodels.balance import Balance

class Softening(Model, Balance):
    def __init__(self, config, pp) -> None:
        super().__init__(config, pp)
        self.config = config