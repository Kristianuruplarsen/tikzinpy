
import numpy as np
from collections.abc import Iterable

from ..tikzelement import tikzElement
from .shapes import *
from ..utils import *


class arrow(tikzElement):

    def __init__(self, x1, x2, y1, y2, 
                label = '',
                labelalign = '',
                draw_opts = [],
                **kwargs
                 ):
        self.name = give_id('arrow')

        self.x1 = x1
        self.x2 = x2 
        self.y1 = y1 
        self.y2 = y2
        self.label = label
        self.labelalign = labelalign
        self.dopts = draw_opts
        self.kw = kwargs 

    @property 
    def content(self):
        lne = line(self.x1, self.x2, self.y1, self.y2,
        label = self.label,
        labelalign = self.labelalign,
        draw_opts = [*self.dopts, '->'],
        **self.kw
        )

        return lne.content


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

        self._points = np.array(points)
        
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
    def points(self):
        points = ','.join(map(str, self._points)) 
        return points


    @property
    def content(self):
        if self.direction in HORIZONTAL:
            t = line(x1 = f'{str(self.x)}cm + \\x cm',
                     x2 = f'{str(self.x)}cm + \\x cm',
                     y1 = f'{str(self.y)}cm {self.w1}',
                     y2 = f'{str(self.y)}cm {self.w2}',
                     draw_opts = self.draw_opts
                    )
        if self.direction in VERTICAL:
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
        self.scaleconst = 1
        self.x = x 
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rangekwargs = rangekwargs
        self.kw = kwargs
        self._points = np.array(points)


    @property
    def points(self):
        points = ','.join(map(str, self._points)) 
        return points


    @property
    def content(self):
        if self.direction in HORIZONTAL:
            t = text(x = f'{self.x}cm + \\x cm + {self.dx}pt', 
                     y = f'{self.y}cm + {self.dy}pt', 
                     string = '$\\pgfmathprintnumber{\\i}$',
                     **self.kw
                     )
        elif self.direction in VERTICAL:
            t = text(x = f'{self.x}cm + {self.dx}pt', 
                     y = f'{self.y}cm + \\x cm + {self.dy}pt', 
                     string = '$\\pgfmathprintnumber{\\i}$',
                     **self.kw
                     )

        s = r"""        
        \foreach \x in {{{pts}}}
            \pgfmathsetmacro\i{{{sc}*\x}}
            {tmarks};
        """.format(pts = self.points, tmarks = t.content, sc = self.scaleconst)

        return s




