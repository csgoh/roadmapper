# Painter class - Wrapper for PyCairo library
# MIT License

# Copyright (c) 2022 CS Goh

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import cairo
from colour import Color


class Painter:
    """A wrapper class for PyCairo library"""

    __VSPACER, __HSPACER = 12, 2
    width = 0
    height = 0
    last_drawn_y_pos = 0

    left_margin = 30
    right_margin = 30
    group_box_width_percentage = 0.2
    timeline_width_percentage = 1 - group_box_width_percentage
    gap_between_group_box_and_timeline = 20
    gap_between_timeline_and_title = 20

    timeline_height = 20

    # initialise code
    def __init__(self, width: int, height: int):
        """__init__ method

        Args:
            width (int): Width of the surface
            height (int): Height of the surface
        """
        self.width = width
        self.height = height
        self.last_drawn_y_pos = 0

        # Default file format
        self.output_type = "PNG"

        if self.output_type == "PNG":
            self.__surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

        # Future Implementation
        # if output_type == "PDF":
        #     self.__surface = cairo.PDFSurface(output_file_name, width, height)

        self.__cr = cairo.Context(self.__surface)

    def set_colour(self, colour: str) -> None:
        """Set colour

        Args:
            colour (str): HTML color code. Eg. #FFFFFF or LightGreen
        """
        c = Color(colour)
        self.__cr.set_source_rgb(*c.get_rgb())

    def set_colour_alpha(self, colour: str) -> None:
        """Set colour with alpha

        Args:
            colour (str): HTML colour name or hex code. Eg. #FFFFFF or LightGreen
        """
        c = Color(colour)
        self.__cr.set_source_rgba(*c.get_rgb(), 0.7)

    def set_font(self, font: str, font_size: int, font_colour: str) -> None:
        """Configure text font settings

        Args:
            font (str): Font name. Eg. Arial
            font_size (int): Font size
            font_colour (str): Font colour in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
        """
        self.__cr.select_font_face(font)
        self.__cr.set_font_size(font_size)
        self.set_colour(font_colour)

    def draw_box(self, x: int, y: int, width: int, height: int) -> None:
        """Draw a rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
        """
        self.__cr.rectangle(x, y, width, height)
        self.__cr.fill()

    def draw_box_with_text(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        text_alignment: str,
        font_colour: str,
        fill_colour: str,
    ) -> None:
        """Draw a box with text

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            text (str): Text to display in the box
            text_alignment (str): Text alignment. Eg. left, center, right
            font_colour (str): Text font colour in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
            fill_colour (str): Box fill colour in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
        """
        self.set_colour(fill_colour)
        self.__cr.rectangle(x, y, width, height)
        self.__cr.fill()
        self.set_colour(font_colour)
        text_x, text_y = self.get_display_text_position(
            x, y, width, height, text, text_alignment
        )
        self.draw_text(text_x, text_y, text)

    def draw_diamond(self, x: int, y: int, width: int, height: int) -> None:
        """Draw a diamond

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Diamond width
            height (int): Diamond height
        """
        self.__cr.set_source_rgb(1, 0, 0)
        self.__cr.move_to(x + width / 2, y)
        self.__cr.line_to(x + width, y + height / 2)
        self.__cr.line_to(x + width / 2, y + height)
        self.__cr.line_to(x, y + height / 2)
        self.__cr.close_path()
        self.__cr.fill()

    def draw_text(self, x: int, y: int, text: str) -> None:
        """Draw text

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            text (str): Text to draw/display
        """
        self.__cr.move_to(x, y)
        self.__cr.show_text(text)

    def set_line_width(self, width: int) -> None:
        """Set line width

        Args:
            width (int): Line width
        """

        self.__cr.set_line_width(width)

    def set_line_style(self, style: str = "solid") -> None:
        """Set line style

        Args:
            style (str, optional): Line style. Defaults to "solid". Options: "solid", "dashed"
        """
        if style == "solid":
            dash = [10.0, 0]
        elif style == "dashed":
            dash = [10.0, 5.0]
        else:
            dash = [10.0, 0]
        self.__cr.set_dash(dash)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Draw a line

        Args:
            x1 (int): Line begin X coordinate
            y1 (int): Line begin Y coordinate
            x2 (int): Line end X coordinate
            y2 (int): Line end Y coordinate
        """
        self.__cr.move_to(x1, y1)
        self.__cr.line_to(x2, y2)
        self.__cr.stroke()

    def get_text_dimension(self, text: str) -> tuple:
        """Get text dimension

        Args:
            text (str): Text that is used to calculate dimension

        Returns:
            (text_width (int), text_height (int)): Text dimension (width, height)
        """
        (
            _,
            _,
            text_width,
            text_height,
            _,
            _,
        ) = self.__cr.text_extents(text)
        return text_width, text_height

    def set_background_colour(self, colour: str) -> None:
        """Set surface background colour

        Args:
            colour (str): Background colour in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
        """
        self.set_colour(colour)
        self.__cr.paint()

    def get_display_text_position(
        self, x: int, y: int, width: int, height: int, text: str, alignment: str
    ) -> tuple:
        """Get text position relative to the rectangle box

        Args:
            x (int): Rectangle X coordinate
            y (int): Rectangle Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            text (str): Text used to calculate position
            alignment (str): Text alignment. Eg. left, center, right

        Returns:
            (text_x (int), text_y (int)): Text x and y coordinates
        """
        text_width, text_height = self.get_text_dimension(text)

        if alignment == "centre":
            text_x_pos = (width / 2) - (text_width / 2)
        elif alignment == "right":
            text_x_pos = width - text_width - 5
        elif alignment == "left":
            text_x_pos = 0 + 5

        text_y_pos = (height / 2) + (text_height / 2)

        return x + text_x_pos, y + text_y_pos

    def save_surface(self, filename: str) -> None:
        """Save surface to PNG file

        Args:
            filename (str): PNG file name
        """
        if self.output_type == "PNG":
            self.__surface.write_to_png(filename)
