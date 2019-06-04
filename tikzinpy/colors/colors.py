
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np 

from ..tikzelement import tikzElement, preambleElement, packageElement
from ..utils import *


def get_cmap_and_normalizer(name, blowout, data = None):
    ''' Return a colormap and a normalizer that scales the data to
        extend the whole colorspace with `blowout` percent blowout 
        in either end of the colorscale.
    '''
    cmap = plt.cm.get_cmap(name)
    if data is None:
        norm = Normalize(vmin=0, vmax=1, clip = True)
    else:
        norm = Normalize(vmin=np.percentile(data, blowout), vmax=np.percentile(data, 100 - blowout), clip = False)        
    #    norm = Normalize(vmin=np.percentile(data, blowout), vmax=np.percentile(data, 100 - blowout))
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    return sm#cmap, norm


def check_orientation(o):
    assert o in ('horizontal', 'vertical'), f"{pos} is not a valid orientation"
    return o


class colorbar():

    def __init__(self, 
                 data, 
                 cmap = 'Spectral',
                 x = 0,
                 y = 0,
                 step = 1,
                 orientation = 'horizontal',
                 width = 10,
                 height = 1,
                 title = '',
                 label = '',
                 fontsize = 'small',
                 discrete = False,
                 nsamples = 10,
                 blowout = 5, 
                 **kwargs
    ):
        self.data = data
        self.cmap = cmap
        self.x = x
        self.y = y 
        self.step = step
        self.orientation = check_orientation(orientation)
        self.width = width
        self.height = height
        self.title = title 
        self.label = label 
        self.fontsize = fontsize
        self.discrete = discrete
        self.nsamples = nsamples
        self.blowout = 5
        self.kw = kwargs

        if self.orientation == 'horizontal':
            self.tickdir = 'x'
            self._orientation = 'horizontal'
        elif self.orientation == 'vertical':
            self.tickdir = 'y'
            self._orientation = 'right'

    @property
    def components(self):
        cmap = self._colormap()
        bar = self._colorbar()

        return [
            preambleElement(cmap.content, cmap.name),
            tikzElement(bar.content, bar.name),
            packageElement('pgfplots')
            ]

    # def clr(self, r, g, b):
    #     return 'color={{rgb:red,{r};green,{g};blue,{b}}}'.format(r=r, g=g, b=b)


    def _colormap(self):
        ''' Construct a pgfplots cmap that can be included in
            the preamble of a tikz figure.
        '''
#        cmap, norm = get_cmap_and_normalizer(self.cmap, self.blowout, self.data)
        sm = get_cmap_and_normalizer(self.cmap, self.blowout, self.data)

        colors = r""
        data = np.unique(np.sort(self.data))

        taken = []
        for val in data:
#            r,g,b,a = map(lambda r: round(r, 4), cmap(norm(val), bytes = False))
            r,g,b,a = map(lambda r: round(r, 4), sm.to_rgba(val))
            if not (r,g,b,a) in taken:
                colors += clr(r,g,b)
#                colors += "rgb=({r},{g},{b})".format(r=r, g=g, b=b)
                taken.append((r,g,b,a))

        s = r"""
            \pgfplotsset{{
                colormap = {{{name}}}{{
                    {colors}
                }}
            }}
        """.format(name = self.cmap, colors = colors)

        return preambleElement(s, give_id('cmap'))


    def _colorbar(self):
        data = np.unique(np.sort(self.data))
        
        at = f"({self.x}cm,{self.y}cm)"

        mini = np.min(data)
        maxi = np.max(data)        
        lims = list(drange(mini, maxi, self.step))

        mi, ma = lims[0], lims[-1]
        lims = ','.join(lims)

        s = r"""
        \begin{{axis}}[
            at = {{{at}}},
            hide axis,
            scale only axis,
            height=0pt,
            width=0pt, {sampled}
            colorbar {orient},
            point meta min={mi},
            point meta max={ma},
            colorbar style={{
                title = {title},
                opacity=1,
                samples={ns},
                {tdir}label = {label},
                width={w}cm,
                height={h}cm,
                {tdir}tick={{{lims}}},
                tick label style={{font=\{fs}}},
                label style={{font=\{fs}}},
                title style={{font=\{fs}}}
            }}]
            \addplot [draw=none] coordinates {{(0,0)}};
        \end{{axis}}
        """.format(lims = lims, 
                    at = at, 
                    mi = mi, 
                    ma = ma,
                    tdir = self.tickdir,
                    w = self.width,
                    h = self.height,
                    orient = self._orientation,
                    fs = self.fontsize,
                    sampled = "colorbar sampled," if self.discrete else '',
                    ns = self.nsamples,
                    title = self.title,
                    label = self.label
                    )

        return tikzElement(s, give_id('colorbar'))