

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
            self.pts = number_range(x1, x2, **kwargs)
        elif isinstance(kwargs['points'], Iterable) and not isinstance(kwargs['points'], str):
            self.pts = ','.join(map(str, kwargs['points']))
        else:
            self.pts = points

        self.line = arrow(x1,x2,y,y, **kwargs)
        self.tcks = ticks(self.pts, 'h', **kwargs)
        self.marks = tickmarks(self.pts, 'h', **kwargs)

    @property 
    def components(self):
        return [self.line, self.tcks, self.marks]



class yaxis(tikzElement):

    def __init__(self, y1, y2, x, **kwargs):
        self.name = give_id('xaxis')

        self.y1 = y1
        self.y2 = y2
        self.x = x

        self.eps = set_eps(**kwargs)

        if not 'points' in kwargs:
            self.pts = number_range(y1, y2, **kwargs)
        elif isinstance(kwargs['points'], Iterable) and not isinstance(kwargs['points'], str):
            self.pts = ','.join(map(str, kwargs['points']))
        else:
            self.pts = points

        self.line = arrow(x,x,y1,y2, **kwargs)
        self.tcks = ticks(self.pts, 'v', **kwargs)
        self.marks = tickmarks(self.pts, 'v', **kwargs)

    @property 
    def components(self):
        return [self.line, self.tcks, self.marks]
