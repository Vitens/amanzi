from abc import ABC, abstractmethod

class Solver(ABC):
    def __init__(self, scenario):
        self.scenario = scenario
        self.solved = False

    @abstractmethod
    def solve(self, until=None):
        pass

    @abstractmethod
    def summary(self):
        pass