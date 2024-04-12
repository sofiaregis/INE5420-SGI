from graphical_object import GraphicalObject
from point import Point

class Line(GraphicalObject):
    def __init__(self, x1, y1, x2, y2, window):
        self.name = ""
        self.points = (Point(x1, y1, window), Point(x2, y2, window))
        self.color = (0.0, 0.0, 0.0)
        self.rgb = (0.0, 0.0, 0.0)
        self.in_window = False

    def draw(self, viewport, window, cairo):
        viewport_point_start = viewport.viewport_transformation(self.points[0], window)
        viewport_point_end = viewport.viewport_transformation(self.points[1], window)
        cairo.save()
        cairo.set_source_rgb(self.color[0], self.color[1], self.color[2])
        cairo.move_to(viewport_point_start.x, viewport_point_start.y)
        cairo.line_to(viewport_point_end.x, viewport_point_end.y)
        cairo.stroke()
        cairo.restore()
    
    def center(self):
        x_center = (self.points[0].x + self.points[1].x) / 2
        y_center = (self.points[0].x + self.points[1].y) / 2
        return (x_center, y_center)
