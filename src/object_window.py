from viewport import Viewport
from point import Point
from line import Line
from wireframe import Wireframe

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GdkPixbuf, cairo

class ObjectWindow:
    def __init__(self, main_window, builder):
        self.main_window = main_window

        # Set create object window and Wireframe Treeview
        self.builder = builder
        self.create_object_dialog = self.builder.get_object("CreateObjectDialog")
        self.wireframe_points = []
        self.wireframe_points_liststore = Gtk.ListStore(int, int)
        self.wireframe_points_treeview = self.builder.get_object("WireframeTreelistPoints")
        self.wireframe_points_treeview.set_model(self.wireframe_points_liststore)
        for i, column_title in enumerate(["X", "Y"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.wireframe_points_treeview.append_column(column)
    
    def open(self, widget):
        self.create_object_dialog.show_all()

    def create_treeview_items(self):
        self.main_window.objects_liststore.clear()
        objects_dict = {"Point": 0, "Line": 0, "Wireframe": 0}

        for i in range(len(self.main_window.world.display_file)):
            object_class = self.main_window.world.display_file[i].__class__.__name__
            objects_dict[object_class] += 1
            self.main_window.objects_liststore.append([f"{object_class} {objects_dict[object_class]}"])

    def confirm(self, widget):
        input = {"PointXInput":None, "PointYInput":None, "LineX1Input":None, "LineY1Input":None,
                 "LineX2Input":None, "LineY2Input":None, "WireframeXInput":None, "WireframeYInput":None}
        
        # Get all input values
        for key in input.keys():
            entry = self.builder.get_object(key).get_text()
            if entry != "":
                input[key] = int(entry)

        # Create new point
        if None not in [input["PointXInput"], input["PointXInput"]]:
            self.main_window.world.display_file.append(Point(input["PointXInput"], input["PointYInput"]))
        
        # Create new line
        elif None not in [input["LineX1Input"], input["LineY1Input"], input["LineX2Input"], input["LineY2Input"]]:
            self.main_window.world.display_file.append(Line(int(input["LineX1Input"]), int(input["LineY1Input"]), int(input["LineX2Input"]), int(input["LineY2Input"])))

        # Create new wireframe
        if self.wireframe_points != []:
            new_wireframe_points = []
            for point in self.wireframe_points:
                new_wireframe_points.append(Point(point[0], point[1]))
            self.main_window.world.display_file.append(Wireframe(new_wireframe_points))
            self.wireframe_points_liststore.clear()
            self.wireframe_points = []
        self.close(widget)
        self.create_treeview_items()

    def add_point_wireframe(self, widget):
        x_entry = self.builder.get_object("WireframeXInput")
        y_entry = self.builder.get_object("WireframeYInput")
        x = x_entry.get_text()
        y = y_entry.get_text()
        if x != "" and y != "":
            self.wireframe_points.append((int(x), int(y)))
            self.wireframe_points_liststore.append(self.wireframe_points[-1])
            x_entry.set_text("")
            y_entry.set_text("")

    def close(self, widget):
        self.create_object_dialog.hide()
        create_object_inputs = ["PointXInput", "PointYInput", "LineX1Input", "LineY1Input", "LineX2Input", "LineY2Input", "WireframeXInput", "WireframeYInput"]
        for i in range(len(create_object_inputs)):
            self.builder.get_object(create_object_inputs[i]).set_text("")