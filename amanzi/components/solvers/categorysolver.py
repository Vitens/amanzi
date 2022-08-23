import pandas as pd

class CategorySolver:
    def __init__(self, scenario: dict) -> None:
        self.models = scenario.models

    def solve(self):
        # categories = []
        rows = []
        for model in self.models.values():
            # categories.extend(list(model.categories.values()))
            for category in model.categories.values():
                row = category.summary
                rows.append(pd.Series(data=row, index=None))

        # combine all model-categories
        df = pd.concat(rows, axis=1).T if len(rows) > 0 else None
        return df