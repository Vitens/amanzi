from .category import Category

########################################
########### SIMULATE DATABSE ###########
import json
with open('../inputs/database.json') as db:
    database = json.load(db)
    print(database)
########################################
########################################


class Maintenance(Category):
    def __init__(self, process: str, config: dict) -> None:
        super().__init__(process, config)
        
#         self.amount = None
#         self.frequency = None
#         self.subunit = None
        
