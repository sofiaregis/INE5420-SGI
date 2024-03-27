from graphical_object import GraphicalObject
from point import Point

class Line(GraphicalObject):
    def __init__(self, x1, y1, x2, y2):
        self.start = Point(x1, y1)
        self.end = Point(x2, y2)
        self.color = (0, 0, 0)

    def draw(self, viewport, window, cairo):
        viewport_point_start = viewport.viewport_transformation(self.start, window)
        viewport_point_end = viewport.viewport_transformation(self.end, window)
        cairo.save()
        cairo.set_source_rgb(self.color[0], self.color[1], self.color[2])
        cairo.move_to(viewport_point_start.x, viewport_point_start.y)
        cairo.line_to(viewport_point_end.x, viewport_point_end.y)
        cairo.stroke()
        cairo.restore()
    