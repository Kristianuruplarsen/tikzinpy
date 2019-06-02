
from collections import defaultdict

ID_COUNTER = defaultdict(lambda: 0)

def give_id(name):
    ''' Assign an id(name) to a tikzElement
    '''
    global ID_COUNTER
    ID_COUNTER[name] += 1
    return f'{name}{str(ID_COUNTER[name])}'


def coerce_to_strint(x):
    if x == int(x):
        return str(int(x))
    return str(x)


def drange(start, stop, step):
    ''' Range in steps
    '''
    r = start
    while r <= stop:
        yield coerce_to_strint(round(r, len(str(step))))
        r += step    
