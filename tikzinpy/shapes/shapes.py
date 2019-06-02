
from ..tikzelement import tikzElement
from ..utils import give_id


def line(x_min, x_max, y_min, y_max, draw_opts = ['thick', 'black']):
    ''' Draw a tikz line
    '''
    dopts = ','.join(draw_opts)
    s = "\draw[{dopts}] ({x_min}, {y_min}) -- ({x_max}, {y_max});".format(
            dopts = ','.join(draw_opts),
            x_min = x_min,
            x_max = x_max,
            y_min = y_min,
            y_max = y_max
        )
    return tikzElement(s, give_id('line'))


def point(x,y, shape = 'fill', color = 'black', alpha=1, **kwargs):
    ''' Draw a single tikz point.
    '''
    if shape == 'fill':
        shape = r'\textbullet'
    elif shape == 'hollow':
        shape = r'$\circ$'

    s = r"\node[{clr}, opacity={alph}] at ({x}, {y}) {{{shp}}};".format(x=round(x,3), y=round(y,3), shp = shape, clr = color, alph=alpha)

    return tikzElement(s, give_id('point'))