from .model import Model
from .submodels.splitter import Splitter

class Membrane(Model, Splitter):
    def __init__(self, config):
        super().__init__(config)
        self.split = config['configuration'].get('recovery', 0.8)