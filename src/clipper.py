from point import Point
from line import Line
from wireframe import Wireframe

class Clipper:
    def __init__(self):
        pass

    def clip(self, display_file, viewport, object):
        new_display_file = []
        for obj in display_file:
            if isinstance(obj, Point):
                new_point = self.clip_point(obj)
                if new_point:
                    new_display_file.append(new_point)
            elif isinstance(obj, Line):
                new_line = self.clip_line(obj)
                if new_line:
                    new_display_file.append(new_line)
            elif isinstance(obj, Wireframe):
                new_wireframe = self.clip_wireframe(obj)
                if new_wireframe:
                    new_display_file.append(new_wireframe)

        return new_display_file
        
    def clip_point(self, point):
        if ((point.scn_x <= 1) and (point.scn_x >= -1)) and ((point.scn_y <= 1) and (point.scn_y >= -1)):
            return point
        return None
    
    def clip_line_1(self, line):
        pass

    def clip_line_2(self, line):
        pass

    def clip_wireframe(self, wireframe):
        pass
