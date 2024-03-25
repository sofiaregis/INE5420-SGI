from world import World
from viewport import Viewport
from point import Point
from line import Line
from wireframe import Wireframe

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GdkPixbuf, cairo

world = World()
viewport = Viewport()

world.add_object(Wireframe([Point(100,100),Point(200,100),Point(200,200),Point(100,200)]))
world.add_object(Line(150,300,600,500))
world.add_object(Point(600,300))
world.add_object(Wireframe([Point(450,100),Point(350,350),Point(500,200)]))


class WindowMain():

    def __init__(self):
        # Get GUI Glade file
        self.builder=Gtk.Builder()
        self.builder.add_from_file("../ui/UI.glade")
        self.builder.connect_signals(self)
        self.viewport_drawing_area = self.builder.get_object("ViewportDrawingArea")
        self.step_entry = self.builder.get_object("StepEntry")
        self.object_description = self.builder.get_object("LogTextView")

    
        # Display main window
        self.windowMain = self.builder.get_object("MainWindow")
        self.windowMain.connect("destroy", Gtk.main_quit)
        self.windowMain.show_all()
    
        # Set up the Treeview for objects
        self.objects_liststore = Gtk.ListStore(str)
        self.objects_treeview = self.builder.get_object("ObjectTreeView")
        self.objects_treeview.set_model(self.objects_liststore)
        for i, column_title in enumerate(["Object Name"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.objects_treeview.append_column(column)
        self.selected_object_index = None

        # Set create object window and Wireframe Treeview
        self.create_object_dialog = self.builder.get_object("CreateObjectDialog")
        self.wireframe_points = []
        self.wireframe_points_liststore = Gtk.ListStore(int, int)
        self.wireframe_points_treeview = self.builder.get_object("WireframeTreelistPoints")
        self.wireframe_points_treeview.set_model(self.wireframe_points_liststore)
        for i, column_title in enumerate(["X", "Y"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.wireframe_points_treeview.append_column(column)

    def post_init(self):
        self.cairo = self.viewport_drawing_area.get_window().cairo_create()
        self.viewport_drawing_area.draw(self.cairo)
        self.create_treeview_items()

    #START  ----------------------------------  Create Object Popup:

    def create_treeview_items(self):
        self.objects_liststore.clear()
        objects_dict = {"Point": 0, "Line": 0, "Wireframe": 0}

        for i in range(len(world.display_file)):
            object_class = world.display_file[i].__class__.__name__
            objects_dict[object_class] += 1
            self.objects_liststore.append([f"{object_class} {objects_dict[object_class]}"])

    
    def open_create_object(self, widget):
        self.create_object_dialog.show_all()

    def confirm_create_object(self, widget):
        input = {"PointXInput":None, "PointYInput":None, "LineX1Input":None, "LineY1Input":None,
                 "LineX2Input":None, "LineY2Input":None, "WireframeXInput":None, "WireframeYInput":None}
        
        # Get all input values
        for key in input.keys():
            entry = self.builder.get_object(key).get_text()
            if entry != "":
                input[key] = int(entry)

        # Create new point
        if None not in [input["PointXInput"], input["PointXInput"]]:
            world.display_file.append(Point(input["PointXInput"], input["PointYInput"]))
        
        # Create new line
        elif None not in [input["LineX1Input"], input["LineY1Input"], input["LineX2Input"], input["LineY2Input"]]:
            world.display_file.append(Line(int(input["LineX1Input"]), int(input["LineY1Input"]), int(input["LineX2Input"]), int(input["LineY2Input"])))

        # Create new wireframe
        if self.wireframe_points != []:
            new_wireframe_points = []
            for point in self.wireframe_points:
                new_wireframe_points.append(Point(point[0], point[1]))
            world.display_file.append(Wireframe(new_wireframe_points))
            self.wireframe_points_liststore.clear()
            self.wireframe_points = []
        self.close_create_object(widget)
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

    def close_create_object(self, widget):
        self.create_object_dialog.hide()
        create_object_inputs = ["PointXInput", "PointYInput", "LineX1Input", "LineY1Input", "LineX2Input", "LineY2Input", "WireframeXInput", "WireframeYInput"]
        for i in range(len(create_object_inputs)):
            self.builder.get_object(create_object_inputs[i]).set_text("")

    #END ---------------------------------- Create Object Popup

    def select_object(self, widget):
        model, iters = self.objects_treeview.get_selection().get_selected()
        if iters is not None:
            index = int(str(model.get_path(iters)))
            if self.selected_object_index is not None:
                world.display_file[self.selected_object_index].color = (0, 0, 0)
            self.selected_object_index = index
            self.update_log(index)
            world.display_file[self.selected_object_index].color = (1, 0, 0)
        self.viewport_drawing_area.queue_draw()

    def delete_selected_object(self, widget):
        if self.selected_object_index is not None:
            world.display_file.pop(self.selected_object_index)
            self.selected_object_index = None
            self.update_log(None)
            self.on_draw(self.viewport_drawing_area, self.cairo)
            self.create_treeview_items()

    def update_log(self, index):
        if index is not None:
            chosen_object = world.display_file[index]
            if isinstance(chosen_object, Point):
                locations = [(chosen_object.x, chosen_object.y)]
            elif isinstance(chosen_object, Line):
                locations = [(chosen_object.start.x, chosen_object.start.y), (chosen_object.end.x, chosen_object.end.y)]
            else:
                locations = []
                for point in chosen_object.points:
                    locations.append((point.x, point.y))

            object_type = chosen_object.__class__.__name__

            self.object_description.get_buffer().set_text(f"{object_type} \nPOINTS: {locations}")
        else:
            self.object_description.get_buffer().set_text("")


    def on_draw(self, widget, cairo):
        cairo.save()
        cairo.set_source_rgb(1, 1, 1)
        cairo.move_to(0, 0)
        cairo.line_to(viewport.xvpmax, 0)
        cairo.line_to(viewport.xvpmax, viewport.yvpmax)
        cairo.line_to(0, viewport.yvpmax)
        cairo.line_to(0, 0)
        cairo.fill()
        cairo.restore()

        for i in range(len(world.display_file)):
            world.display_file[i].draw(viewport, world.window, cairo)
    
    def button_create_point(x,y):
        world.add_object(Point(x,y))

    def press_up_button(self, widget, data=None):
        step = int(self.step_entry.get_text())
        world.window.move_up(step)
        self.viewport_drawing_area.queue_draw()
    
    def press_down_button(self, widget, data=None):
        step = int(self.step_entry.get_text())
        world.window.move_down(step)
        self.viewport_drawing_area.queue_draw()

    def press_left_button(self, widget, data=None):
        step = int(self.step_entry.get_text())
        world.window.move_left(step)
        self.viewport_drawing_area.queue_draw()
    
    def press_right_button(self, widget, data=None):
        step = int(self.step_entry.get_text())
        world.window.move_right(step)
        self.viewport_drawing_area.queue_draw()

    def press_in_button(self, widget, data=None):
        percentage = int(self.step_entry.get_text())
        world.window.zoom_in(percentage)
        self.viewport_drawing_area.queue_draw()
    
    def press_out_button(self, widget, data=None):
        percentage = int(self.step_entry.get_text())
        world.window.zoom_out(percentage)
        self.viewport_drawing_area.queue_draw()


    def main(self):
        Gtk.main()

if __name__ == "__main__":
    application=WindowMain()
    application.post_init()
    application.main()
