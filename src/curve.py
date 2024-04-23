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

    def calculate_points(self, window):
        calculated_points = []
        for i in range(0, len(self.points), 3):
            if i == len(self.points) - 1:
                break
            if i == 0:
                calculated_points.extend(self.calculate_bezier_curve(self.points[i], self.points[i+1], self.points[i+2], self.points[i+3], window))
            if i > 0:
                calculated_points.extend(self.calculate_bezier_curve(self.points[i], self.points[i+1], self.points[i+2], self.points[i+3], window)[1:])
                   
        self.curve_points = calculated_points

    def calculate_bezier_curve(self, p1, p2, p3, p4, window):
        curve_points = []

        mb = np.array(( [-1, 3, -3, 1],
						[3, -6,  3, 0],
						[-3, 3,  0, 0],
						[1,  0,  0, 0]), dtype = float)

        gbx = np.array(([float(p1.x)],
						[float(p2.x)],
						[float(p3.x)],
						[float(p4.x)]), dtype = float)

        gby = np.array(([float(p1.y)],
						[float(p2.y)],
						[float(p3.y)],
						[float(p4.y)]), dtype = float)

        curve_points.append(Point(p1.x, p1.y, window))
        
        step = 0.001
        for i in np.arange(0.0, 1.0+step, step):
            t2 = i*i
            t3 = t2*i
            mt = np.array(([t3, t2, i, 1]), dtype = float)
            mtmb = np.dot(mt, mb)
            curve_point_x = np.dot(mtmb, gbx)[0]
            curve_point_y = np.dot(mtmb, gby)[0]
            curve_points.append(Point(curve_point_x, curve_point_y, window))

        curve_points.append(Point(p4.x, p4.y, window)) 
        
        return curve_points

    def draw(self, viewport, window, cairo):
        cairo.save()
        cairo.set_source_rgb(self.color[0], self.color[1], self.color[2])
        for i in range(len(self.curve_points)):
            if (not (i == len(self.curve_points) - 1)) and (self.curve_points[i].in_window and self.curve_points[i+1].in_window):
                viewport_point_start = viewport.viewport_transformation(self.curve_points[i], window)
                viewport_point_end = viewport.viewport_transformation(self.curve_points[i+1], window)
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
