

from ..tikzelement import Element, tikzElement, pgfAxisOptionElement
from ..tikzbase import tikzBase

from ..utils import * 


class pgfAxis(tikzBase, tikzElement):

    def __init__(self):
        self.name = give_id('pgfaxis')
    
        self._top = r"\begin{axis}"
        self._axis_options = list()
        self._body = dict()
        self._bottom = r"\end{axis}"

    @property
    def top(self):
        return "{top}[{opts}]".format(top = self._top, opts = ','.join([x(self) for x in self._axis_options]))

    @property
    def body(self):
        return '\n'.join([x(self) for x in self._body.values()])
    
    @property
    def content(self):
        return self.top + '\n' + self.body + '\n' + self._bottom


    def add_axis_option(self, option):
        self._axis_options.append(option)


    def __add__(self, axiselement):
        # TODO: this check is made twice if passed to super().__add__

        if hasattr(axiselement, 'components'):
            axiselements = axiselement.components
        elif isinstance(axiselement, Element):
            axiselements = [axiselement]

        for a in axiselements:
            if a.name in self._body:
                raise KeyError(f"figure already contains an element with name {name}")

            if isinstance(a, pgfAxisOptionElement):
                self.add_axis_option(a)
            elif isinstance(a, tikzElement):
                self._body[a.name] = a
            else:
                raise ValueError("pgfbase stupid")
        return self


