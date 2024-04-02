from point import Point
from line import Line
from wireframe import Wireframe
import numpy as np

# THIS CLASSE'S METHODS DO NOT RETURN ANYTHING, THEY JUST CHANGE THE OBJECTS PASSED AS ARGUMENTS
class Transformator:
    def __init__(self):
        pass

    #Basic matrix operations
    def create_homogenous_matrix(self, n_dimensions, point):
        if n_dimensions == 2:
            matrix = [point.x,   point.y,    1]
        return matrix

    def create_translation_matrix(self, n_dimensions, vector):
        if n_dimensions == 2:
            translation_matrix = [[1,           0,     0],
                                  [0,           1,     0],
                                  [vector.x, vector.y, 1]]
        return translation_matrix

    def create_scale_matrix(self, n_dimensions, scale_vector):
        if n_dimensions == 2:
            scale_matrix = [[scale_vector.x,        0,       0],
                            [0             , scale_vector.y, 0],
                            [0             ,        0,       1]]
        return scale_matrix
    
    def create_rotate_matrix(self, n_dimensions, angle):
        if n_dimensions == 2:
            rotate_matrix = [[np.cos(angle), -np.sin(angle),  0],
                             [np.sin(angle),  np.cos(angle),  0],
                             [      0,             0,         1]]
        return rotate_matrix

    def multiply_matrix(self, A, B):
        if len(A) == len(B[0]):
            return np.dot(A, B)
        else:
            return None
    
    #Transformations for objects
    def move_point(self, n_dimensions, point, vector):
        homogenous_matrix = self.create_homogenous_matrix(n_dimensions, point)
        print(homogenous_matrix)
        move_matrix = self.create_translation_matrix(n_dimensions, vector)
        print(move_matrix)
        result = self.multiply_matrix(homogenous_matrix, move_matrix)
        print(result)
        point.x = result[0]
        point.y = result[1]
    
    #EXTERNAL METHODS move_object, scale_object, rotate_object
    def move_object(self, n_dimensions, object, vector):
        if isinstance(object, Point):
            self.move_point(n_dimensions, object, vector)
        elif isinstance(object, Line):
            self.move_point(n_dimensions, object.start, vector)
            self.move_point(n_dimensions, object.end, vector)
        elif isinstance(object, Wireframe):
            new_points = []
            for point in object.points:
                print("Before move:" +str(point.x)+ ", "+str(point.y))
                self.move_point(n_dimensions, point, vector)
                print("After move:" +str(point.x)+ ", "+str(point.y))
                new_points.append(point)
            object.points = new_points

    def scale_object(self, n_dimensions, object, scale_vector):
        if isinstance(object, Point):
            return
        else:
            if n_dimensions == 2:
                center_coord = object.center()
                take_to_center_op = self.create_translation_matrix(n_dimensions, Point(-center_coord[0], -center_coord[1]))
                scale_op = self.create_scale_matrix(n_dimensions, scale_vector)
                take_back_op = self.create_translation_matrix(n_dimensions, Point(center_coord[0], center_coord[1]))
                temp_op = self.multiply_matrix(take_to_center_op, scale_op)
                op_matrix = self.multiply_matrix(temp_op, take_back_op)
                if isinstance(object, Line):
                    homogenous_start = self.create_homogenous_matrix(2, object.start)
                    homogenous_end = self.create_homogenous_matrix(2, object.end)
                    result_start = self.multiply_matrix(homogenous_start, op_matrix)
                    result_end = self.multiply_matrix(homogenous_end, op_matrix)
                    object.start.x = result_start[0]
                    object.start.y = result_start[1]
                    object.end.x = result_end[0]
                    object.end.y = result_end[1]
                elif isinstance(object, Wireframe):
                    new_points = []
                    for point in object.points:
                        homogenous_point = self.create_homogenous_matrix(2, point)
                        result = self.multiply_matrix(homogenous_point, op_matrix)
                        point.x = result[0]
                        point.y = result[1]
                        new_points.append(point)
                    object.points = new_points

    def rotate_object(self, n_dimensions, object, angle):
        angle *= (np.pi/180)
        if isinstance(object, Point):
            return
        else:
            if n_dimensions == 2:
                center_coord = object.center()
                take_to_center_op = self.create_translation_matrix(n_dimensions, Point(-center_coord[0], -center_coord[1]))
                rotate_op = self.create_rotate_matrix(n_dimensions, angle)
                take_back_op = self.create_translation_matrix(n_dimensions, Point(center_coord[0], center_coord[1]))
                temp_op = self.multiply_matrix(take_to_center_op, rotate_op)
                op_matrix = self.multiply_matrix(temp_op, take_back_op)
                if isinstance(object, Line):
                    homogenous_start = self.create_homogenous_matrix(2, object.start)
                    homogenous_end = self.create_homogenous_matrix(2, object.end)
                    result_start = self.multiply_matrix(homogenous_start, op_matrix)
                    result_end = self.multiply_matrix(homogenous_end, op_matrix)
                    object.start.x = result_start[0]
                    object.start.y = result_start[1]
                    object.end.x = result_end[0]
                    object.end.y = result_end[1]
                elif isinstance(object, Wireframe):
                    new_points = []
                    for point in object.points:
                        homogenous_point = self.create_homogenous_matrix(2, point)
                        result = self.multiply_matrix(homogenous_point, op_matrix)
                        point.x = result[0]
                        point.y = result[1]
                        new_points.append(point)
                    object.points = new_points

    def rotate_object_center(self, n_dimensions, object, angle):
        angle *= (np.pi/180)
        if isinstance(object, Point):
            return
        else:
            if n_dimensions == 2:
                center_coord = object.center()
                take_to_center_op = self.create_translation_matrix(n_dimensions, Point(-center_coord[0], -center_coord[1]))
                rotate_op = self.create_rotate_matrix(n_dimensions, angle)
                take_back_op = self.create_translation_matrix(n_dimensions, Point(center_coord[0], center_coord[1]))
                temp_op = self.multiply_matrix(take_to_center_op, rotate_op)
                op_matrix = self.multiply_matrix(temp_op, take_back_op)
                if isinstance(object, Line):
                    homogenous_start = self.create_homogenous_matrix(2, object.start)
                    homogenous_end = self.create_homogenous_matrix(2, object.end)
                    result_start = self.multiply_matrix(homogenous_start, op_matrix)
                    result_end = self.multiply_matrix(homogenous_end, op_matrix)
                    object.start.x = result_start[0]
                    object.start.y = result_start[1]
                    object.end.x = result_end[0]
                    object.end.y = result_end[1]
                elif isinstance(object, Wireframe):
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
            return
        else:
            if n_dimensions == 2:
                op_matrix = self.create_rotate_matrix(n_dimensions, angle)
                if isinstance(object, Line):
                    homogenous_start = self.create_homogenous_matrix(2, object.start)
                    homogenous_end = self.create_homogenous_matrix(2, object.end)
                    result_start = self.multiply_matrix(homogenous_start, op_matrix)
                    result_end = self.multiply_matrix(homogenous_end, op_matrix)
                    object.start.x = result_start[0]
                    object.start.y = result_start[1]
                    object.end.x = result_end[0]
                    object.end.y = result_end[1]
                elif isinstance(object, Wireframe):
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
                take_to_center_op = self.create_translation_matrix(n_dimensions, Point(-point_coord[0], -point_coord[1]))
                rotate_op = self.create_rotate_matrix(n_dimensions, angle)
                take_back_op = self.create_translation_matrix(n_dimensions, Point(point_coord[0], point_coord[1]))
                temp_op = self.multiply_matrix(take_to_center_op, rotate_op)
                op_matrix = self.multiply_matrix(temp_op, take_back_op)
                if isinstance(object, Line):
                    homogenous_start = self.create_homogenous_matrix(2, object.start)
                    homogenous_end = self.create_homogenous_matrix(2, object.end)
                    result_start = self.multiply_matrix(homogenous_start, op_matrix)
                    result_end = self.multiply_matrix(homogenous_end, op_matrix)
                    object.start.x = result_start[0]
                    object.start.y = result_start[1]
                    object.end.x = result_end[0]
                    object.end.y = result_end[1]
                elif isinstance(object, Wireframe):
                    new_points = []
                    for point in object.points:
                        homogenous_point = self.create_homogenous_matrix(2, point)
                        result = self.multiply_matrix(homogenous_point, op_matrix)
                        point.x = result[0]
                        point.y = result[1]
                        new_points.append(point)
                    object.points = new_points               
