
import numpy as np

from ..tikzelement import tikzElement
from ..elements import tikzCommand
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
        s = tikzCommand().node([self.color, f'opacity={self.alpha}']) \
                         .at() \
                         .coordinate2d(round(self.x,3), round(self.y, 3)) \
                         .label(f'\{self.size} {self.shape}')
        return s.string



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
        s = tikzCommand().draw(self.draw_opts) \
                         .coordinate2d(self.x1, self.y1) \
                         .dash().dash() \
                         .coordinate2d(self.x2, self.y2) \
                         .node(self.labelalign, backslash=False) \
                         .label(self.label)
        return s.string




class text(tikzElement):
    def __init__(self,x, y, string, align = 'right', fontsize = 'tiny', draw_opts = [], **kwargs):
        self.name = give_id('text')

        self.x = x
        self.y = y
        self.string = string
        self.align = align
        self.fontsize = assert_valid_symbolsize(fontsize)
        self.draw_opts = draw_opts

    @property
    def content(self):
        s = tikzCommand().node((self.align, *self.draw_opts)) \
            .at() \
            .coordinate2d(self.x, self.y) \
            .label(f'\{self.fontsize} {self.string}')

        return s.string




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
        return ' '.join([f'({x},{y})' for x,y in pointarray])


    @property
    def content(self):
        s = tikzCommand().draw(self.draw_opts)\
                         .plot(['smooth', f'tension={self.tension}'] if self.smooth else '')\
                         .rawstring('coordinates') \
                         .label(self.points_from_array(self._points))
 
        return s.string


class circle(tikzElement):
    def __init__(self, x, y, radius, draw_opts = []):
        self.name = give_id('circle')

        self.x = x
        self.y = y
        self.radius = radius
        self.draw_opts = draw_opts


    @property
    def content(self):
        s = tikzCommand().draw(self.draw_opts)\
            .coordinate2d(self.x, self.y)\
            .rawstring('circle')\
            .coordinate1d(self.radius)
            
        return s.string
