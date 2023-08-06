
from .. import util, svg
from .PlotTitle import PlotTitle
from .PlotAxis import PlotAxis
from .PlotInner import PlotInner
from .PlotObject import PlotObject

class PlotBase(PlotObject):
    def __init__(self,title=None,axis=None,inner=None,bg=None):
        self.title = title
        self.axis = axis
        self.inner = inner
        self.bg = bg

    def toSvg(self):
        canv = svg.SVG()
        is_valid = lambda o: (
            isinstance(o,PlotObject) or 
            isinstance(o,svg.Element)
            )
        if is_valid(self.bg):
            canv.children.append(self.bg)
        if is_valid(self.inner):
            canv.children.append(self.inner)
        if is_valid(self.axis):
            canv.children.append(self.axis)
        if is_valid(self.title):
            canv.children.append(self.title)
        return canv

    def save(self,filename,filemode="w"):
        with open(filename,filemode) as f:
            f.write(self.render())

