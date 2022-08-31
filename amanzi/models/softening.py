from .model import Model
from .submodels.balance import Balance

class Softening(Model, Balance):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.config = config