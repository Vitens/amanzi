from .category import Category

########################################
########### SIMULATE DATABSE ###########
import json
with open('../inputs/database.json') as db:
    database = json.load(db)
    print(database)
########################################
########################################


class Dosing(Category):
    def __init__(self, process: str, config: dict) -> None:
        super().__init__(process, config)
        
#         self.chemical = None
#         self.molarity = None
#         self.amount = None
    
    @property
    def euro(self):
        cost_per_unit = database['chemicals'][self.chemical]['price']
        dosing_cost = cost_per_unit * self.amount
        print(dosing_cost)
        return dosing_cost