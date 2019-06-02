

class tikzElement():
    ''' An element in a tikz plot
    Only here b.c. i might want to extend it at some point
    '''
    def __init__(self, content, name):
        self.content = content
        self.name = name
