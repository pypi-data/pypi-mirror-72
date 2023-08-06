

class PlotObject:
    def __init__(self,**kwargs):
        for k,v in kwargs.items():
            setattr(self,k,v)
    
    def __str__(self):
        return self.render()

    def __repr__(self):
        return "<PlotObject />"

    def toSvg(self):
        raise NotImplementedError

    def render(self):
        return self.toSvg().render()

