
import subprocess
import pathlib 
from collections.abc import Iterable

from .tikzelement import (Element, 
                          tikzElement, 
                          preambleElement, 
                          packageElement)


class tikzBase():
    ''' The base on which we draw.
    '''

    def __init__(self, border = '2mm'):

        self._top = r"""
        \documentclass[tikz, border={b}]{{standalone}}
        """.format(b = border)

        self._preamble = dict()
        self._packages = [packageElement('tikz'), packageElement('xcolor')]

        self._begin_doc = r"""
        \begin{document}    
            \begin{tikzpicture}
        """

        self._bottom = r"""
            \end{tikzpicture}
        \end{document}
        """

        self._body = dict()

        self.saved = False 
        self.filename = None


    @property
    def body(self):
        # The x(self) allows in theory each element to be a function of 
        # the base class.
        return '\n'.join([x(self) for x in self._body.values()])
    
    @property
    def packages(self):
        return '\n'.join([r'\usepackage{{{}}}'.format(p(self)) for p in self._packages])    
    
    @property 
    def preamble(self):
        return '\n'.join([x(self) for x in self._preamble.values()])

    @property
    def top(self):
        return self.top
        
    @property
    def figure(self):
        figure = self._top + self.packages + self.preamble + self._begin_doc + self.body + self._bottom
        return figure

    def add(self, element, overwrite = False):
        ''' Add one or more elements to the figure
        '''
        # Makes it possible to add multiple base components
        # from a single class.
        if hasattr(element, 'components'):
            elements = element.components
        elif isinstance(element, Element):
            elements = [element]

        for e in elements:
            name = e.name
            if not overwrite and name in self._body:
                raise KeyError(f"figure already contains an element with name {name}")

            if isinstance(e, tikzElement):
                self._body[name] = e
            elif isinstance(e, preambleElement):
                self.add_to_preamble(name, e)
            elif isinstance(e, packageElement):                
                self.add_package(e)                
            else:
                raise ValueError(f"element of type {type(element)} is not valid.")

        return self

    def remove(self, name):
        del self._body[name]
        return self

    def __add__(self, tikzelements):
        return self.add(tikzelements)

    def __sub__(self, name):
        return self.remove(name)


    def add_package(self, package):

        # Fix add_package('packagename') 
        if isinstance(package, str):
            package = preambleElement(package, package)

        # Dont add if already there
        for p in self._packages:
            if p.name == package.name:
                return self 
        self._packages.append(package)

    def remove_package(self, packagename):
        self._packages.remove(packagename)


    def add_to_preamble(self, name, addition):
        self._preamble[name] = addition

    def remove_from_preamble(self, name):
        del self._preamble[name]
