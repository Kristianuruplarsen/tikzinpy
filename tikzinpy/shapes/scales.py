
import numpy as np
from collections.abc import Iterable

from ..tikzelement import tikzElement
from .shapes import *
from ..utils import *

_HORIZONTAL = ('horizontal', 'h')
_VERTICAL = ('vertical', 'v')


class arrow(tikzElement):

    def __init__(self, x1, x2, y1, y2, 
                label = '',
                align = '',
                draw_opts = [],
                **kwargs
                 ):
        self.name = give_id('arrow')

        self.x1 = x1
        self.x2 = x2 
        self.y1 = y1 
        self.y2 = y2
        self.label = label
        self.align = align
        self.dopts = draw_opts
        self.kw = kwargs 

        self.line = line(self.x1, self.x2, self.y1, self.y2,
        label = self.label,
        align = self.align,
        draw_opts = [*self.dopts, '->']
        )

    @property 
    def content(self):
        return self.line.content


class ticks(tikzElement):

    def __init__(self, 
                points, 
                direction,
                x = 0,
                y = 0,
                tickwidth = 2,
                tickalign = 'center',
                draw_opts = [],
                rangekwargs = {},
                **kwargs
                ):
        self.name = give_id('ticks')

        self.direction = direction
        self.x = x
        self.y = y
        self.tickwidth = tickwidth
        self.tickpos = tickalign
        self.draw_opts = draw_opts
        self.rangekwargs = rangekwargs

        if isinstance(points, Iterable) and not isinstance(points, str):
            self.points = ','.join(map(str, points)) # _number_range(min(points), max(points), **rangekwargs)
        else:
            self.points = points
        
        if self.tickpos == 'left':
            self.w1 = f"+{int(self.tickwidth)}pt"
            self.w2 = ''
        elif self.tickpos == 'right':
            self.w1 = ''
            self.w2 = f"-{int(self.tickwidth)}pt"                        
        elif self.tickpos == 'center':
            self.w1 = f"+{int(self.tickwidth/2)}pt"
            self.w2 = f"-{int(self.tickwidth/2)}pt"
        
    @property
    def content(self):
        if self.direction in _HORIZONTAL:
            t = line(x1 = f'{str(self.x)}cm + \\x cm',
                     x2 = f'{str(self.x)}cm + \\x cm',
                     y1 = f'{str(self.y)}cm {self.w1}',
                     y2 = f'{str(self.y)}cm {self.w2}',
                     draw_opts = self.draw_opts
                    )
        if self.direction in _VERTICAL:
            t = line(x1 = f'{str(self.x)}cm {self.w1}',
                     x2 = f'{str(self.x)}cm {self.w2}',
                     y1 = f'\\x cm + {str(self.y)}cm',
                     y2 = f'\\x cm + {str(self.y)}cm',
                     draw_opts = self.draw_opts
                    )
        
        s = r"""        
        \foreach \x in {{{pts}}}
            {ticks};
        """.format(pts = self.points, ticks = t.content)

        return s


class tickmarks(tikzElement):

    def __init__(self,
                points,
                direction,
                x=0,
                y=0,
                dx = 0,
                dy = 0,
                rangekwargs = {},
                **kwargs
                ):
        self.name = give_id('tickmarks')

        self.direction = direction 
        self.x = x 
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rangekwargs = rangekwargs
        self.kw = kwargs

        if isinstance(points, Iterable) and not isinstance(points, str):
            self.points = ','.join(map(str, points)) #_number_range(min(points), max(points), **rangekwargs)
        else:
            self.points = points

    @property
    def content(self):
        if self.direction in _HORIZONTAL:
            t = text(x = f'{self.x}cm + \\x cm + {self.dx}pt', 
                     y = f'{self.y}cm + {self.dy}pt', 
                     string = '$\\x$',
                     **self.kw
                     )
        elif self.direction in _VERTICAL:
            t = text(x = f'{self.x}cm + {self.dx}pt', 
                     y = f'{self.y}cm + \\x cm + {self.dy}pt', 
                     string = '$\\x$',
                     **self.kw
                     )

        s = r"""        
        \foreach \x in {{{pts}}}
            {tmarks};
        """.format(pts = self.points, tmarks = t.content)

        return s

