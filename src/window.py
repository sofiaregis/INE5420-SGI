
class Window:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min        
        self.x_max = x_max
        self.y_min = y_min        
        self.y_max = y_max

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
        x_size = self.x_max - self.x_min
        y_size = self.y_max - self.y_min
        new_x_size = x_size * (percentage/100)
        new_y_size = y_size * (percentage/100)
        self.x_min += new_x_size/2
        self.x_max -= new_x_size/2
        self.y_min += new_y_size/2
        self.y_max -= new_y_size/2

    def zoom_out(self, percentage):
        x_size = self.x_max - self.x_min
        y_size = self.y_max - self.y_min
        new_x_size = x_size * (percentage/100)
        new_y_size = y_size * (percentage/100)
        self.x_min -= new_x_size/2
        self.x_max += new_x_size/2
        self.y_min -= new_y_size/2
        self.y_max += new_y_size/2
