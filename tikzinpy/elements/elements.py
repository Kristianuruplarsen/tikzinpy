
''' Basic building block elements for tikz code
'''

class tikzCommand():

    def __init__(self):
        self._string = r''

    @property
    def string(self):
        return f'{self._string};'

    def node(self, options):

        if isinstance(options, str):
            options = [options]

        self._string  += r'\node[{opts}] '.format(opts = ', '.join(options))
        return self 

    def draw(self, options):

        if isinstance(options, str):
            options = [options]

        self._string += r'\draw[{opts}] '.format(opts = ', '.join(options))
        return self

    def at(self):
        self._string += 'at '
        return self

    def label(self, content):
        self._string += r'{{{cont}}} '.format(cont = content)
        return self

    def dash(self):
        if self._string[-1] == '-':
            self._string += '- '
        else:
            self._string += ' -'
        return self 

    def coordinate2d(self, x, y):
        self._string += r'({x}, {y}) '.format(x = x, y = y) 
        return self

    def coordinate1d(self, x):
        self._string += r'({x})'.format(x = x)
        return self

    def circle(self):
        self._string += r'circle '
        return self
    
