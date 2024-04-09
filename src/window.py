import numpy as np

class Window:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.x_center = (x_min + x_max) / 2
        self.y_center = (y_min + y_max) / 2
        self.viewup = (0, 1)

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

    def unit_vector(self, vector):
        return vector / np.linalg.norm(vector)

    def rotate_right(self, angle):
        #viewup_vector = Point(self.viewup[0], self.viewup[1], self)
        #self.viewup = viewup_vector.rotate_point_origin_xy(2, self.viewup[0], self.viewup[1], angle)
        #print("Viewup: "+str(self.viewup))
        A = np.array([self.viewup[0], self.viewup[1]])
        theta = np.radians(angle)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c,-s), (s, c)))

        A = self.unit_vector(np.dot(R, A))
        self.viewup = (A[0], A[1])
        print (str(self.viewup))

    def rotate_left(self, angle):
        angle *= -1
        #viewup_vector = Point(self.viewup[0], self.viewup[1], self)
        #self.viewup = viewup_vector.rotate_point_origin_xy(2, self.viewup[0], self.viewup[1], angle)
        #print("Viewup: "+str(self.viewup))

        A = np.array([self.viewup[0], self.viewup[1]])

        theta = np.radians(angle)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c,-s), (s, c)))

        A = self.unit_vector(np.dot(R, A))
        self.viewup = (A[0], A[1])
        print (str(self.viewup))

