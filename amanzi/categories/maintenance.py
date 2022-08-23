from .category import Category

class Maintenance(Category):
    def __init__(self, process: str, config: dict) -> None:
        super().__init__(process, config)
        
#         self.amount = None
#         self.frequency = None
#         self.subunit = None
        
