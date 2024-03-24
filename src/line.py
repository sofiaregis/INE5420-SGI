from graphical_object import GraphicalObject
from point import Point

class Line(GraphicalObject):
    def __init__(self, x1, y1, x2, y2):
        self.start = Point(x1, y1)
        self.end = Point(x2, y2)

    def draw(self, viewport, window, cairo):
        viewport_point_start = viewport.viewport_transformation(self.start, window)
        viewport_point_end = viewport.viewport_transformation(self.end, window)
        #print("Point Start:" + str(viewport_point_start.x) + " " + str(viewport_point_start.y))
        #print("Point End:" + str(viewport_point_end.x) + " " + str(viewport_point_end.y))
        cairo.save()
        cairo.set_source_rgb(0, 0, 0)
        cairo.move_to(viewport_point_start.x, viewport_point_start.y)
        cairo.line_to(viewport_point_end.x, viewport_point_end.y)
        cairo.stroke()
        cairo.restore()

    def remove():
        pass
    