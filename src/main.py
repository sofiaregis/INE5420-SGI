from world import World
from viewport import Viewport
from point import Point
from line import Line
from wireframe import Wireframe
from window_main import WindowMain
from transformator import Transformator

world = World()
viewport = Viewport()
main_window = WindowMain(world, viewport)

#Starting objects in the World for easier visualization
world.add_object(Wireframe([Point(100,100, world.window),Point(200,100, world.window),Point(200,200, world.window),Point(100,200, world.window)]))
world.add_object(Line(150,300,600,500, world.window))
world.add_object(Point(600,300, world.window))
world.add_object(Wireframe([Point(450,100, world.window),Point(350,350, world.window),Point(500,200, world.window)]))

if __name__ == "__main__":
    main_window.post_init()
    main_window.main()
