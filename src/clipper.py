from point import Point
from line import Line
from wireframe import Wireframe

class Clipper:
    def __init__(self)
        pass

    def clip(self, display_file, viewport, object):
        new_display_file = []
        for obj in display_file:
            if isinstance(obj, Point):
                new_display_file.append(self.clip_point(window, viewport, obj))
            elif isinstance(obj, Line):
                new_display_file.append(self.clip_line(window, viewport, obj))
            elif isinstance(obj, Wireframe):
                new_display_file.append(self.clip_wireframe(window, viewport, obj))

        return new_display_file
        
    def clip_point(self, window, viewport, point):
        pass