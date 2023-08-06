
from .. import util, svg
from .PlotObject import PlotObject

class PlotInner(PlotObject):
    def __init__(self,xrange,yrange):
        self.xmin, self.xmax = xrange
        self.ymin, self.ymax = yrange
        

    def toSvg(self):
        raise NotImplementedError

