
import numpy as np

from ..tikzbase import tikzBase
from ..shapes import * 
from ..colors import * 
from ..utils import *

def significant_digits(x):
    n = 0
    for s in str(x):
        if not s in ('0','.'):
            break
        n += 1
    return n

def determine_stepsize(minval, maxval, steps = 5):
    x = (maxval - minval)/steps
    sigdigits = significant_digits(x)
    return round(x, sigdigits)


def vertical_barpos(x0,x1,y0,y1):
    k = 2
    h = round((y1 - y0)/k, 1)
    w = 0.05*h
    y = y1 - (k-1) * (y1 - y0) * (1/(2*k))
    x = x1 - 0.5
    return w,h,x,y

def horizontal_barpos(x0, x1, y0, y1):
    k = 2
    w = round((x1 - x0)/k, 1)
    h = 0.05*w
    x = x0 + (k-1) * (x1 - x0) * (1/(2*k))
    y = y0 - 0.5
    return w,h,x,y



def calculate_barpos(x0, x1,y0, y1, orientation):
    if orientation == 'vertical':
        return vertical_barpos(x0,x1,y0,y1)
    if orientation == 'horizontal':
        return horizontal_barpos(x0,x1,y0,y1)
    raise ValueError("Bad orientation")



def scatterplot(x, y, c = 'blue', cmap = 'PuOr', alpha = 1,
                xlabel = '', ylabel = '', fontsize = 'normalsize',
                markersize = 'normalsize', cbar_orientation = 'horizontal',
                cbar_fontsize = 'footnotesize', cbar_label = '',
                xy_ratio = '1:1', discrete = False, cbar_steps = 3
                ):
    
    x0,x1 = np.min(x), np.max(x)
    y0,y1 = np.min(y), np.max(y)

    if cbar_orientation == 'v':
        cbar_orientation = 'vertical'
    if cbar_orientation == 'h':
        cbar_orientation = 'horizontal'

    base = tikzBase(xy_ratio = xy_ratio)

    base += xaxis(x0, x1, y0, align='below', labelalign='right', tickalign='left', label = '')
    base += yaxis(y0, y1, x0, align='left', labelalign='above', tickalign='left', label = '')

    base += xaxis(x0, x1, y1, align='above', labelalign='right', tickalign='right', label = '')
    base += yaxis(y0, y1, x1, align='right', labelalign='above', tickalign='right', label = '')

    base += text(x0 + (x1-x0)/2, y0-0.5, xlabel, align = 'align=center', fontsize = fontsize)
    base += text(x0-0.5, y0 + (y1-y0)/2, ylabel, align = 'align=center', fontsize = fontsize, draw_opts=['rotate=90'])

    base += pointscatter(x, y, color = c, cmap = cmap, alpha = alpha, size = markersize)

    sts = 1
    if not isinstance(c, str):
        c0,c1 = np.min(c), np.max(c)    
        sts = determine_stepsize(c0, c1)

        barwidth, barheight, bar_x, bar_y = calculate_barpos(x0,x1,y0,y1, cbar_orientation)

        base += colorbar(c, cmap, stepsize = sts, orientation = cbar_orientation,
                            width = barwidth, height = barheight,
                            x = bar_x, y =  bar_y,
                            fontsize = cbar_fontsize, label = cbar_label, discrete=discrete, nsamples=cbar_steps)

    return base
