#import matplotlib.pyplot as plt
#from matplotlib.colors import Normalize
from typing import Union, List

import numpy as np 

from .shapes import *
from ..tikzelement import tikzElement
from ..colors import get_cmap_and_normalizer
from ..utils import *


class pointscatter(tikzElement):
    ''' Draw a 2D scatter of points.
    
    Arguments:
        X: The x-values of data
        Y: The y-values of data
        color: either a string with a fixed color, or the array of data to color
               points by.
        cmap: matplotlib colormap name
        blowout: Share op points that are colored at the extreme upper and lower
                 colors.
    '''
    def __init__(self,
                 X: List[float],
                 Y: List[float], 
                 color: Union[List[float], str] = 'blue', 
                 cmap: str = 'Spectral', 
                 blowout: float = 0, 
                 **kwargs):
        self.name = give_id('pointscatter')
            
        self.X = X
        self.Y = Y
        self.color = color
        self.kw = kwargs
        self.cmap = cmap 
        self.blowout = blowout

    @property
    def components(self):

        if type(self.color) == str:
            points = [point(x,y, color = self.color, **self.kw) for x,y in zip(self.X, self.Y)]

        else:
            sm = get_cmap_and_normalizer(self.cmap, self.blowout, data = self.color)            

            points = []
            for x,y,c in zip(self.X, self.Y, self.color):
                r,g,b,a = map(lambda r: round(r, 4), sm.to_rgba(c))

                points.append( point(x, y, color = self.clr(r,g,b), **self.kw) )

        return points

    def clr(self, r,g,b):
        return 'color={{rgb,1:red,{r};green,{g};blue,{b}}}'.format(r=r, g=g, b=b)



class lineplot(tikzElement):
    def __init__(self, X,Y, *drawopts, color = 'blue', **kwargs):
        self.name = give_id('lineplot')
        
        self.X = X
        self.Y = Y
        self.color = color 
        self.dopts = drawopts
        self.specials = []

        for special in 'label', 'align':
            if special in self.dopts:
                self.specials.append(special)
                self.dopts.remove(special)


    @property
    def components(self):
        lines = []
        for x1,y1,x2,y2 in zip(self.X[:-1], self.Y[:-1], self.X[1:], self.Y[1:]):
            lines.append( line(x1,x2,y1,y2, *self.specials, draw_opts = [self.color, *self.dopts]) )

        return lines




# class function(tikzElement):

#     def __init__(self, function, variable = 'x', draw_opts = ['color=blue'], 
#                 label = '', labelalign = 'right'):
#         self.name = give_id('function')
        
#         self.function = function
#         self.variable = variable
#         self.dopts = draw_opts
#         self.label = label
#         self.labelalign = labelalign

#     @property 
#     def content(self):
#         s = "\draw[{dopts}] plot (\{var}, {{{func}(\{var})}}) node[{all}] {{{label}}};".format(
#                 dopts = ','.join(self.dopts),
#                 var = self.variable,
#                 func = self.function,
#                 all = self.labelalign,
#                 label = self.label
#             )
#         return s