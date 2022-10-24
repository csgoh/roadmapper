import math
import cairo
# from webcolors import rgb_to_name
# from webcolors import name_to_rgb
# named_color = rgb_to_name((255,0,0), spec='css3')
# print(named_color)
 
# print(name_to_rgb("red"))
 

class RoadmapGenerator():
    def __init__(self) -> None:
        pass

    def paint(self):
        WIDTH, HEIGHT = 512, 512
 
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        cr = cairo.Context(surface)
        
        cr.set_source_rgb(255, 0, 0)
        for x in range(3):
            cr.set_source_rgb(255, 0.6*x, 0.6)
            cr.rectangle((x*WIDTH/3), 20, WIDTH/3, 40)
            cr.fill()
        
        """ Elements of roadmap
        (1) Title
        (2) Timeline
        (3) Grouping of item (4)
        (4) Tasks/Functions/Activities/Steps
        (4) Milestone
        """
        


        surface.write_to_png("example.png")  # Output to PNG



x = RoadmapGenerator()
x.paint()

