from point import Point
from line import Line
from wireframe import Wireframe

class ObjDescriptor:
    def __init__(self) -> None:
        pass

    def object_to_obj(self, object, file):
        f = open(file, "w")
        if isinstance(object, Point):
            f.write("Point\n")
            f.write(object.name+"\n")
            f.write(str(object.rgb[0])+", "+str(object.rgb[1])+", "+str(object.rgb[2])+"\n")
            f.write(str(object.x)+", "+str(object.y)+"\n")
            f.close()
        if isinstance(object, Line):
            f.write("Line\n")
            f.write(object.name+"\n")
            f.write(str(object.rgb[0])+", "+str(object.rgb[1])+", "+str(object.rgb[2])+"\n")
            for point in object.points:
                f.write(str(point.x)+", "+str(point.y)+"\n")
            f.close()
        if isinstance(object, Wireframe):
            f.write("Wireframe\n")
            f.write(object.name+"\n")
            f.write(str(object.rgb[0])+", "+str(object.rgb[1])+", "+str(object.rgb[2])+"\n")
            for point in object.points:
                f.write(str(point.x)+", "+str(point.y)+"\n")
            f.close()

    def obj_to_object(self, file, world):
        f = open(file, "r")
        type = f.readline().strip()
        name = f.readline().strip()
        rgb = tuple(float(x) for x in f.readline().strip().split(", "))
        if type == "Point":
            x, y = f.readline().strip().split(", ")
            point = Point(int(x), int(y), world.window)
            point.name = name
            point.color = rgb
            point.rgb = rgb
            world.add_object(point)
        elif type == "Line":
            points = []
            for line in f:
                x, y = line.strip().split(", ")
                points.append(Point(int(x), int(y), world.window))
            line = Line(points[0].x, points[0].y, points[1].x, points[1].y, world.window)
            line.name = name
            line.color = rgb
            line.rgb = rgb
            world.add_object(line)
        elif type == "Wireframe":
            points = []
            for line in f:
                x, y = line.strip().split(", ")
                points.append(Point(int(x), int(y), world.window))
            wireframe = Wireframe(points)
            wireframe.name = name
            wireframe.color = rgb
            wireframe.rgb = rgb
            world.add_object(wireframe)