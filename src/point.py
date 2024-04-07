from graphical_object import GraphicalObject

class Point(GraphicalObject):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #self.window_x
        #self.window_y
        self.color = (0, 0, 0)

    def draw(self, viewport, window, cairo):
        viewport_point = viewport.viewport_transformation(self, window)
        cairo.save()
        cairo.set_source_rgb(self.color[0], self.color[1], self.color[2])
        cairo.move_to(viewport_point.x, viewport_point.y)
        cairo.line_to(viewport_point.x+0.5, viewport_point.y+0.5)
        cairo.stroke()
        cairo.restore()

    def center(self):
        return (self.x, self.y)
