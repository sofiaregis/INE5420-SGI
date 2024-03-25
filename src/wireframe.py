from graphical_object import GraphicalObject
from point import Point

class Wireframe(GraphicalObject):
    def __init__(self, points):
        self.points = points
        self.color = (0, 0, 0)

    def draw(self, viewport, window, cairo):
        viewport_point_start = viewport.viewport_transformation(self.points[0], window)
        cairo.save()
        cairo.set_source_rgb(self.color[0], self.color[1], self.color[2])
        for i in range(len(self.points)):
            viewport_point_start = viewport.viewport_transformation(self.points[i], window)
            if not (i == len(self.points) - 1):
                viewport_point_end = viewport.viewport_transformation(self.points[i+1], window)
                cairo.move_to(viewport_point_start.x, viewport_point_start.y)
                cairo.line_to(viewport_point_end.x, viewport_point_end.y)
                cairo.stroke()
            else:
                viewport_point_end = viewport.viewport_transformation(self.points[0], window)
                cairo.move_to(viewport_point_start.x, viewport_point_start.y)
                cairo.line_to(viewport_point_end.x, viewport_point_end.y)
                cairo.stroke()
        cairo.restore()
