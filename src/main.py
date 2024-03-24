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
        self.windowMain = self.builder.get_object("MainWindow")
        self.windowMain.connect("destroy", Gtk.main_quit)
        self.windowMain.show_all()
        # Set create object window
        self.create_object_dialog = self.builder.get_object("CreateObjectDialog")

    def post_init(self):
        self.cairo = self.viewport_drawing_area.get_window().cairo_create()
        self.viewport_drawing_area.draw(self.cairo)

    def draw_background(self):
        pass

    #START  ----------------------------------  Create Object Popup:

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
            

        self.close_create_object(widget)

    def close_create_object(self, widget):
        self.create_object_dialog.hide()
        create_object_inputs = ["PointXInput", "PointYInput", "LineX1Input", "LineY1Input", "LineX2Input", "LineY2Input", "WireframeXInput", "WireframeYInput"]
        for i in range(len(create_object_inputs)):
            self.builder.get_object(create_object_inputs[i]).set_text("")

    #END ---------------------------------- Create Object Popup

    def on_draw(self, widget, cairo):
        #print("On Draw Called")
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
            #print(object)
            object.draw(viewport, world.window, cairo)
    
    def button_create_point(x,y):
        world.add_object(Point(x,y))

    def press_out_bt(self, widget, data=None):
        #print("Test button clicked")
        self.viewport_drawing_area.draw(self.cairo)

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    application=WindowMain()
    application.post_init()
    application.main()
