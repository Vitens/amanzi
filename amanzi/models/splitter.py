from .model import Model
from .submodels.splitter import Splitter
 
class Splitter(Model, Splitter):
    parametric_model = ['splitter']
    def __init__(self, config, pp):
        super().__init__(config, pp)
        config = config.get('configuration', {})
        config = config.get('parameters', {})
        self.split = config.get('split', 0.5)