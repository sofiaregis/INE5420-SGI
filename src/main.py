from world import World
from viewport import Viewport
from point import Point
from line import Line

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GdkPixbuf, cairo

world = World()
viewport = Viewport()
#world.add_object(Point(200, 200))
world.add_object(Line(200,200,500,500))
#world.add_object(Line(300,300,100,100))
class WindowMain():

    def __init__(self):
        # Get GUI Glade file
        self.builder=Gtk.Builder()
        self.builder.add_from_file("../ui/UI.glade")
        self.builder.connect_signals(self)
        self.viewport_drawing_area = self.builder.get_object("ViewportDrawingArea")
        # Display main window
        self.windowMain=self.builder.get_object("MainWindow")
        self.windowMain.show_all()

    def post_init(self):
        self.cairo = self.viewport_drawing_area.get_window().cairo_create()
        self.viewport_drawing_area.draw(self.cairo)

    def draw_background(self):
        pass

    #def open_create_object(self, a):
    #    self.windowMain=self.builder.get_object("CreateObjectWindow")
    #    self.windowMain.show_all()

    def on_window_main_destroy(self, widget, data=None):
        print("on_window_main_destroy")
        Gtk.main_quit()
    
    def on_draw(self, widget, cairo):
        print("On Draw Called")
        cairo.save()
        cairo.set_source_rgb(1, 1, 1)
        cairo.move_to(0, 0)
        cairo.line_to(viewport.xvpmax, 0)
        cairo.line_to(viewport.xvpmax, viewport.yvpmax)
        cairo.line_to(0, viewport.yvpmax)
        cairo.line_to(0, 0)
        cairo.fill()
        cairo.restore()
        
        for object in world.display_file:
            print(object)
            object.draw(viewport, world.window, cairo)
    
    def button_create_point(x,y):
        world.add_object(Point(x,y))

    def press_out_bt(self, widget, data=None):
        print("Test button clicked")
        #Gtk.main_quit()
        self.viewport_drawing_area.draw(self.cairo)

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    application=WindowMain()
    application.post_init()
    application.main()
