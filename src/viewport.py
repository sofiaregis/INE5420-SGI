from point import Point
from window import Window

class Viewport:
    def __init__(self):
        self.xvpmax = 800
        self.yvpmax = 600

    def viewport_transformation(self, point: Point, window: Window):
        new_x = ((point.x - window.x_min)/(window.x_max - window.x_min)) * (self.xvpmax)
        new_y = (1 - (point.y - window.y_min)/(window.y_max - window.y_min)) * (self.yvpmax)
        #print("Viewport Transformation: w("+str(point.x)+","+str(point.y)+") -> vp("+str(new_x)+","+str(new_y)+")")
        return Point(new_x, new_y)
