from .model import Model
from .submodels.splitter import Splitter

class Recycle(Model, Splitter):
    def __init__(self, config):
        super().__init__(config)
        self.split = config['configuration'].get('fraction', 0.5)
