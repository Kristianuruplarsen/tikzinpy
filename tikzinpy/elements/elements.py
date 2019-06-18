
''' Basic building block elements for tikz code
'''
from ..tikzelement import tikzElement
from ..utils import * 

def with_options(func):
    def wrapped(cls, opts = None, *a, **kw):
        if opts is None:
            opts = ['']

        if isinstance(opts, str):
            opts = [opts]

        return func(cls, opts, *a, **kw)
    return wrapped 


class tikzCommand(tikzElement):

    def __init__(self):
        self.name = give_id('tikzCommand')
        self._string = r''

    @property
    def string(self):
        return f'{self._string[:-1]};'

    @string.setter
    def string(self, element):
        if not element[-1] == ' ':
            element = f'{element} '
        self._string += element

        
    @with_options
    def node(self, options, backslash = True):
        ''' Add a \node[options] to the drawing.
        '''
        self.string  = r'{bs}node[{opts}] '.format(
                                                opts = ', '.join(options), 
                                                bs = '\\' if backslash else ''
                                                )
        return self 

    @with_options
    def draw(self, options, backslash = True):
        ''' Add a \draw[options] to the drawing.
        '''
        self.string = r'{bs}draw[{opts}] '.format(
                                            opts = ', '.join(options),
                                            bs = '\\' if backslash else ''
                                                )
        return self

    def at(self):
        ''' Add an 'at' to the drawing.
        '''
        self.string = 'at '
        return self

    def label(self, content):
        self.string = r'{{{cont}}} '.format(cont = content)
        return self

    def dash(self):
        if self._string[-1] == '-':
            self.string = '- '
        else:
            self.string = '-'
        return self 


    def coordinate3d(self, x, y, z):
        self.string = r'({x}, {y}, {z}) '.format(x = x, y = y, z = z) 
        return self

    def coordinate2d(self, x, y):
        self.string = r'({x}, {y}) '.format(x = x, y = y) 
        return self

    def coordinate1d(self, x):
        self.string = r'({x}) '.format(x = x)
        return self


    def rawstring(self, string):
        self.string = f'{string} '
        return self

    @with_options
    def circle(self, options):
        self.rawstring('circle[{opts}] '.format(opts = ','.join(options)))
        return self

    @with_options
    def plot(self, options):
        self.string = 'plot[{opts}] '.format(opts = ', '.join(options))
        return self    
