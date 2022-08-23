
class CategorySolver:
    def __init__(self, scenario: dict) -> None:
        print("Hi from CategorySolver")
        print(scenario)

        self.models = scenario.models

    def solve(self):
        self.collect_categories()

    def collect_categories(self):
        for model in self.models:
            for cname, cat in model.categories.items():
                print(cname)
                print(cat.__dict__)




