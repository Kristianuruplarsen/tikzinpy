
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

    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    return sm


def check_orientation(o):
    assert o in ('horizontal', 'vertical', 'h', 'v'), f"{pos} is not a valid orientation"

    if o == 'h':
        o = 'horizontal'
    if o == 'v':
        o = 'vertical'

    return o


class colorbar():
    ''' Draw a color bar on the plot.

    Arguments:
        data: array of values that should determine the color.
        cmap: Name of the matplotlib colormap to use.
        x: x-axis anchor point.
        y: y-axis anchor point.
        stepsize: Distance betweeen numbers in the colorbar.
        orientation: orientation (horizontal or vertical).
        width: width of bar.
        height: height of bar.
        title: title of bar.
        label: label of bar.
        fontsize: fontsize used for all strings.
        discrete: Should the bar be discretized?
        nsamples: number of steps to discretize into.
        blowout: the amount of points that are colored at the extreme ends
                 of the color scale.
    '''
    def __init__(self, 
                 data, 
                 cmap: str = 'Spectral',
                 x: float = 0,
                 y: float = 0,
                 stepsize: float = 1,
                 orientation: str = 'horizontal',
                 width: float = 10,
                 height: float = 1,
                 title: str = '',
                 label: str = '',
                 fontsize: str = 'small',
                 discrete: bool = False,
                 nsamples: int = 10,
                 blowout: float = 0, 
                 **kwargs
    ):
        self.data = data
        self.cmap = cmap
        self.x = x
        self.y = y 
        self.step = stepsize
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


    def _colormap(self):
        ''' Construct a pgfplots cmap that can be included in
            the preamble of a tikz figure.
        '''
        sm = get_cmap_and_normalizer(self.cmap, self.blowout, self.data)
        colors = r""
        data = np.unique(np.sort(self.data))

        taken = []
        for val in data:
            r,g,b,a = map(lambda r: round(r, 4), sm.to_rgba(val))
            if not (r,g,b,a) in taken:
                colors += self.clr(r,g,b)
                taken.append((r,g,b,a))

        s = r"""
            \pgfplotsset{{
                colormap = {{{name}}}{{
                    {colors}
                }}
            }}
        """.format(name = self.cmap, colors = colors)

        return preambleElement(s, give_id('cmap'))

    def clr(self, r, g, b):
        return "rgb=({r},{g},{b})".format(r=r,g=g,b=b)

    def _colorbar(self):

        data = np.unique(np.sort(self.data))
        at = f"({self.x}cm,{self.y}cm)"

        mini = np.min(data)
        maxi = np.max(data)
        assert maxi - mini > self.step, f"Stepsize {self.step} must be smaller than the range of data ({maxi - mini})"

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
                tick label style={{font=\{fs}, /pgf/number format/fixed}},
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