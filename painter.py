# Painter class - Wrapper for PyCairo library
# Copyright (C) 2022 Cheng Soon Goh
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
import cairo

# from webcolors import name_to_rgb, hex_to_rgb
from colour import Color


class Painter:
    __VSPACER, __HSPACER = 12, 2

    # initialise code
    def __init__(self, width, height, output_file_name):
        if output_file_name == "":
            output_file_name = "roadmap"

        if output_file_name.split(".")[-1].upper() == "PNG":
            output_type = "PNG"
        elif output_file_name.split(".")[-1].upper() == "PDF":
            output_type = "PDF"
        else:
            # Default file format
            output_type = "PNG"
            output_file_name.join(".png")

        if output_type == "PNG":
            self.__surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        if output_type == "PDF":
            self.__surface = cairo.PDFSurface(output_file_name, width, height)

        self.__cr = cairo.Context(self.__surface)
        self.__width = width
        self.__height = height
        self.__output_type = output_type
        self.__output_file_name = output_file_name

    def set_colour(self, colour):
        c = Color(colour)
        self.__cr.set_source_rgb(*c.get_rgb())

    def set_font(self, font, font_size, font_colour):
        self.__cr.select_font_face(font)
        self.__cr.set_font_size(font_size)
        self.set_colour(font_colour)

    def draw_box(self, x, y, width, height):
        self.__cr.rectangle(x, y, width, height)
        self.__cr.fill()

    def draw_text(self, x, y, text):
        self.__cr.move_to(x, y)
        self.__cr.show_text(text)

    def get_text_dimension(self, text):
        (
            text_x_bearing,
            text_y_bearing,
            text_width,
            text_height,
            dx,
            dy,
        ) = self.__cr.text_extents(text)
        return text_width, text_height

    def set_background_colour(self, colour):
        self.set_colour(colour)
        self.__cr.paint()

    def get_display_text_position(self, x, y, width, height, text, alignment):
        text_width, text_height = self.get_text_dimension(text)
        if alignment == "centre":
            text_x_pos = (width / 2) - (text_width / 2)
        elif alignment == "right":
            text_x_pos = width - text_width
        elif alignment == "left":
            text_x_pos = x + 10

        text_y_pos = (height / 2) + (text_height / 2)

        return x + text_x_pos, y + text_y_pos

    def save_surface(self):
        if self.__output_type == "PNG":
            self.__surface.write_to_png(self.__output_file_name)  # Output to PNG
        if self.__output_type == "PDF":
            self.__surface.show_page()
