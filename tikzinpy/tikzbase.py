
import subprocess
import pathlib 

def packages(packagelist):
    return '\n'.join([r'\usepackage{{{}}}'.format(p) for p in packagelist])

class tikzBase():
    ''' The base on which we draw.
    '''

    def __init__(self):

        self._top = r"""
        \documentclass[tikz, border=2mm]{standalone}
        """
        self._preamble = dict()
        self._packages = ['tikz']

        self._begin_doc = r"""
        \begin{document}    
            \begin{tikzpicture}
        """

        self._bottom = r"""
            \end{tikzpicture}
        \end{document}
        """

        self._body = dict()

        self.saved = False 
        self.filename = None

    @property
    def body(self):
        return '\n'.join(self._body.values())
    
    
    @property 
    def preamble(self):
        return '\n'.join(self._preamble.values())

    @property
    def top(self):
        return self.top
        
    @property
    def figure(self):
        figure = self._top + packages(self._packages) + self.preamble + self._begin_doc + self.body + self._bottom
        return figure

    def add(self, tikzelement, overwrite = False):
        name = tikzelement.name
        content = tikzelement.content

        if not overwrite and name in self._body:
            raise KeyError(f"figure already contains an element with name {name}")

        self._body[name] = content
        return self

    def remove(self, name):
        del self._body[name]
        return self

    def __add__(self, tikzelement):
        return self.add(tikzelement)

    def __sub__(self, name):
        return self.remove(name)


    def add_package(self, packagename):
        self._packages.append(packagename)

    def remove_package(self, packagename):
        self._packages.remove(packagename)


    def add_to_preamble(self, name, addition):
        self._preamble[name] = addition

    def remove_from_preamble(self, name):
        del self._preamble[name]
