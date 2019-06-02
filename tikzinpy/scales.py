
import numpy as np
from .tikzelement import tikzElement
from .utils import give_id, coerce_to_strint, drange

_HORIZONTAL = ('horizontal', 'h')
_VERTICAL = ('vertical', 'v')


def arrow(x_min, x_max, y_min, y_max, label = 'label', nodepos = 'above', width = 'thick', **kwargs):
    ''' Draw an arrow from (x_min, y_min) to (x_max, y_max)
        This is used to draw the coordinate system.
    '''
    s = "\draw[{w}, ->] ({x_min},{y_min}) -- ({x_max},{y_max}) node[{a}] {{${l}$}};".format(
            w = width,
            x_min = x_min,
            y_min = y_min,
            x_max = x_max,
            y_max = y_max,
            a = nodepos,
            l = label
        )
    return tikzElement(s, give_id('arrow'))


def _number_range(start, stop, decimals = 0, remove_zero = False, **kwargs):
    ''' Return numbers from `start` to `stop` in steps 
        of 10^(-`decimal')
    '''
    points = ','.join(list(drange(start, stop, 10**(-decimals))))
    if remove_zero:
        return ','.join([x for x in points.split(',') if x != '0'])
    return points
number_range = _number_range        # This is just for showing off the atomics in the notebook


def ticks(points, direction, width = 2, **kwargs):
    ''' Draw tick marks at each point in points, along either the
        horizontal (h) or vertical (v) axis.
    '''
    w = f"{int(width/2)}pt"

    if direction in _HORIZONTAL:
        t = r"\draw (\x cm, {w}) -- (\x cm, -{w})".format(w=w)
    elif direction in _VERTICAL:
        t = r"\draw ({w}, \x cm) -- (-{w}, \x cm)".format(w=w)

    s = r"""        
    \foreach \x in {{{pts}}}
        {t};
    """.format(pts = points, t = t)

    return tikzElement(s, give_id('ticks'))


def tickmarks(points, direction, offset = '-5pt', fontsize = 'footnotesize', **kwargs):
    ''' Draw numbered tick marks at each point in points, along either the
        horizontal (h) or vertical (v) axis.
    '''
    if direction in _HORIZONTAL:
        t = r"\node at (\x, {off})  {{\{fs} $\x$}}".format(off = offset, fs = fontsize)
    elif direction in _VERTICAL:
        t = r"\node at ({off}, \x)  {{\{fs} $\x$}}".format(off = offset, fs = fontsize)

    s = r"""        
    \foreach \x in {{{pts}}}
        {t};
    """.format(pts = points, t = t)

    return tikzElement(s, give_id('tickmarks'))


def set_eps(**kwargs):
    if 'eps' in kwargs:
        return kwargs['eps']
    else:
        return 0.5

def xaxis(x_min, x_max, **kwargs):
    ''' Draw an x-axis
    '''
    eps = set_eps(**kwargs)    
    pts = _number_range(x_min, x_max, **kwargs)

    ar = arrow(x_min - eps, x_max + eps, 0, 0, **kwargs)
    tcks = ticks(pts, 'h', **kwargs)
    marks = tickmarks(pts, 'h', **kwargs)

    s = r"""
    {arrow}
    {ticks}
    {marks}
    """.format(arrow = ar.content, ticks = tcks.content, marks = marks.content)
    return tikzElement(s, give_id('xaxis'))



def yaxis(y_min, y_max, **kwargs):
    ''' Draw an y-axis
    '''
    eps = set_eps(**kwargs)    
    pts = _number_range(y_min, y_max, **kwargs)

    ar = arrow(0, 0, y_min - eps, y_max + eps, **kwargs)
    tcks = ticks(pts, 'v', **kwargs)
    marks = tickmarks(pts, 'v', **kwargs)

    s = r"""
    {arrow}
    {ticks}
    {marks}
    """.format(arrow = ar.content, ticks = tcks.content, marks = marks.content)
    return tikzElement(s, give_id('yaxis'))


# TODO: this needs to be better
def grid(lower_left, upper_right, color = 'gray', step = '0.5cm', width='very thin', **kwargs):
    ''' Draw a grid
    '''
    s = "\draw[step={s}, {c}, {w}] {ll} grid {ur};".format(
            s = step,
            w = width,
            c = color,
            ll = str(lower_left),
            ur = str(upper_right)
        )

    return tikzElement(s, give_id('grid'))