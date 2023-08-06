
from .. import util, svg
from .PlotObject import PlotObject

class PlotBg(PlotObject):
    def __init__(self,x=0,y=0,w=100,h=100,fill="#f0f0f0",**kwargs):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.fill = fill
        self.kwargs = kwargs

    def toSvg(self):
        r = svg.Rect(
            self.x,self.y,
            self.w,self.h,
            **self.kwargs
            )
        r.attributes['fill'] = self.fill
        return svg.Group(a={'id':'plot-bg'},c=[r])

