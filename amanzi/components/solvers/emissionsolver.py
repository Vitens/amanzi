from dataclasses import dataclass

@dataclass
class EmissionSolver:
    scenario: dict

    def solve(self):
        pass