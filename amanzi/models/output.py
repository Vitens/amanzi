from .model import Model
import logging

class Output(Model):
    parametric_model = ['base', 'output']

    @property
    def equations(self):
        return []