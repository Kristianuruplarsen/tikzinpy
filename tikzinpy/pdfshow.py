
import os
import pathlib

def build(fig, path, name):

    path = pathlib.Path(path)
    if not path.exists():
        path.mkdir(parents = True, exist_ok = True)

    with open(path / f'{name}.tex', 'w') as f:
        f.write(fig)

    cmd = f"latexmk -pdf -jobname={path}/{name} {path}/{name}.tex"
    x = os.system(cmd)
    return x


class PDF(object):
    def __init__(self, pdf, size=(700,700)):
        self.pdf = pdf
        self.size = size

    def _repr_html_(self):
        return '<iframe src={0} width={1[0]} height={1[1]}></iframe>'.format(self.pdf, self.size)

    def _repr_latex_(self):
        return r'\includegraphics[width=1.0\textwidth]{{{0}}}'.format(self.pdf)