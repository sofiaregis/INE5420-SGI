from graphical_object import GraphicalObject
from point import Point

class Wireframe(GraphicalObject):
    def __init__(self, points):
        self.name = ""
        self.points = points
        self.clipped_points = []
        self.color = (0.0, 0.0, 0.0)
        self.rgb = (0.0, 0.0, 0.0)
        self.in_window = False
        self.filled = False

    def draw(self, viewport, window, cairo):
        viewport_point_start = viewport.viewport_transformation(self.points[0], window)
        cairo.save()
        cairo.set_source_rgb(self.color[0], self.color[1], self.color[2])
        for i in range(len(self.clipped_points)):
            viewport_point_start = viewport.viewport_transformation(self.clipped_points[i], window)
            if not (i == len(self.clipped_points) - 1):
                viewport_point_end = viewport.viewport_transformation(self.clipped_points[i+1], window)
                cairo.move_to(viewport_point_start.x, viewport_point_start.y)
                cairo.line_to(viewport_point_end.x, viewport_point_end.y)
                cairo.stroke()
            else:
                viewport_point_end = viewport.viewport_transformation(self.clipped_points[0], window)
                cairo.move_to(viewport_point_start.x, viewport_point_start.y)
                cairo.line_to(viewport_point_end.x, viewport_point_end.y)
                cairo.stroke()
        cairo.restore()

    def center(self):
        x_center = 0
        y_center = 0
        for point in self.points:
            x_center += point.x
            y_center += point.y
        x_center /= len(self.points)
        y_center /= len(self.points)
        return (x_center, y_center)
