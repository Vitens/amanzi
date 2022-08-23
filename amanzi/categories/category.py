import pandas as pd
import json

class Category:
    def __init__(self, process: str, config: dict) -> None:
        self.config = config
        self.process = process
        self.category = type(self).__name__.lower()
        self.generate_attributes()
        self.create_summary()
    
    def generate_attributes(self):
        """Fill or generate all relevant class attributes from settings."""
        for key, value in self.config.items():
            setattr(self, key, value)
            
    def create_summary(self):
        self.summary = {'process': self.process,
                        'category': self.category,
                        'euro': self.euro,
                        'emission': self.emission,
                        'energy': self.energy}
        
        # Add categorical specific attributes as columns
        # self.summary.update(self.config)
            
    @property
    def database(self):
        with open('../inputs/database.json') as db:
            database = json.load(db)
        return database

    @property
    def euro(self) -> float:
        return 3_000
    
    @property
    def emission(self) -> float:
        return 500
    
    @property
    def energy(self) -> float:
        return 2_000
        