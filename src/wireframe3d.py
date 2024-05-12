from graphical_object import GraphicalObject
from point import Point

class Wireframe3d(GraphicalObject):
    def __init__(self, lines):
        self.name = ""
        self.lines = lines
        self.clipped_lines = []
        self.color = (0.0, 0.0, 0.0)
        self.rgb = (0.0, 0.0, 0.0)
        self.in_window = False
        self.filled = False

    # Wireframe3d has list of lines, each containing two points, representing a ridge

    def draw(self, viewport, window, cairo):
        viewport_point_start = viewport.viewport_transformation(self.points[0], window)
        cairo.save()
        cairo.set_source_rgb(self.color[0], self.color[1], self.color[2])
        for i in range(len(self.clipped_lines)):
            viewport_point_start = viewport.viewport_transformation(self.clipped_lines[i][0], window)
            if not (i == len(self.clipped_points) - 1):
                viewport_point_end = viewport.viewport_transformation(self.clipped_lines[i][1], window)
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
        z_center = 0
        for point in self.lines.values():
            x_center += point.x
            y_center += point.y
            z_center += point.z
        x_center /= len(self.points)
        y_center /= len(self.points)
        z_center /= len(self.points)
        return (x_center, y_center, z_center)
