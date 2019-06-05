

class Element():
    ''' An element in a tikz plot
    Only here b.c. i might want to extend it at some point
    '''
    def __init__(self, content, name):
        self.content = content
        self.name = name

    def __call__(self, basecls):
        try:
            basecls.n_calls += 1
        except AttributeError:
            pass

        me = basecls.rescale(self)
        
        return me.content
        #return self.content
        

class tikzElement(Element):
    pass


class preambleElement(Element):
    pass


class packageElement(Element):

    def __init__(self, content):
        super().__init__(content, content)
