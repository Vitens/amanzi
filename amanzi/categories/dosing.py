from .category import Category
class Dosing(Category):
    def __init__(self, process: str, config: dict) -> None:
        super().__init__(process, config)
        
#         self.chemical = None
#         self.molarity = None
#         self.amount = None
    
    @property
    def euro(self) -> float:
        cost_per_unit = self.database['chemicals'][self.chemical]['price']
        dosing_cost = cost_per_unit * self.amount
        return dosing_cost

    @property
    def emission(self) -> float:
        co2_footprint = self.database['chemicals'][self.chemical]['co2_footprint'] # co2eq/unit
        return co2_footprint * self.amount


    