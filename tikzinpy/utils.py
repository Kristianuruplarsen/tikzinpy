
from collections import defaultdict

ID_COUNTER = defaultdict(lambda: 0)
FONTSIZES = ['Huge', 'huge', 'LARGE', 'Large', 'large', 'normalsize',
             'small', 'footnotesize', 'scriptsize', 'tiny']


def assert_valid_symbolsize(size):
    assert size in FONTSIZES, f"Size invalid. Must be one of {', '.join(FONTSIZES)}"
    return size 


def assert_valid_alpha(alpha):
    assert 0 < alpha <= 1, "Invalid alpha, must be in (0,1]"
    return alpha 


def pstr(x):
    ''' x as a string with a +/- in front
    '''
    if x < 0:
        return str(x)
    return f'+{str(x)}'


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


def drange(start, stop, step, rnd = None):
    ''' Range in steps
    '''
    if rnd is None:
        rnd = len(str(step)) - 2
    if rnd < 0:
        rnd = 0
        
    r = start
    while r <= stop:
        yield coerce_to_strint(round(r, rnd))
        r += step    


def number_range(start, stop, decimals = 0, axis_intercept = 0, remove_zero = False, **kwargs):
    ''' Return numbers from `start` to `stop` in steps 
        of 10^(-`decimal')
    '''
    points = ','.join(list(drange(start, stop, 10**(-decimals))))
    if remove_zero:
        return ','.join([x for x in points.split(',') if x != str(axis_intercept)])
    return points


def set_eps(**kwargs):
    if 'eps' in kwargs:
        return kwargs['eps']
    else:
        return 0.5


def clr(r, g, b):
    c = 100
    return 'color={{rgb:red,{r};green,{g};blue,{b}}}'.format(r=c*r/(r+g+b), g=c*g/(r+g+b), b=c*b/(r+g+b))
