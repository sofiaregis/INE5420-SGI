from point import Point

class Window:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.x_center = (x_min + x_max) / 2
        self.y_center = (y_min + y_max) / 2
        self.viewup = Point(0, 1, self)

    def move_up(self, step):
        self.y_min += step
        self.y_max += step

    def move_down(self, step):
        self.y_min -= step
        self.y_max -= step

    def move_right(self, step):
        self.x_min += step
        self.x_max += step

    def move_left(self, step):
        self.x_min -= step
        self.x_max -= step

    def zoom_in(self, percentage):
        self.x_min /= percentage/100 + 1
        self.x_max /= percentage/100 + 1
        self.y_min /= percentage/100 + 1
        self.y_max /= percentage/100 + 1

    def zoom_out(self, percentage):
        self.x_min *= percentage/100 + 1
        self.x_max *= percentage/100 + 1
        self.y_min *= percentage/100 + 1
        self.y_max *= percentage/100 + 1
