
from ..tikzelement import tikzElement, pgfAxisOptionElement
from ..utils import *


class pgfscatterplot(tikzElement):

    def __init__(self, x, y, group = None, xlabel = '', ylabel = ''):
        self.x = x 
        self.y = y
        self._group = group
        self.xlabel = xlabel
        self.ylabel = ylabel


    @property
    def group(self):
        if self._group is None:
            return ['a' for _ in self.x]
        return self._group


    @property
    def data(self):
        s = "x  y  group \n"
        for x,y,g in zip(self.x, self.y, self.group):
            s += f"{x}  {y}  {g} \n"
        return s

    @property
    def components(self):
        opts = [
            f'xlabel={self.xlabel}',
            f'ylabel={self.ylabel}'
        ]
        s = r"""\addplot3[only marks, blue]
            table[meta=group] {{
                {data}
            }};
             """.format(data = self.data)

        options = [pgfAxisOptionElement(o) for o in opts]
        plot = tikzElement(s, give_id('pgfscatterplot'))

        return options + [plot]



def tabledata(x,y,group, *args):
    s = "x  y  group \n"
    for x,y,g in zip(self.x, self.y, self.group, *args):
        s += f"{x}  {y}  {g} \n"
    return s


class addplot_opts(tikzElement):
    def __init__(self):
        pass 

    @property
    def content(self):
        pass


class addplot(tikzElement):
    def __init__(self):
        pass

    @property
    def content(self):
        pass