from point import Point
from window import Window

class Viewport:
    def __init__(self):
        self.xvpmax = 800
        self.yvpmax = 600

    def viewport_transformation(self, point: Point, window: Window):
        new_x = ((point.scn_x - -1)/(1 - -1)) * (self.xvpmax)
        new_y = (1 - (point.scn_y - -1)/(1 - -1)) * (self.yvpmax)
        return Point(new_x, new_y, window)
