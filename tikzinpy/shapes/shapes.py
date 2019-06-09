
import numpy as np

from ..tikzelement import tikzElement
from ..utils import *


class point(tikzElement):
    def __init__(self, x, y, shape = 'fill', color = 'black', alpha = 1, size = 'normalsize', **kwargs):
        self.name = give_id('point')

        self.x = x
        self.y = y
        self.color = color 
        self.alpha = assert_valid_alpha(alpha)
        self.size = assert_valid_symbolsize(size)

        if shape == 'fill':
            self.shape = r'\textbullet'
        elif shape == 'hollow':
            self.shape = r'$\circ$'
        else:
            self.shape = shape


    @property
    def content(self):
        s = r"\node[{clr}, opacity={alph}] at ({x}, {y}) {{\{size} {shp}}};".format(
                x = round(self.x, 3),
                y = round(self.y, 3),
                shp = self.shape,
                clr = self.color,
                alph = self.alpha,
                size = self.size
            )
        return s



class line(tikzElement):
    def __init__(self, x1, x2, y1, y2, draw_opts = ['thick', 'black'], label = '', labelalign = '', **kwargs):
        self.name = give_id('line')

        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2 
        self.draw_opts = draw_opts 

        self.labelalign = labelalign 
        self.label = label

    @property
    def content(self):
        s = "\draw[{dopts}] ({x_min}, {y_min}) -- ({x_max}, {y_max})  node[{align}] {{{label}}};".format(
                dopts = ','.join(self.draw_opts),
                x_min = self.x1,
                x_max = self.x2,
                y_min = self.y1,
                y_max = self.y2,
                align = self.labelalign,
                label = self.label
            )       
        return s 




class text(tikzElement):
    def __init__(self,x, y, string, align = 'right', fontsize = 'tiny', draw_opts = [], **kwargs):
        self.name = give_id('text')

        self.x = x 
        self.y = y 
        self.string = string 
        self.align = align 
        self.fontsize = fontsize 
        self.dopts = draw_opts

    @property
    def content(self):
        s = r"\node[{dopts}] at ({x},{y}) {{\{size} {s}}};".format(
                    s = self.string,
#                    a = self.align,
                    x = self.x,
                    y = self.y,
                    size = self.fontsize,
                    dopts = ', '.join((self.align, *self.dopts))
                )
        return s




class path(tikzElement):
    def __init__(self, *points, cycle=False, smooth = False,
                tension = 2, draw_opts = [], **kwargs):
        self.name = give_id('path')

        if cycle:
            points = (*points, 'cycle')

        self.smooth = smooth
        self.tension = tension

        self._points = np.array(points) 
        self.cycle = cycle
        self.draw_opts = draw_opts
        self.kw = kwargs

    def points_from_array(self, pointarray):
        return [f'({x},{y})' for x,y in pointarray]
        

    @property
    def content(self):
        if self.smooth:
            s = r"\draw[{opts}] plot [smooth, tension={tens}] coordinates {{{points}}};".format(
                opts = ', '.join(self.draw_opts),
                points = ' '.join(self.points_from_array(self._points)),
                tens = self.tension
            )
        else:
            s = r"\draw[{opts}] {points};".format(
                    opts = ', '.join(self.draw_opts),
                    points = ' -- '.join(self.points_from_array(self._points))
                )
        return s        
        


class circle(tikzElement):
    def __init__(self, x, y, radius):
        self.x = x 
        self.y = y 
        self.radius = radius


    @property
    def content(self):
        raise NotImplementedError()