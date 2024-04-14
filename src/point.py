from graphical_object import GraphicalObject
import copy
import numpy as np

class Point(GraphicalObject):
    def __init__(self, x, y, window):
        self.window = window
        self.x = x
        self.y = y
        self.scn_x = 0
        self.scn_y = 0
        self.name = ""
        self.color = (0.0, 0.0, 0.0)
        self.rgb = (0.0, 0.0, 0.0)
        self.in_window = False

    def draw(self, viewport, window, cairo):
        viewport_point = viewport.viewport_transformation(self, window)
        cairo.save()
        cairo.set_source_rgb(self.color[0], self.color[1], self.color[2])
        cairo.move_to(viewport_point.x, viewport_point.y)
        cairo.line_to(viewport_point.x+0.5, viewport_point.y+0.5)
        cairo.stroke()
        cairo.restore()

    def update_scn(self):
        x = copy.deepcopy(self.x)
        y = copy.deepcopy(self.y)
        translation_vector = (-self.window.x_center, -self.window.y_center)
        result = self.move_point_xy(2, x, y, translation_vector)
        x = result[0]
        y = result[1]
        angle = self.angle_between((0,1), self.window.viewup)/(np.pi/180)
        if angle != 0:
            if self.window.viewup[0] < 0:
                angle = 360 - angle
            result = self.rotate_point_origin_xy(2, x, y, angle)
            x = result[0]
            y = result[1]
        self.scn_x = -1 + 2 * (x - (self.window.x_min - self.window.x_center)) / ((self.window.x_max - self.window.x_center) - (self.window.x_min - self.window.x_center))
        self.scn_y = -1 + 2 * (y - (self.window.y_min - self.window.y_center)) / ((self.window.y_max - self.window.y_center) - (self.window.y_min - self.window.y_center))

    def create_homogenous_matrix_xy(self, n_dimensions, x, y):
        if n_dimensions == 2:
            matrix = [x,    y,    1]
        return matrix
    
    def create_translation_matrix_tuple(self, n_dimensions, vector):
        if n_dimensions == 2:
            translation_matrix = [[1,           0,     0],
                                  [0,           1,     0],
                                  [vector[0], vector[1], 1]]
        return translation_matrix
    
    def move_point_xy(self, n_dimensions, x, y, vector):
        homogenous_matrix = self.create_homogenous_matrix_xy(n_dimensions, x, y)
        move_matrix = self.create_translation_matrix_tuple(n_dimensions, vector)
        result = self.multiply_matrix(homogenous_matrix, move_matrix)
        return (result[0], result[1])

    def create_rotate_matrix(self, n_dimensions, angle):
        if n_dimensions == 2:
            rotate_matrix = [[np.cos(angle), -np.sin(angle),  0],
                             [np.sin(angle),  np.cos(angle),  0],
                             [      0,             0,         1]]
        return rotate_matrix
    
    def rotate_point_origin_xy(self, n_dimensions, x, y, angle):
        angle *= (np.pi/180)
        if n_dimensions == 2:
            op_matrix = self.create_rotate_matrix(n_dimensions, angle)
            homogenous_point = self.create_homogenous_matrix_xy(2, x, y)
            result = self.multiply_matrix(homogenous_point, op_matrix)
            return (result[0], result[1])
    
    def multiply_matrix(self, A, B):
        if len(A) == len(B[0]):
            return np.dot(A, B)
        else:
            return None
        
    def unit_vector(self, vector):
        return vector / np.linalg.norm(vector)

    def angle_between(self, v1, v2):
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    def center(self):
        return (self.x, self.y)
