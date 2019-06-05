# Tikzinpy

This is my (unfinished) attempt at a relatively high level interface to tikz 
in python. There are some examples of what can be made in notebooks/simple_examples.ipynb.
Note the `bshow` function i use to build the figures is hard coded, and might mess up 
your filesystem. Pdf plots are stored in notebooks/test if you just want to see the output.

I try to keep the API at approximately the same level of abstraction as matplotlib or ggplot2,
for example a simple scatter plot can be made by

```python
base = tip.tikzBase(xy_ratio = '3:2')

base += tip.pointscatter(data_x, data_y, color = data_e, cmap = 'PuOr', alpha = 1)
base += tip.colors.colorbar(data_e, 'PuOr', stepsize = 0.1, width = 5,
                            height = 0.2, x = 0.5, y = -0.5, label = '$\epsilon$')
base += tip.xaxis(-2,7,0, align = 'below', labelalign='right', label = '$x$')
base += tip.yaxis(-2,5,0, align = 'left', labelalign='above', label = '$y$')
``` 