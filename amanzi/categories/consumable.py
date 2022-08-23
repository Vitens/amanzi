from .category import Category

class Consumable(Category):
    def __init__(self, process: str, config: dict) -> None:
        super().__init__(process, config)

