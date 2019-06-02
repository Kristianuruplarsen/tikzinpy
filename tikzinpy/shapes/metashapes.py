import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np 

from .shapes import point
from ..tikzelement import tikzElement
from ..colors import get_cmap_and_normalizer
from ..utils import give_id

def pointswarm(X,Y, c, shape = 'fill', cmap='Spectral',alpha = 1, blowout=10, **kwargs):
    ''' Plot a swarm of points with coordinates given in X and Y.
        if c is a variable as well, the points will be colored according 
        to this variable.
    '''
    s = ""

    if type(c) == str:
        
        for x,y in zip(X,Y):
            s += point(x, y, shape, c, **kwargs)

    else:
        cmap, norm = get_cmap_and_normalizer(cmap, blowout, data = c)

        for x,y,c in zip(X, Y, c):
            r,g,b,a = cmap(norm(c), bytes = False)
            clr = 'color={{rgb:red,{r};green,{g};blue,{b}}}'.format(r=r, g=g, b=b)    
            s += point(x,y, shape = shape, color = clr, alpha = alpha).content + '\n'

    return tikzElement(s, give_id('pointswarm'))