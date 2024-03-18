from point import Point
from window import Window

class Viewport:
    def __init__(self):
        self.xvpmax = 800
        self.yvpmax = 600

    def viewport_transformation(point: Point, window: Window):
        new_x = ((point.x - window.xmin)/(window.xmax - window.xmin)) * (self.xvpmax)
        new_y = (1 - (point.y - window.ymin)/(window.ymax - window.ymin)) * (self.yvpmax)
        return Point(new_x, new_y)
