from .model import Model
from .submodels.splitter import Splitter
 
class Splitter(Model, Splitter):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.split = config.get('configuration',{}).get('fraction', 0.5)