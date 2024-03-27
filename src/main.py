from world import World
from viewport import Viewport
from point import Point
from line import Line
from wireframe import Wireframe
from window_main import WindowMain

world = World()
viewport = Viewport()
main_window = WindowMain(world, viewport)

world.add_object(Wireframe([Point(100,100),Point(200,100),Point(200,200),Point(100,200)]))
world.add_object(Line(150,300,600,500))
world.add_object(Point(600,300))
world.add_object(Wireframe([Point(450,100),Point(350,350),Point(500,200)]))

if __name__ == "__main__":
    main_window.post_init()
    main_window.main()
