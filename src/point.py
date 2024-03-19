from graphical_object import GraphicalObject

class Point(GraphicalObject):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, viewport, window, cairo):
        viewport_point = viewport.viewport_transformation(self, window)
        print("Point:" + str(viewport_point.x) + " " + str(viewport_point.y))
        cairo.save()
        cairo.set_source_rgb(0, 0, 0)
        cairo.move_to(viewport_point.x, viewport_point.y)
        cairo.line_to(viewport_point.x+0.5, viewport_point.y+0.5)
        cairo.stroke()
        cairo.restore()

    def remove():
        pass
