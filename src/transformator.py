from point import Point
from point3d import Point3d
from line import Line
from wireframe import Wireframe
from curve import Curve
import numpy as np
import math

# THIS CLASSE'S METHODS DO NOT RETURN ANYTHING, THEY JUST CHANGE THE OBJECTS PASSED AS ARGUMENTS
class Transformator:
    def __init__(self, world):
        self.window = world.window

    #Basic matrix operations
    def create_homogenous_matrix(self, n_dimensions, point):
        if n_dimensions == 2:
            matrix = [point.x,   point.y,    1]
        elif n_dimensions == 3:
            matrix = [point.x,   point.y,    point.z,    1]
        return matrix
    
    def create_homogenous_matrix_xy(self, n_dimensions, x, y):
        if n_dimensions == 2:
            matrix = [x,    y,    1]
        return matrix

    def create_translation_matrix(self, n_dimensions, vector):
        if n_dimensions == 2:
            translation_matrix = [[1,           0,     0],
                                  [0,           1,     0],
                                  [vector.x, vector.y, 1]]
        elif n_dimensions == 3:
            translation_matrix = [[1,           0,        0,     0],
                                  [0,           1,        0,     0],
                                  [0,           0,        1,     0],
                                  [vector.x, vector.y, vector.z, 1]]
        return translation_matrix

    def create_scale_matrix(self, n_dimensions, scale_vector):
        if n_dimensions == 2:
            scale_matrix = [[scale_vector.x,        0,       0],
                            [0             , scale_vector.y, 0],
                            [0             ,        0,       1]]
        elif n_dimensions == 3:
            scale_matrix = [[scale_vector.x,        0,              0,       0],
                            [0             , scale_vector.y,        0,       0],
                            [0             ,        0,       scale_vector.z, 0],
                            [0             ,        0,              0,       1]]
        return scale_matrix
    
    def create_rotate_matrix(self, n_dimensions, angle, type="z"):
        if n_dimensions == 2:
            rotate_matrix = [[np.cos(angle), -np.sin(angle),  0],
                             [np.sin(angle),  np.cos(angle),  0],
                             [      0,             0,         1]]
        elif n_dimensions == 3:
            if type == "x":
                rotate_matrix = [[1,        0,             0,         0],
                                 [0,  np.cos(angle),  np.sin(angle),  0],
                                 [0, -np.sin(angle),  np.cos(angle),  0],
                                 [0,       0,               0,        1]]
            elif type == "y":
                rotate_matrix = [[np.cos(angle),  0, -np.sin(angle),  0],
                                 [      0,        1,        0,        0],
                                 [np.sin(angle),  0,  np.cos(angle),  0],
                                 [      0,        0,        0,        1]]
            elif type == "z":
                rotate_matrix = [[ np.cos(angle),  np.sin(angle),  0,  0],
                                 [-np.sin(angle),  np.cos(angle),  0,  0],
                                 [       0,              0,        1,  0],
                                 [       0,              0,        0,  1]]
                
        return rotate_matrix 

    def multiply_matrix(self, A, B):
        if len(A) == len(B[0]):
            return np.dot(A, B)
        else:
            return None
    
    #Transformations for objects
    def move_point_xy(self, n_dimensions, x, y, vector):
        homogenous_matrix = self.create_homogenous_matrix(n_dimensions, x, y)
        move_matrix = self.create_translation_matrix(n_dimensions, vector)
        result = self.multiply_matrix(homogenous_matrix, move_matrix)
        x = result[0]
        y = result[1]

    def move_point(self, n_dimensions, point, vector):
        homogenous_matrix = self.create_homogenous_matrix(n_dimensions, point)
        move_matrix = self.create_translation_matrix(n_dimensions, vector)
        result = self.multiply_matrix(homogenous_matrix, move_matrix)
        point.x = result[0]
        point.y = result[1]
        if n_dimensions == 3:
            point.z = result[2]
    
    #EXTERNAL METHODS move_object, scale_object, rotate_object
    def move_object(self, n_dimensions, object, vector):
        if isinstance(object, Point):
            self.move_point(n_dimensions, object, vector)
        elif isinstance(object, Line) or isinstance(object, Wireframe) or isinstance(object, Curve):
            new_points = []
            for point in object.points:
                self.move_point(n_dimensions, point, vector)
                new_points.append(point)
            object.points = new_points

    def scale_object(self, n_dimensions, object, scale_vector):
        if isinstance(object, Point) or isinstance(object, Point3d):
            return
        else:
            if n_dimensions == 2:
                center_coord = object.center()
                take_to_center_op = self.create_translation_matrix(n_dimensions, Point(-center_coord[0], -center_coord[1], self.window))
                scale_op = self.create_scale_matrix(n_dimensions, scale_vector)
                take_back_op = self.create_translation_matrix(n_dimensions, Point(center_coord[0], center_coord[1], self.window))
                temp_op = self.multiply_matrix(take_to_center_op, scale_op)
                op_matrix = self.multiply_matrix(temp_op, take_back_op)
                new_points = []
                for point in object.points:
                    homogenous_point = self.create_homogenous_matrix(2, point)
                    result = self.multiply_matrix(homogenous_point, op_matrix)
                    point.x = result[0]
                    point.y = result[1]
                    new_points.append(point)
                object.points = new_points
            elif n_dimensions == 3:
                center_coord = object.center()
                take_to_center_op = self.create_translation_matrix(n_dimensions, Point(-center_coord[0], -center_coord[1], -center_coord[2]))
                scale_op = self.create_scale_matrix(n_dimensions, scale_vector)
                take_back_op = self.create_translation_matrix(n_dimensions, Point(center_coord[0], center_coord[1], center_coord[2]))
                temp_op = self.multiply_matrix(take_to_center_op, scale_op)
                op_matrix = self.multiply_matrix(temp_op, take_back_op)
                new_points = []
                for point in object.points:
                    homogenous_point = self.create_homogenous_matrix(3, point)
                    result = self.multiply_matrix(homogenous_point, op_matrix)
                    point.x = result[0]
                    point.y = result[1]
                    point.z = result[2]
                    new_points.append(point)
                object.points = new_points

    def rotate_object_center(self, n_dimensions, object, angle):
        angle *= (np.pi/180)
        if isinstance(object, Point) or isinstance(object, Point3d):
            return
        else:
            if n_dimensions == 2:
                center_coord = object.center()
                take_to_center_op = self.create_translation_matrix(n_dimensions, Point(-center_coord[0], -center_coord[1], self.window))
                rotate_op = self.create_rotate_matrix(n_dimensions, angle)
                take_back_op = self.create_translation_matrix(n_dimensions, Point(center_coord[0], center_coord[1], self.window))
                temp_op = self.multiply_matrix(take_to_center_op, rotate_op)
                op_matrix = self.multiply_matrix(temp_op, take_back_op)
                new_points = []
                for point in object.points:
                    homogenous_point = self.create_homogenous_matrix(2, point)
                    result = self.multiply_matrix(homogenous_point, op_matrix)
                    point.x = result[0]
                    point.y = result[1]
                    new_points.append(point)
                object.points = new_points

    def rotate_object_origin(self, n_dimensions, object, angle):
        angle *= (np.pi/180)
        if isinstance(object, Point):
            if n_dimensions == 2:
                op_matrix = self.create_rotate_matrix(n_dimensions, angle)
                new_points = []
                homogenous_point = self.create_homogenous_matrix(2, object)
                result = self.multiply_matrix(homogenous_point, op_matrix)
                object.x = result[0]
                object.y = result[1]
        else:
            if n_dimensions == 2:
                op_matrix = self.create_rotate_matrix(n_dimensions, angle)
                new_points = []
                for point in object.points:
                    homogenous_point = self.create_homogenous_matrix(2, point)
                    result = self.multiply_matrix(homogenous_point, op_matrix)
                    point.x = result[0]
                    point.y = result[1]
                    new_points.append(point)
                object.points = new_points

    def rotate_object_point(self, n_dimensions, object, angle, rotation_point):
        angle *= (np.pi/180)
        if isinstance(object, Point):
            return
        else:
            if n_dimensions == 2:
                point_coord = (rotation_point.x, rotation_point.y)
                take_to_center_op = self.create_translation_matrix(n_dimensions, Point(-point_coord[0], -point_coord[1], self.window))
                rotate_op = self.create_rotate_matrix(n_dimensions, angle)
                take_back_op = self.create_translation_matrix(n_dimensions, Point(point_coord[0], point_coord[1], self.window))
                temp_op = self.multiply_matrix(take_to_center_op, rotate_op)
                op_matrix = self.multiply_matrix(temp_op, take_back_op)
                new_points = []
                for point in object.points:
                    homogenous_point = self.create_homogenous_matrix(2, point)
                    result = self.multiply_matrix(homogenous_point, op_matrix)
                    point.x = result[0]
                    point.y = result[1]
                    new_points.append(point)
                object.points = new_points               

    def rotate_object_axis(self, object, angle, axis):
        # axis argument has to be a vector that goes through the center of the object
        axis = np.linalg.norm(axis)
        if isinstance(object, Point) or isinstance(object, Point3d):
            return object
        angle *= (np.pi/180)
        center_coord = object.center()
        take_to_center_op = self.create_translation_matrix(3, Point(-center_coord[0], -center_coord[1], -center_coord[2], self.window))
        angle_x = math.arcsin(abs(np.dot(np.array(axis), np.array([0,0,1])))/(axis*np.linalg.norm([0,0,1])))
        rotate_x_op = self.create_rotate_matrix(3, angle_x, type="x")
        angle_z = math.arcsin(axis[0]/axis[1])
        rotate_z_op = self.create_rotate_matrix(3, angle_z, type="z")
        rotate_op = self.create_rotate_matrix(3, angle, type="y")
        derotate_x_op = self.create_rotate_matrix(3, -angle_x, type="x")
        derotate_z_op = self.create_rotate_matrix(3, -angle_z, type="z")
        take_back_op = self.create_translation_matrix(3, Point(center_coord[0], center_coord[1], center_coord[2], self.window))
        op_matrix = np.linalg.multi_dot([take_to_center_op, rotate_x_op, rotate_z_op, rotate_op, derotate_z_op, derotate_x_op, take_back_op])
        new_points = []
        for point in object.points:
            homogenous_point = self.create_homogenous_matrix(3, point)
            result = self.multiply_matrix(homogenous_point, op_matrix)
            point.x = result[0]
            point.y = result[1]
            point.z = result[2]
            new_points.append(point)
        object.points = new_points

    def world_to_scn_coords(self, n_dimensions, point, window):
        if n_dimensions == 2:
            scn_x = (point[0] - -1) / (1 - -1) * (window.x_max)
            scn_y = (point[1] - -1) / (1 - -1) * (window.y_max)
            return (scn_x, scn_y)
