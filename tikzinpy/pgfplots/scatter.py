
''' This sucks and should be reworked
'''

from ..tikzelement import tikzElement
from ..utils import give_id

def coordinate(x, y, group):
    return f'({str(x)}, {str(y)}) [{str(group)}]'


def coordinates_from_lists(x_vec, y_vec, groups):
    assert len(x_vec) == len(y_vec) == len(groups), "Length of inputs does not match up"

    s = r''
    for x, y, g in zip(x_vec, y_vec, groups):
        s += coordinate(x, y, g) + '\n'
    return s


def group_styles(groups, styles):
    s = []
    for g in set(groups):

        if g in styles:
            style = styles[g]
        else:
            style = 'black'

        s.append( r'{gr}={{{st}}}'.format(gr = g, st = style) )

    return ','.join(s) 


def scatterplot(x,y, groups = None, styles = None):

    if groups is None:
        groups = ['a' for _ in x]

    if styles is None:
        styles = {groups[0]: 'black'}


    coords = coordinates_from_lists(x, y, groups)
    styles = group_styles(groups, styles)

    begin = r"""
        \begin{{axis}}[scatter/classes={{
            {styles}
        }}]
    """.format(styles = styles)
    
    plot = r"""
    \addplot[scatter,only marks,scatter src=explicit symbolic]
        coordinates {{
            {coords}
            }};
    \end{{axis}}    
    """.format(coords = coords)

    return tikzElement(begin + plot, give_id('scatterplot'))