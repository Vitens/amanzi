from .model import Model
from .submodels.splitter import Splitter
 
class Splitter(Model, Splitter):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.configurations = config.get('configuration', {})
        self.split = self.configurations.get('fraction', 0.5)