
# TODO: the number range thing is confusing, move everything to np array,
# instead of using ','.join everywhere

from collections.abc import Iterable

from .shapes import *
from .scales import *
from ..utils import *

class xaxis(tikzElement):

    def __init__(self, x1, x2, y, **kwargs):
        self.name = give_id('xaxis')

        self.x1 = x1
        self.x2 = x2
        self.y = y

        self.eps = set_eps(**kwargs)

        if not 'points' in kwargs:
            self.pts = list(map(float, drange(x1, x2, 1) ))
        else:
            self.pts = points

        self.line = arrow(x1-self.eps,x2+self.eps,y,y, **kwargs)
        self.tcks = ticks(self.pts, 'h', y=y, **kwargs)
        self.marks = tickmarks(self.pts, 'h', y=y, **kwargs)

    @property 
    def components(self):
        return [self.line, self.tcks, self.marks]



class yaxis(tikzElement):

    def __init__(self, y1, y2, x, **kwargs):
        self.name = give_id('yaxis')

        self.y1 = y1
        self.y2 = y2
        self.x = x

        self.eps = set_eps(**kwargs)

        if not 'points' in kwargs:
            self.pts = list(map(float, drange(y1, y2, 1) ))
        else:
            self.pts = points
        
        self.line = arrow(x,x,y1 - self.eps,y2 + self.eps, **kwargs)
        self.tcks = ticks(self.pts, 'v', x=x, **kwargs)
        self.marks = tickmarks(self.pts, 'v', x=x, **kwargs)

    @property 
    def components(self):
        return [self.line, self.tcks, self.marks]


