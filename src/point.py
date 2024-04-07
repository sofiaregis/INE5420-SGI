from graphical_object import GraphicalObject

class Point(GraphicalObject):
    def __init__(self, x, y, window):
        self.window = window
        self.x = x
        self.y = y
        self.scn_x = -1 + 2 * (self.x - window.x_min) / (window.x_max - window.x_min)
        self.scn_y = -1 + 2 * (self.x - window.y_min) / (window.y_max - window.y_min)
        self.color = (0, 0, 0)

    def draw(self, viewport, window, cairo):
        self.update_scn()
        viewport_point = viewport.viewport_transformation(self, window)
        cairo.save()
        cairo.set_source_rgb(self.color[0], self.color[1], self.color[2])
        cairo.move_to(viewport_point.x, viewport_point.y)
        cairo.line_to(viewport_point.x+0.5, viewport_point.y+0.5)
        cairo.stroke()
        cairo.restore()

    def update_scn(self):
        self.scn_x = -1 + 2 * (self.x - self.window.x_min) / (self.window.x_max - self.window.x_min)
        self.scn_y = -1 + 2 * (self.y - self.window.y_min) / (self.window.y_max - self.window.y_min)

    def center(self):
        return (self.x, self.y)
