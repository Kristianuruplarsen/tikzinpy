
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np 

from ..tikzelement import tikzElement
from ..utils import give_id



def get_cmap_and_normalizer(name, blowout, data = None):
    ''' Return a colormap and a normalizer that scales the data to
        extend the whole colorspace with `blowout` percent blowout 
        in either end of the colorscale.
    '''
    cmap = plt.cm.get_cmap(name)
    if data is None:
        norm = Normalize(vmin=0, vmax=1)
    else:
        norm = Normalize(vmin=np.percentile(data, blowout), vmax=np.percentile(data, 100 - blowout))
    return cmap, norm



def build_cmap(name, data = None, blowout = 10):
    ''' Construct a pgfplots cmap that can be included in
        the preamble of a tikz figure.
    '''
    cmap, norm = get_cmap_and_normalizer(name, blowout, data)

    colors = r""
    data = np.unique(np.sort(data))

    taken = []
    for val in data:
        r,g,b,_ = map(lambda r: round(r, 4), cmap(norm(val), bytes = False))
    
        if not (r,g,b) in taken:
            colors += "rgb=({r},{g},{b})".format(r=r, g=g, b=b)
            taken.append((r,g,b))

    s = r"""
        \pgfplotsset{{
            colormap = {{{name}}}{{
                {colors}
            }}
        }}
    """.format(name = name, colors = colors)

    return tikzElement(s, give_id('cmap'))


def add_colormap(figurebase):
    pass