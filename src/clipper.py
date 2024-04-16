from point import Point
from line import Line
from wireframe import Wireframe
from window import Window
import copy
import numpy as np

class Clipper:
    def __init__(self):
        self.margin = 0.05
        self.selected_algorithm = 1

    def clip(self, display_file, window):
        for obj in display_file:
            if isinstance(obj, Point):
                obj.update_scn()
                self.clip_point(obj)

            elif isinstance(obj, Line):
                for point in obj.points:
                    point.update_scn()
                self.clip_line1(obj) if self.selected_algorithm == 1 else self.clip_line_2(obj)

            elif isinstance(obj, Wireframe):
                for point in obj.points:
                    point.update_scn()
                self.clip_wireframe(obj, window)
        
    def clip_point(self, point):
        if ((point.scn_x <= 1) and (point.scn_x >= -1)) and ((point.scn_y <= 1) and (point.scn_y >= -1)):
            point.update_scn()
            point.in_window = True
        
    ###################################################################################################
    #COHEN-SUTHERLAND
    def clip_line1(self, line):
        x_min = y_min = -1 + self.margin
        x_max = y_max = 1 - self.margin
        x1, y1, x2, y2 = line.points[0].scn_x, line.points[0].scn_y, line.points[1].scn_x, line.points[1].scn_y
        code1 = self.compute_cohen_sutherland_code(x1, y1, x_min, x_max, y_min, y_max)
        code2 = self.compute_cohen_sutherland_code(x2, y2, x_min, x_max, y_min, y_max)
        accept = False

        while True:
            if code1 == 0 and code2 == 0:
                accept = True
                break

            elif code1 & code2 != 0:
                break
            
            else:
                x, y = 0, 0
                code_out = code1 if code1 != 0 else code2
                m = (y2 - y1) / (x2 - x1)

                if code_out & 8:
                    x = x1 + 1/m * (y_max - y1)
                    y = y_max
                elif code_out & 4:
                    x = x1 + 1/m * (y_min - y1)
                    y = y_min
                elif code_out & 2:
                    y = m * (x_max - x1) + y1
                    x = x_max
                elif code_out & 1:
                    y = m * (x_min - x1) + y1
                    x = x_min

                if code_out == code1:
                    x1, y1 = x, y
                    code1 = self.compute_cohen_sutherland_code(x1, y1, x_min, x_max, y_min, y_max)
                else:
                    x2, y2 = x, y
                    code2 = self.compute_cohen_sutherland_code(x2, y2, x_min, x_max, y_min, y_max)
        
        if accept:
            line.points[0].scn_x = x1
            line.points[0].scn_y = y1
            line.points[1].scn_x = x2
            line.points[1].scn_y = y2
            line.in_window = True

    def compute_cohen_sutherland_code(self, x, y, x_min, x_max, y_min, y_max):
        code = 0
        if x < x_min:
            code |= 1
        elif x > x_max:
            code |= 2
        if y < y_min:
            code |= 4
        elif y > y_max:
            code |= 8
        return code

    ###################################################################################################

    #LIANG-BARSKY
    def clip_line_2(self, line):
        x_min = y_min = -1 + self.margin
        x_max = y_max = 1 - self.margin
        x1, y1, x2, y2 = line.points[0].scn_x, line.points[0].scn_y, line.points[1].scn_x, line.points[1].scn_y
        dx, dy = x2 - x1, y2 - y1
        p = [-dx, dx, -dy, dy]
        q = [x1 - x_min, x_max - x1, y1 - y_min, y_max - y1]
        u1, u2 = 0, 1

        if x_min < x1 < x_max and y_min < y1 < y_max and x_min < x2 < x_max and y_min < y2 < y_max:
            line.in_window = True
            return

        for i in range(4):
            if p[i] == 0:
                if q[i] < 0:
                    break                    
            else:
                r = q[i] / p[i]
                if p[i] < 0:
                    u1 = max(u1, r)
                else:
                    u2 = min(u2, r)
        
        if u1 > u2:  # Reject the line if u1 > u2
            return
        
        # Apply Liang-Barsky clipping
        x1_clip = x1 + u1 * dx
        y1_clip = y1 + u1 * dy
        x2_clip = x1 + u2 * dx
        y2_clip = y1 + u2 * dy
        
        line.points[0].scn_x = x1_clip
        line.points[0].scn_y = y1_clip
        line.points[1].scn_x = x2_clip
        line.points[1].scn_y = y2_clip
        line.in_window = True
###################################################################################################

    #SUTHERLAND-HODGMAN
    def clip_wireframe(self, wireframe, window):
        #wireframe.in_window = True
        wireframe.clipped_points = []
        x_min = y_min = -1 + self.margin
        x_max = y_max = 1 - self.margin
        clipper_polygon = [(x_min, y_min), (x_min, y_max), (x_max, y_max), (x_max, y_min)]
        polygon_points = []
        for point in wireframe.points:
            polygon_points.append((point.scn_x, point.scn_y))
        
        for i in range(len(clipper_polygon)):
            k = (i+1) % len(clipper_polygon)
            polygon_points = self.compute_sutherland_hodgman_polygon_clip(polygon_points, clipper_polygon[i][0], clipper_polygon[i][1], clipper_polygon[k][0], clipper_polygon[k][1])
        
        if len(polygon_points) > 0:
            wireframe.in_window = True
     
        for p in polygon_points:
            clip_point = Point(0, 0, window)
            clip_point.scn_x = p[0]
            clip_point.scn_y = p[1]
            wireframe.clipped_points.append(clip_point)
        
        

    # Function to return x-value of point of intersection of two lines
    def x_intersect(self, x1, y1, x2, y2, x3, y3, x4, y4):
        num = (x1*y2 - y1*x2) * (x3-x4) - (x1-x2) * (x3*y4 - y3*x4)
        den = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)
        return num/den

    # Function to return y-value of point of intersection of two lines
    def y_intersect(self, x1, y1, x2, y2, x3, y3, x4, y4):
        num = (x1*y2 - y1*x2) * (y3-y4) - (y1-y2) * (x3*y4 - y3*x4)
        den = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)
        return num/den
    
    def compute_sutherland_hodgman_polygon_clip(self, polygon_points, x1, y1, x2, y2):
        #new_polygon_points = np.zeros((30, 2), dtype=int)
        new_polygon_points = []

        for i in range(len(polygon_points)):
            k = (i+1) % len(polygon_points)
            ix, iy = polygon_points[i]
            kx, ky = polygon_points[k]

            i_pos = (x2-x1) * (iy-y1) - (y2-y1) * (ix-x1)
            k_pos = (x2-x1) * (ky-y1) - (y2-y1) * (kx-x1)
            
            # Case 1 : When both points are inside
            if i_pos < 0 and k_pos < 0:
                # Only second point is added
                new_polygon_points.append((kx, ky))
            # Case 2: When only first point is outside
            elif i_pos >= 0 and k_pos < 0:
                # Point of intersection with edge and the second point is added
                new_polygon_points.append((self.x_intersect(x1, y1, x2, y2, ix, iy, kx, ky), self.y_intersect(x1, y1, x2, y2, ix, iy, kx, ky)))
                new_polygon_points.append((kx, ky))
            # Case 3: When only second point is outside
            elif i_pos < 0 and k_pos >= 0:
                # Only point of intersection with edge is added
                new_polygon_points.append((self.x_intersect(x1, y1, x2, y2, ix, iy, kx, ky), self.y_intersect(x1, y1, x2, y2, ix, iy, kx, ky)))
            # Case 4: When both points are outside
            else:
                pass

        return new_polygon_points

