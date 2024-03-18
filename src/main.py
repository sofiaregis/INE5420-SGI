from world import World
from viewport import Viewport

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GdkPixbuf


world = World()
viewport = Viewport()

world.display_file

class WindowMain():

    def __init__(self):
        # Get GUI Glade file
        self.builder=Gtk.Builder()
        self.builder.add_from_file("../ui/UI.glade")
        self.builder.connect_signals(self)
        self.viewport_drawing_area = self.builder.get_object("ViewportDrawingArea")
        self.cairo = self.viewport_drawing_area.get_window().cairo_create()
        # Display main window
        self.windowMain=self.builder.get_object("MainWindow")
        self.windowMain.show_all()

    def on_window_main_destroy(self, widget, data=None):
        print("on_window_main_destory")
        Gtk.main_quit()

    def button_create_point(x,y):
        world.add_object(Point(x,y))

    def press_out_bt(self, widget, data=None):
        print("Test button clicked")
        Gtk.main_quit()
    
    def main(self):
        Gtk.main()

if __name__ == "__main__":
    application=WindowMain()
    application.main()
