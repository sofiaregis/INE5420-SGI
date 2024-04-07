from graphical_object import GraphicalObject
from point import Point

class Wireframe(GraphicalObject):
    def __init__(self, points):
        self.points = points
        self.color = (0, 0, 0)

    def draw(self, viewport, window, cairo):
        for point in self.points:
            point.update_scn()
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

    def center(self):
        x_center = 0
        y_center = 0
        for point in self.points:
            x_center += point.x
            y_center += point.y
        x_center /= len(self.points)
        y_center /= len(self.points)
        return (x_center, y_center)
