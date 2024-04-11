from viewport import Viewport
from clipper import Clipper
from point import Point
from line import Line
from wireframe import Wireframe
from object_window import ObjectWindow
from obj_descriptor import ObjDescriptor
from transformator import Transformator
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GdkPixbuf, cairo

class WindowMain():
    def __init__(self, world, viewport):
        self.world = world
        self.viewport = viewport
        self.transformator = Transformator(self.world)
        self.obj_descriptor = ObjDescriptor()

        # Get GUI Glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file("../ui/UI.glade")
        self.builder.connect_signals(self)
        self.viewport_drawing_area = self.builder.get_object("ViewportDrawingArea")
        self.step_entry = self.builder.get_object("StepEntry")
        self.object_description = self.builder.get_object("LogTextView")
    
        #Create different windows
        self.object_window = ObjectWindow(self, self.builder, self.world.window)

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
                self.world.display_file[self.selected_object_index].color = self.world.display_file[self.selected_object_index].rgb
            self.selected_object_index = index
            self.update_log(index)
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
            object_name = self.world.display_file[i].name
            self.objects_liststore.append([f"{object_name} ({object_class} {objects_dict[object_class]})"])

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

        display_file_clipped = Clipper().clip(self.world.display_file)

        for object in display_file_clipped:
            object.draw(self.viewport, self.world.window, cairo)

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
    
    def press_rotate_right_button(self, widget, data=None):
        self.world.window.rotate_right(45)
        self.viewport_drawing_area.queue_draw()

    def press_rotate_left_button(self, widget, data=None):
        self.world.window.rotate_left(45)
        self.viewport_drawing_area.queue_draw()

    def press_load_object_button(self, widget, data=None):
        dialog = Gtk.FileChooserDialog("Please choose a file", self.windowMain,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        dialog.set_current_folder(os.getcwd().replace("src", "objects"))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            print("Open clicked")
            print("File selected: " + file_path)
            self.obj_descriptor.obj_to_object(file_path, self.world)
            self.viewport_drawing_area.queue_draw()
            self.create_treeview_items()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def press_save_object_button(self, widget, data=None):
        print('save')
        dialog = Gtk.FileChooserDialog("Please choose a file", self.windowMain,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        dialog.set_current_folder(os.getcwd().replace("src", "objects"))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            print("Save clicked")
            print("File selected: " + file_path)
            if self.selected_object_index is not None:
                selected_object = self.world.display_file[self.selected_object_index]
                self.obj_descriptor.object_to_obj(selected_object, file_path)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    #Object Manipulation
    def confirm_move_object(self, widget, data=None):
        x_entry = self.builder.get_object("XMoveInput")
        y_entry = self.builder.get_object("YMoveInput")
        x = x_entry.get_text()
        y = y_entry.get_text()
        if self.selected_object_index is not None:
            selected_object = self.world.display_file[self.selected_object_index]
            if x != "" and y != "" and selected_object is not None:
                self.transformator.move_object(2, selected_object, Point(int(x), int(y), self.world.window))
                x_entry.set_text("")
                y_entry.set_text("")
                self.viewport_drawing_area.queue_draw()

    def confirm_resize_object(self, widget, data=None):
        x_entry = self.builder.get_object("XResizeInput")
        y_entry = self.builder.get_object("YResizeInput")
        x = x_entry.get_text()
        y = y_entry.get_text()
        if self.selected_object_index is not None:
            selected_object = self.world.display_file[self.selected_object_index]
            if x != "" and y != "" and selected_object is not None:
                self.transformator.scale_object(2, selected_object, Point(float(x), float(y), self.world.window))
                x_entry.set_text("")
                y_entry.set_text("")
                self.viewport_drawing_area.queue_draw()

    def confirm_rotate_object(self, widget, data=None):
        angle_entry = self.builder.get_object("AngleRotateInput")
        angle = angle_entry.get_text()
        radio_center = self.builder.get_object("CenterRadio")
        radio_world = self.builder.get_object("WorldRadio")
        radio_point = self.builder.get_object("PointRadio")
        
        if self.selected_object_index is not None:
            selected_object = self.world.display_file[self.selected_object_index]
            if angle != "" and selected_object is not None:
                if radio_center.get_active():
                    self.transformator.rotate_object_center(2, selected_object, float(angle))
                elif radio_world.get_active():
                    self.transformator.rotate_object_origin(2, selected_object, float(angle))
                elif radio_point.get_active():
                    x_entry = self.builder.get_object("XRotateInput")
                    y_entry = self.builder.get_object("YRotateInput")
                    x = x_entry.get_text()
                    y = y_entry.get_text()
                    self.transformator.rotate_object_point(2, selected_object, float(angle), Point(int(x), int(y), self.world.window))
                    x_entry.set_text("")
                    y_entry.set_text("")
                else:
                    pass         
                angle_entry.set_text("")
                self.viewport_drawing_area.queue_draw()

    def main(self):
        Gtk.main()
