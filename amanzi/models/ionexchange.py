from .model import Model
from .submodels.balance import Balance

class Ionexchange(Model, Balance):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        # self.config = config
        print("Ionexchange")

        

    # def run_model(self, type, total_inflow, solution):
    #     permeate = solution.copy()
    #     ion_removal = {}

    #     ion_removal = {}
    #     for ion, ret in self.retention.items():
    #         ion_removal[ion] = solution.total(ion, 'mmol') * ret  * -0.99999
        
    #     permeate.change(ion_removal, 'mmol')