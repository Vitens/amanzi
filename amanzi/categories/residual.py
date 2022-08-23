from .category import Category

class Residual(Category):
    def __init__(self, process: str, config: dict) -> None:
        super().__init__(process, config)

    @property
    def euro(self):
        deposition_cost = self.database['compounds'][self.compound]['deposition_cost']
        return deposition_cost * self.amount
        
