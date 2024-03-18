
from graphical_object import GraphicalObject

class Point(GraphicalObject):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
