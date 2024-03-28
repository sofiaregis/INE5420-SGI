from viewport import Viewport
from point import Point
from line import Line
from wireframe import Wireframe
from object_window import ObjectWindow

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GdkPixbuf, cairo

class WindowMain():
    def __init__(self, world, viewport):
        self.world = world
        self.viewport = viewport

        # Get GUI Glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file("../ui/UI.glade")
        self.builder.connect_signals(self)
        self.viewport_drawing_area = self.builder.get_object("ViewportDrawingArea")
        self.step_entry = self.builder.get_object("StepEntry")
        self.object_description = self.builder.get_object("LogTextView")
    
        #Create different windows
        self.object_window = ObjectWindow(self, self.builder)

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

    def post_init(self):
        self.cairo = self.viewport_drawing_area.get_window().cairo_create()
        self.viewport_drawing_area.draw(self.cairo)
        self.create_treeview_items()

    def open_create_object(self, widget):
        self.object_window.open(widget)

    def confirm_create_object(self, widget):
        self.object_window.confirm(widget)

    def add_point_wireframe(self, widget):
        self.object_window.add_point_wireframe(widget)

    def close_create_object(self, widget):
        self.object_window.close(widget)

    def select_object(self, widget):
        model, iters = self.objects_treeview.get_selection().get_selected()
        if iters is not None:
            index = int(str(model.get_path(iters)))
            if self.selected_object_index is not None:
                self.world.display_file[self.selected_object_index].color = (0, 0, 0)
            self.selected_object_index = index
            self.update_log(index)
            self.world.display_file[self.selected_object_index].color = (1, 0, 0)
        self.viewport_drawing_area.queue_draw()

    def delete_selected_object(self, widget):
        if self.selected_object_index is not None:
            self.world.display_file.pop(self.selected_object_index)
            self.selected_object_index = None
            self.update_log(None)
            self.viewport_drawing_area.queue_draw()
            self.create_treeview_items()

    def update_log(self, index):
        if index is not None:
            chosen_object = self.world.display_file[index]
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

    def create_treeview_items(self):
        self.objects_liststore.clear()
        objects_dict = {"Point": 0, "Line": 0, "Wireframe": 0}

        for i in range(len(self.world.display_file)):
            object_class = self.world.display_file[i].__class__.__name__
            objects_dict[object_class] += 1
            self.objects_liststore.append([f"{object_class} {objects_dict[object_class]}"])

    def on_draw(self, widget, cairo):
        cairo.save()
        cairo.set_source_rgb(1, 1, 1)
        cairo.move_to(0, 0)
        cairo.line_to(self.viewport.xvpmax, 0)
        cairo.line_to(self.viewport.xvpmax, self.viewport.yvpmax)
        cairo.line_to(0, self.viewport.yvpmax)
        cairo.line_to(0, 0)
        cairo.fill()
        cairo.restore()

        for i in range(len(self.world.display_file)):
            self.world.display_file[i].draw(self.viewport, self.world.window, cairo)

    def press_up_button(self, widget, data=None):
        step = int(self.step_entry.get_text())
        self.world.window.move_up(step)
        self.viewport_drawing_area.queue_draw()

    def press_down_button(self, widget, data=None):
        step = int(self.step_entry.get_text())
        self.world.window.move_down(step)
        self.viewport_drawing_area.queue_draw()

    def press_left_button(self, widget, data=None):
        step = int(self.step_entry.get_text())
        self.world.window.move_left(step)
        self.viewport_drawing_area.queue_draw()

    def press_right_button(self, widget, data=None):
        step = int(self.step_entry.get_text())
        self.world.window.move_right(step)
        self.viewport_drawing_area.queue_draw()

    def press_in_button(self, widget, data=None):
        percentage = int(self.step_entry.get_text())
        self.world.window.zoom_in(percentage)
        self.viewport_drawing_area.queue_draw()

    def press_out_button(self, widget, data=None):
        percentage = int(self.step_entry.get_text())
        self.world.window.zoom_out(percentage)
        self.viewport_drawing_area.queue_draw()

    def main(self):
        Gtk.main()
