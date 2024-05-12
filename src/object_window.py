from viewport import Viewport
from point import Point
from line import Line
from wireframe import Wireframe
from curve import Curve
from wireframe3d import Wireframe3d
from point3d import Point3d

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GdkPixbuf, cairo

class ObjectWindow:
    def __init__(self, main_window, builder, window):
        self.main_window = main_window
        self.window = window

        # Set create object window
        self.builder = builder
        self.builder.connect_signals(self)
        self.create_object_dialog = self.builder.get_object("CreateObjectDialog")

        # Set create Wireframe Treeview
        self.wireframe_points = []
        self.wireframe_points_liststore = Gtk.ListStore(int, int)
        self.wireframe_points_treeview = self.builder.get_object("WireframeTreelistPoints")
        self.wireframe_points_treeview.set_model(self.wireframe_points_liststore)
        for i, column_title in enumerate(["X", "Y"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.wireframe_points_treeview.append_column(column)

        # Set create Bezier Treeview
        self.bezier_points = []
        self.bezier_points_liststore = Gtk.ListStore(int, int)
        self.bezier_points_treeview = self.builder.get_object("BezierTreelistPoints")
        self.bezier_points_treeview.set_model(self.bezier_points_liststore)
        for i, column_title in enumerate(["X", "Y"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.bezier_points_treeview.append_column(column)

        # Set create Wireframe3d Treeview
        self.wireframe3d_ridges = []
        self.wireframe3d_points_liststore = Gtk.ListStore(int, int, int, int, int, int)
        self.wireframe3d_points_treeview = self.builder.get_object("Wireframe3dTreelistPoints")
        self.wireframe3d_points_treeview.set_model(self.wireframe3d_points_liststore)
        for i, column_title in enumerate(["X1", "Y1", "Z1", "X2", "Y2", "Z2"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.wireframe3d_points_treeview.append_column(column)
        
    def open(self, widget):
        self.create_object_dialog.show_all()

    def confirm(self, widget):
        success = False
        input = {"PointXInput":None, "PointYInput":None, "LineX1Input":None, "LineY1Input":None,
                 "LineX2Input":None, "LineY2Input":None, "WireframeXInput":None, "WireframeYInput":None,
                 "WireframeNameInput":None, "WireframeColorInput":None, "PointNameInput":None, "PointColorInput":None, 
                 "LineNameInput":None, "LineColorInput":None, "BezierXInput":None, "BezierYInput":None,
                 "BezierNameInput":None, "BezierColorInput":None, "Wireframe3d_X1_input":None, "Wireframe3d_Y1_input":None,
                 "Wireframe3d_Z1_input":None, "Wireframe3d_X2_input":None, "Wireframe3d_Y2_input":None, "Wireframe3d_Z2_input":None,
                 "Wireframe3dNameInput":None, "Wireframe3dColorInput":None}
        
        # Get all input values
        for key in input.keys():
            try:
                entry = self.builder.get_object(key).get_text()
            except AttributeError:
                if self.builder.get_object(key) != None:
                    entry = self.builder.get_object(key).get_rgba()
            if entry != "":
                try:
                    input[key] = int(entry)
                except (ValueError, TypeError):
                    input[key] = entry

        # Create new point
        if None not in [input["PointXInput"], input["PointXInput"], input["PointNameInput"], input["PointColorInput"]]:
            point = Point(input["PointXInput"], input["PointYInput"], self.window)
            point.name = input["PointNameInput"]
            point.color = (input["PointColorInput"].red, input["PointColorInput"].green, input["PointColorInput"].blue)
            point.rgb = (input["PointColorInput"].red, input["PointColorInput"].green, input["PointColorInput"].blue)
            self.main_window.world.add_object(point)
            success = True
        
        # Create new line
        elif None not in [input["LineX1Input"], input["LineY1Input"], input["LineX2Input"], input["LineY2Input"], input["LineNameInput"], input["LineColorInput"]]:
            line = Line(int(input["LineX1Input"]), int(input["LineY1Input"]), int(input["LineX2Input"]), int(input["LineY2Input"]), self.window)
            line.name = input["LineNameInput"]
            line.color = (input["LineColorInput"].red, input["LineColorInput"].green, input["LineColorInput"].blue)
            line.rgb = (input["LineColorInput"].red, input["LineColorInput"].green, input["LineColorInput"].blue)
            self.main_window.world.add_object(line)
            success = True

        # Create new wireframe
        filled = self.builder.get_object("WireframeFilledRadio").get_active()
        if len(self.wireframe_points) >= 3 and None not in [input["WireframeNameInput"], input["WireframeColorInput"]]:
            new_wireframe_points = []
            for point in self.wireframe_points:
                new_wireframe_points.append(Point(point[0], point[1], self.window))
            wireframe = Wireframe(new_wireframe_points)
            wireframe.name = input["WireframeNameInput"]
            wireframe.color = (input["WireframeColorInput"].red, input["WireframeColorInput"].green, input["WireframeColorInput"].blue)
            wireframe.rgb = (input["WireframeColorInput"].red, input["WireframeColorInput"].green, input["WireframeColorInput"].blue)
            wireframe.filled = filled
            self.main_window.world.add_object(wireframe)
            self.wireframe_points_liststore.clear()
            self.wireframe_points = []       
            success = True

        # Create new curve
        if len(self.bezier_points) >= 4 and None not in [input["BezierNameInput"], input["BezierColorInput"]]:
            is_bezier = self.builder.get_object("CurveBezierRadio").get_active()
            new_bezier_points = []
            for point in self.bezier_points:
                new_bezier_points.append(Point(point[0], point[1], self.window))
            bezier_curve = Curve(new_bezier_points)
            bezier_curve.name = input["BezierNameInput"]
            bezier_curve.color = (input["BezierColorInput"].red, input["BezierColorInput"].green, input["BezierColorInput"].blue)
            bezier_curve.rgb = (input["BezierColorInput"].red, input["BezierColorInput"].green, input["BezierColorInput"].blue)
            bezier_curve.is_bezier = is_bezier
            self.main_window.world.add_object(bezier_curve)
            self.bezier_points_liststore.clear()
            self.bezier_points = [] 
            success = True

        # Create new wireframe3d
        if len(self.wireframe3d_ridges) >= 1 and None not in [input["Wireframe3dNameInput"], input["Wireframe3dColorInput"]]:
            new_wireframe3d_ridges = []
            for ridge in self.wireframe3d_ridges:
                new_wireframe3d_ridges.append([Point3d(ridge[0], ridge[1], ridge[2], self.window), Point3d(ridge[3], ridge[4], ridge[5], self.window)])
            wireframe3d = Wireframe3d(new_wireframe3d_ridges)
            wireframe3d.name = input["Wireframe3dNameInput"]
            wireframe3d.color = (input["Wireframe3dColorInput"].red, input["Wireframe3dColorInput"].green, input["Wireframe3dColorInput"].blue)
            wireframe3d.rgb = (input["Wireframe3dColorInput"].red, input["Wireframe3dColorInput"].green, input["Wireframe3dColorInput"].blue)
            self.main_window.world.add_object(wireframe3d)
            self.wireframe3d_points_liststore.clear()
            self.wireframe3d_ridges = []       
            success = True

        if success:
            self.close(widget)
            self.main_window.create_treeview_items()
        else:
            dialog = Gtk.MessageDialog(parent=self.create_object_dialog, flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, text="Invalid input")
            dialog.run()
            dialog.destroy()

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

    def add_point_bezier(self, widget):
        x_entry = self.builder.get_object("BezierXInput")
        y_entry = self.builder.get_object("BezierYInput")
        x = x_entry.get_text()
        y = y_entry.get_text()
        if x != "" and y != "":
            self.bezier_points.append((int(x), int(y)))
            self.bezier_points_liststore.append(self.bezier_points[-1])
            x_entry.set_text("")
            y_entry.set_text("")

    def add_point_wireframe3d(self, widget):
            x1_entry = self.builder.get_object("Wireframe3d_X1_input")
            y1_entry = self.builder.get_object("Wireframe3d_Y1_input")
            z1_entry = self.builder.get_object("Wireframe3d_Z1_input")
            x2_entry = self.builder.get_object("Wireframe3d_X2_input")
            y2_entry = self.builder.get_object("Wireframe3d_Y2_input")
            z2_entry = self.builder.get_object("Wireframe3d_Z2_input")
            x1 = x1_entry.get_text()
            y1 = y1_entry.get_text()
            z1 = z1_entry.get_text()
            x2 = x2_entry.get_text()
            y2 = y2_entry.get_text()
            z2 = z2_entry.get_text()
            if "" not in [x1, y1, z1, x2, y2, z2]:
                self.wireframe3d_ridges.append([int(x1), int(y1), int(z1), int(x2), int(y2), int(z2)])
                self.wireframe3d_points_liststore.append(self.wireframe3d_ridges[-1])
                x1_entry.set_text("")
                y1_entry.set_text("")
                z1_entry.set_text("")
                x2_entry.set_text("")
                y2_entry.set_text("")
                z2_entry.set_text("")

    def close(self, widget):
        self.create_object_dialog.hide()
        create_object_inputs = ["PointXInput", "PointYInput", "LineX1Input", "LineY1Input", "LineX2Input", "LineY2Input", "WireframeXInput", "WireframeYInput"]
        for i in range(len(create_object_inputs)):
            self.builder.get_object(create_object_inputs[i]).set_text("")
        self.wireframe_points_liststore.clear()
        self.wireframe_points = []       
        self.bezier_points_liststore.clear()
        self.bezier_points = [] 
