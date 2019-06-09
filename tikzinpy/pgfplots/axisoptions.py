
from ..tikzelement import pgfAxisOptionElement

class Label(pgfAxisOptionElement):
    def __init__(self, label, variable):
        self.label = label
        self.var = variable

    @property
    def content(self):
        return f"{self.var}label={self.label}"


class xlabel(Label):
    def __init__(self, label):
        super().__init__(label, 'x')
    

class ylabel(Label):
    def __init__(self, label):
        super().__init__(label, 'y')
    

