from graphical_object import GraphicalObject
from point import Point
import numpy as np

class Curve(GraphicalObject):
    def __init__(self, points):
        self.name = ""
        self.points = points
        self.curve_points = []
        self.color = (0.0, 0.0, 0.0)
        self.rgb = (0.0, 0.0, 0.0)
        self.in_window = False

    def calculate_points(self):
        calculated_points = []
        for i in range(0, len(self.points), 3):
            if i == len(self.points) - 1:
                break
            if i == 0:
                calculated_points.extend(self.calculate_bezier_curve(self.points[i], self.points[i+1], self.points[i+2], self.points[i+3]))
            if i > 0:
                calculated_points.extend(self.calculate_bezier_curve(self.points[i], self.points[i+1], self.points[i+2], self.points[i+3])[1:])
                   
        self.curve_points = calculated_points

    def calculate_bezier_curve(self, p1, p2, p3, p4, window):
        curve_points = []

        Mb = np.array(( [-1, 3, -3, 1],
						[3, -6,  3, 0],
						[-3, 3,  0, 0],
						[1,  0,  0, 0]), dtype = float)

        Gbx = np.array(([float(p1.x)],
						[float(p2.x)],
						[float(p3.x)],
						[float(p4.x)]), dtype = float)

        Gby = np.array(([float(p1.y)],
						[float(p2.y)],
						[float(p3.y)],
						[float(p4.y)]), dtype = float)

        curve_points.append(Point(p1.x, p1.y, window))
        
        step = 0.05
        for i in np.arange(0.0, 1.0+step, step):
            t2 = i*i
            t3 = t2*i
            Mt = np.array(([t3, t2, i, 1]), dtype = float)
            MtMb = np.dot(Mt, Mb)
            curve_point_x = np.dot(MtMb, Gbx)
            curve_point_y = np.dot(MtMb, Gby)
            curve_points.append(Point(curve_point_x, curve_point_y, window))

        curve_points.append(Point(p4.x, p4.y, window)) 
        
        return curve_points

    def draw(self, viewport, window, cairo):
        pass

    def center(self):
        x_center = 0
        y_center = 0
        for point in self.points:
            x_center += point.x
            y_center += point.y
        x_center /= len(self.points)
        y_center /= len(self.points)
        return (x_center, y_center)
