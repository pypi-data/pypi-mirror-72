
def make_scale(dmin,dmax,rmin,rmax):
    dextent = dmax - dmin
    rextent = rmax - rmin
    sfactor = rextent / dextent
    def scale(n):
        return (n - dmin) * sfactor + rmin
    return scale

def extent(iterable):
    lo = hi = None
    for v in iterable:
        if lo is None and hi is None:
            lo = hi = v
        elif lo < v:
            lo = v
        elif hi > v:
            hi = v
    return lo, hi


