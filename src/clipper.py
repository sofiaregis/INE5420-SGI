from point import Point
from line import Line
from wireframe import Wireframe

class Clipper:
    def __init__(self):
        pass

    def clip(self, display_file):
        selected_algorithm = 1 #TEMPORARY
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
        window = line.points[0].window
        margin = 0.05
        x_min, x_max, y_min, y_max = -1 + margin, 1 - margin, -1 + margin, 1 - margin
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

    def clip_line_2(self, line):
        pass

    def clip_wireframe(self, wireframe):
        wireframe.in_window = True
