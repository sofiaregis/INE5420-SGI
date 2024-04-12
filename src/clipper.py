from point import Point
from line import Line
from wireframe import Wireframe

class Clipper:
    def __init__(self):
        self.margin = 0.05

    def clip(self, display_file):
        selected_algorithm = 2 #TEMPORARY
        for obj in display_file:
            if isinstance(obj, Point):
                obj.update_scn()
                self.clip_point(obj)

            elif isinstance(obj, Line):
                for point in obj.points:
                    point.update_scn()
                self.clip_line1(obj) if selected_algorithm == 1 else self.clip_line_2(obj)

            elif isinstance(obj, Wireframe):
                for point in obj.points:
                    point.update_scn()
                self.clip_wireframe(obj)
        
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
        
        print(f"Line clipped again, new points are: ({x1_clip}, {y1_clip}) and ({x2_clip}, {y2_clip}).")
        line.in_window = True
###################################################################################################

    def clip_wireframe(self, wireframe):
        wireframe.in_window = True
