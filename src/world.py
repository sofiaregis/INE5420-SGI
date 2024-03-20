from window import Window
from graphical_object import GraphicalObject

class World:
    def __init__(self):
        self.display_file = []
        self.window = Window(x_min=0, x_max=800, y_min=0, y_max=600)
    
    def add_object(self, object : GraphicalObject):
        self.display_file.append(object)