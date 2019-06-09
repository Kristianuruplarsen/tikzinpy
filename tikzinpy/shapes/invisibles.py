
from ..tikzelement import tikzElement
from ..utils import * 


class coordinate(tikzElement):

    def __init__(self, x, y, coord_id):
        self.name = give_id('coordinate')
        self.x = x
        self.y = y
        self.coord_id = coord_id 

    @property
    def content(self):
        return r"\coordinate ({c}) at ({x},{y})".format(
                                                    c=self.coord_id,
                                                    x = self.x,
                                                    y = self.y
                                                    )
