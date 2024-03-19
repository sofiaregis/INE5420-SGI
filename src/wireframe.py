from graphical_object import GraphicalObject
from point import Point

class Wireframe(GraphicalObject):
    def __init__(self, points):
        self.points = points

    def draw(self, viewport, window, cairo):
        viewport_point_start = viewport.viewport_transformation(self.points[0], window)
        cairo.save()
        cairo.set_source_rgb(0, 0, 0)
        print("move_to: " + str(viewport_point_start.x) + ", " + str(viewport_point_start.y))
        cairo.move_to(viewport_point_start.x, viewport_point_start.x)
        #print("line_to: " + str(viewport_point_start.x) + ", " + str(viewport_point_start.y))
        #cairo.line_to(viewport_point_start.x, viewport_point_start.x)
        for point in self.points:
            viewport_point = viewport.viewport_transformation(point, window)
            print("line_to: " + str(viewport_point.x) + ", " + str(viewport_point.y))
            cairo.line_to(viewport_point.x, viewport_point.y)
        print("line_to: " + str(viewport_point_start.x) + ", " + str(viewport_point_start.y))
        cairo.line_to(viewport_point_start.x, viewport_point_start.y)
        cairo.stroke()
        cairo.restore()
        

    def remove():
        pass
