from window import Window
from point import Point
from graphical_object import GraphicalObject
from transformator import Transformator

class World:
    def __init__(self):
        self.display_file = []
        self.window = Window(x_min=0, x_max=800, y_min=0, y_max=600)
    
    def add_object(self, object : GraphicalObject):
        translation_vector = Point(self.window.x_center, self.window.y_center, self.window)
        Transformator(self).move_object(2, object, translation_vector)
        self.display_file.append(object)
