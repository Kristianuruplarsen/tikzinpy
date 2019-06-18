
import subprocess
import pathlib 
from collections.abc import Iterable
from math import floor 

from .tikzelement import (Element, 
                          tikzElement, 
                          preambleElement, 
                          packageElement)

from .utils import *


def set_xy_ratio(xy):
    x, y = [float(i) for i in xy.split(':')]
    scale = max([x,y])
    const = min([x,y])

    y, x = [1/i for i in (x,y)]
#    scale = min([x,y])**-1
#    y,x = tuple(map(lambda x: 1/float(x), xy.split(':')))

    y,x = y*scale*const, x*scale*const
    return y, x


class tikzBase():
    ''' The base on which we draw.

    Arguments:
        border: border width around the figure
        xy_ratio: a sting like 2:1 which determines the aspect
                  of the figure.
    '''

    def __init__(self, border = '2mm', xy_ratio = '1:1'):
        self.xy_ratio = xy_ratio
        self.yratio, self.xratio = set_xy_ratio(xy_ratio)
        self.n_calls = 0

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


    def rescale(self, elementcls):
        for xval in ('x', 'x1', 'x2'):
            try:
                setattr(elementcls, xval, getattr(elementcls, xval)*self.xratio)
            except AttributeError:
                pass 

        for yval in ('y', 'y1', 'y2'):
            try:
                setattr(elementcls, yval, getattr(elementcls, yval)*self.yratio)                
            except AttributeError:
                pass

        for dirval in ('_points',):
            try:
                if elementcls.direction in HORIZONTAL:
                    setattr(elementcls, 'scaleconst', self.xratio**-1)                    
                    setattr(elementcls, dirval, getattr(elementcls, dirval)*self.xratio)
                if elementcls.direction in VERTICAL:
                    setattr(elementcls, 'scaleconst', self.yratio**-1)                    
                    setattr(elementcls, dirval, getattr(elementcls, dirval)*self.yratio)
            except AttributeError:
                pass

        return elementcls
