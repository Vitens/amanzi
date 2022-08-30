import pandas as pd

class CategorySolver:
    def __init__(self, scenario: dict) -> None:
        self.scenario = scenario
        self.models = scenario.models

    def solve(self):
        # categories = []
        total_rows = []
        for model in self.models.values():
            # categories.extend(list(model.categories.values()))
            model_rows = []
            for category in model.categories.values():
                row = category.summary
                model_rows.append(pd.Series(data=row, index=None))

            # assign costfuncs per model
            model.costfuncs = pd.concat(model_rows, axis=1).T if len(model_rows) > 0 else None
            
            # collect all costfuncs for whole scenario
            total_rows.extend(model_rows)

        # combine all model-categories
        self.scenario.costfuncs = pd.concat(total_rows, axis=1).T if len(total_rows) > 0 else None
        # df = pd.concat(total_rows, axis=1).T if len(total_rows) > 0 else None
        # return df