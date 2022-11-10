import cairo
import math


def draw_diamond(x, y, width, height):
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 200, 200)
    cr = cairo.Context(surface)

    cr.set_source_rgb(1, 1, 1)
    cr.move_to(x + width / 2, y)
    cr.line_to(x + width, y + height / 2)
    cr.line_to(x + width / 2, y + height)
    cr.line_to(x, y + height / 2)
    cr.close_path()
    cr.fill()
    surface.write_to_png("test.png")


draw_diamond(50, 50, 50, 50)
