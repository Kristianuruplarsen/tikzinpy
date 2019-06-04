import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np 

from .shapes import *
from ..tikzelement import tikzElement
from ..colors import get_cmap_and_normalizer
from ..utils import *


class scatter():

    def __init__(self, X,Y, color = 'blue', cmap = 'Spectral', blowout = 5, **kwargs):
        self.X = X
        self.Y = Y
        self.color = color
        self.kw = kwargs
        self.cmap = cmap 
        self.blowout = blowout

    @property
    def components(self):

        if type(self.color) == str:
            comp = [point(x,y, color = self.color, **self.kw) for x,y in zip(self.X, self.Y)]

        else:
#            cmap, norm = get_cmap_and_normalizer(self.cmap, self.blowout, data = self.color)            
            sm = get_cmap_and_normalizer(self.cmap, self.blowout, data = self.color)            

            comp = []
            for x,y,c in zip(self.X, self.Y, self.color):
    #            r,g,b,_ = cmap(norm(c), bytes = False)                
                r,g,b,a = map(lambda r: round(r, 4), sm.to_rgba(c))                
                comp.append( point(x, y, color = clr(r,g,b), **self.kw) )

        return comp

    # def clr(self, r, g, b):
    #     return 'color={{rgb:red,{r};green,{g};blue,{b}}}'.format(r=r, g=g, b=b)


# TODO: line plot
class plot():
    def __init__(self, X,Y, color, **kwargs):
        self.X = X
        self.Y = Y
        self.color = color 
        self.kw = kwargs

    @property
    def components(self):
        pass

