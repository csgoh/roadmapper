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

# import cairo
# from colour import Color
from roadmapper.colourpalette import ColourTheme
from PIL import Image, ImageDraw, ImageFont, ImageColor


class Painter:
    """A wrapper class for PyCairo library"""

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

    # Colour scheme
    title_font: str
    title_font_size: int
    title_font_colour: str

    subtitle_font: str
    subtitle_font_size: int
    subtitle_font_colour: str

    timeline_font: str
    timeline_font_size: int
    timeline_font_colour: str
    timeline_fill_colour: str

    marker_font: str
    marker_font_size: int
    marker_font_colour: str
    marker_line_colour: str

    group_font: str
    group_font_size: int
    group_font_colour: str
    group_fill_colour: str

    task_font: str
    task_font_size: int
    task_font_colour: str
    task_fill_colour: str

    milestone_font: str
    milestone_font_size: int
    milestone_font_colour: str
    milestone_fill_colour: str

    footer_font: str
    footer_font_size: int
    footer_font_colour: str

    current_colour: str
    line_width: int
    transparency_level: int
    dash = None
    font: str
    font_size: int

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

        # if self.output_type == "PNG":
        self.__surface = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        # Future Implementation
        # if output_type == "PDF":
        #     self.__surface = cairo.PDFSurface(output_file_name, width, height)

        # self.__cr = cairo.Context(self.__surface)
        self.__cr = ImageDraw.Draw(self.__surface)

        # self.__cr.set_antialias(cairo.ANTIALIAS_NONE)

        self.__new_cr = None
        self.__new_surface = None

    def set_colour_palette(self, colour_palette: str) -> None:
        """Set colour palette

        Args:
            colour_palette (str): Name of the colour palette. Eg. OrangePeel
        """
        colour_theme = ColourTheme(colour_palette)
        self.background_colour = colour_theme.get_colour_theme_settings("background")
        (
            self.title_font,
            self.title_font_size,
            self.title_font_colour,
            self.subtitle_font,
            self.subtitle_font_size,
            self.subtitle_font_colour,
        ) = colour_theme.get_colour_theme_settings("title")
        (
            self.timeline_font,
            self.timeline_font_size,
            self.timeline_font_colour,
            self.timeline_fill_colour,
        ) = colour_theme.get_colour_theme_settings("timeline")
        (
            self.marker_font,
            self.marker_font_size,
            self.marker_font_colour,
            self.marker_line_colour,
        ) = colour_theme.get_colour_theme_settings("marker")
        (
            self.group_font,
            self.group_font_size,
            self.group_font_colour,
            self.group_fill_colour,
        ) = colour_theme.get_colour_theme_settings("group")
        (
            self.task_font,
            self.task_font_size,
            self.task_font_colour,
            self.task_fill_colour,
        ) = colour_theme.get_colour_theme_settings("task")
        (
            self.milestone_font,
            self.milestone_font_size,
            self.milestone_font_colour,
            self.milestone_fill_colour,
        ) = colour_theme.get_colour_theme_settings("milestone")
        (
            self.footer_font,
            self.footer_font_size,
            self.footer_font_colour,
        ) = colour_theme.get_colour_theme_settings("footer")

    # def XXXset_colour(self, colour: str) -> None:
    #     """Set colour

    #     Args:
    #         colour (str): HTML color code. Eg. #FFFFFF or LightGreen
    #     """
    #     # c = Color(colour)
    #     # self.__cr.set_source_rgb(*c.get_rgb())
    #     self.current_colour = colour

    # def XXXset_colour_alpha(self, colour: str) -> None:
    #     """Set colour with alpha

    #     Args:
    #         colour (str): HTML colour name or hex code. Eg. #FFFFFF or LightGreen
    #     """
    #     # c = Color(colour)
    #     # self.__cr.set_source_rgba(*c.get_rgb(), 0.5)
    #     self.transparency_level = 0.5

    # def XXXset_font(self, font: str, font_size: int, font_colour: str) -> None:
    #     """Configure text font settings

    #     Args:
    #         font (str): Font name. Eg. Arial
    #         font_size (int): Font size
    #         font_colour (str): Font colour in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
    #     """
    #     # self.set_colour(font_colour)
    #     # self.__cr.select_font_face(
    #     #     font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL
    #     # )
    #     # self.__cr.set_font_size(font_size)
    #     self.font = font
    #     self.font_size = font_size
    #     # self.__cr.text((0, 0), "", font=ImageFont.truetype(font, font_size), fill=font_colour)

    def draw_box(
        self, x: int, y: int, width: int, height: int, box_fill_colour: str
    ) -> None:
        """Draw a rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """
        shape = [(x, y), (x + width, y + height)]
        self.__cr.rectangle(shape, fill=box_fill_colour)

    def draw_box_with_text(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        box_fill_colour: str,
        text: str,
        text_alignment: str,
        text_font: str,
        text_font_size: int,
        text_font_colour: str,
    ) -> None:
        """Draw a box with text

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str): Box fill colour in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
            text (str): Text to display in the box
            text_alignment (str): Text alignment. Eg. left, center, right
            text_font (str): Text font name. Eg. Arial
            text_font_size (int): Text font size
            text_font_colour (str): Text font colour in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
        """
        # self.set_colour(text_fill_colour)
        # self.__cr.rectangle(x, y, width, height)
        self.draw_box(x, y, width, height, box_fill_colour=box_fill_colour)

        # self.set_colour(text_font_colour)
        text_x, text_y = self.get_display_text_position(
            x,
            y,
            width,
            height,
            text,
            text_alignment,
            text_font,
            text_font_size,
            text_font_colour,
        )
        self.draw_text(
            text_x, text_y, text, text_font, text_font_size, text_font_colour
        )

    def draw_diamond(
        self, x: int, y: int, width: int, height: int, fill_colour: str
    ) -> None:
        """Draw a diamond

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Diamond width
            height (int): Diamond height
            fill_colour (str): Diamond fill colour in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
        """
        # self.__cr.set_source_rgb(1, 0, 0)
        # self.__cr.move_to(x + width / 2, y)
        # self.__cr.line_to(x + width, y + height / 2)
        # self.__cr.line_to(x + width / 2, y + height)
        # self.__cr.line_to(x, y + height / 2)
        # self.__cr.close_path()
        # self.__cr.fill()

        # Calculate the coordinates of the four points of the diamond.
        points = [
            (x + width / 2, y),
            (x + width, y + height / 2),
            (x + width / 2, y + height),
            (x, y + height / 2),
        ]

        # Use Pillow's ImageDraw module to draw a polygon with the given points and fill color.
        self.__cr.polygon(points, fill=fill_colour)

    def draw_text(
        self, x: int, y: int, text: str, font: str, font_size: int, font_colour: str
    ) -> None:
        """Draw text

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            text (str): Text to draw/display
        """
        self.__cr.text(
            (x, y),
            text,
            font=ImageFont.truetype(font, font_size),
            fill=(font_colour),
        )

    # def XXXset_line_width(self, width: int) -> None:
    #     """Set line width

    #     Args:
    #         width (int): Line width
    #     """

    #     # self.__cr.set_line_width(width)
    #     self.line_width = width

    def set_line_style(self, style: str = "solid") -> None:
        """Set line style

        Args:
            style (str, optional): Line style. Defaults to "solid". Options: "solid", "dashed"
        """
        if style == "solid":
            self.dash = None
        elif style == "dashed":
            self.dash = (10.0, 5.0)
        else:
            self.dash = None
        # self.__cr.set_dash(dash)

    def draw_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        line_colour: str,
        line_transparency: int,
        line_width: int,
        line_style: str = "solid",
    ) -> None:
        """Draw a line

        Args:
            x1 (int): Line begin X coordinate
            y1 (int): Line begin Y coordinate
            x2 (int): Line end X coordinate
            y2 (int): Line end Y coordinate
            line_colour (str): Line colour in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
            line_transparency (int): Line transparency. 0 is opaque and 255 is transparent
            line_width (int): Line width
            line_style (str, optional): Line style. Defaults to "solid". Options: "solid", "dashed"
        """
        if line_style == "solid":
            dash = None
        elif line_style == "dashed":
            dash = (10.0, 5.0)
        else:
            dash = None

        r, g, b = ImageColor.getrgb(line_colour)

        self.__cr.line(
            (x1, y1, x2, y2),
            width=line_width,
            fill=(r, g, b, line_transparency),
        )

        # self.__cr.move_to(x1, y1)
        # self.__cr.line_to(x2, y2)
        # self.__cr.stroke()

    def get_text_dimension(self, text: str, font: str, font_size: int) -> tuple:
        """Get text dimension

        Args:
            text (str): Text that is used to calculate dimension

        Returns:
            (text_width (int), text_height (int)): Text dimension (width, height)
        """
        # Use Pillow's ImageFont module to get the dimensions of the text.
        image_font = ImageFont.truetype(font, font_size)
        ascent, descent = image_font.getmetrics()

        text_width = image_font.getmask(text).getbbox()[2]
        text_height = image_font.getmask(text).getbbox()[3] + descent

        return text_width, text_height

    def set_background_colour(self) -> None:
        """Set surface background colour"""
        # self.set_colour(self.background_colour)
        # self.__cr.paint()
        self.__cr.rectangle(
            (0, 0, self.width, self.height), fill=self.background_colour
        )

    def get_display_text_position(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        alignment: str,
        text_font: str,
        text_font_size: int,
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
        text_width, text_height = self.get_text_dimension(
            text, text_font, text_font_size
        )

        if alignment == "centre":
            text_x_pos = (width / 2) - (text_width / 2)
        elif alignment == "right":
            text_x_pos = width - text_width - 5
        elif alignment == "left":
            text_x_pos = 0 + 5

        text_y_pos = (height / 2) + (text_height / 2)

        return x + text_x_pos, y + text_y_pos

    def set_surface_size(self, width: int, height: int) -> None:
        """Set surface size

        Args:
            width (int): Surface width
            height (int): Surface height
        """
        height += 50
        # self.__new_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        print(f"width: {width}, height: {height}")
        self.__surface.resize((width, height))

        # self.__new_cr = cairo.Context(self.__new_surface)

        # # Copy the contents of the old surface onto the new surface
        # self.__new_cr.set_source_surface(self.__surface)
        # self.__new_cr.paint()

    def save_surface(self, filename: str) -> None:
        """Save surface to PNG file

        Args:
            filename (str): PNG file name
        """
        if self.output_type == "PNG":
            if self.__surface is not None:
                self.__surface.save(filename)
