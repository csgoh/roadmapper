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
import textwrap


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
    gap_between_timeline_item = 3
    gap_between_timeline_group_item = 3

    additional_height_for_milestone = 15

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
        box_x: int,
        box_y: int,
        box_width: int,
        box_height: int,
        box_fill_colour: int,
        text: str,
        text_alignment: str,
        text_font: str,
        text_font_size: int,
        text_font_colour: str,
    ) -> None:
        font = ImageFont.truetype(text_font, size=text_font_size)

        multi_lines = []
        wrap_lines = []

        ### Make '\n' work
        multi_lines = text.splitlines()

        left, _, right, bottom = font.getbbox("a")
        single_char_width = right - left

        ### wrap text
        for line in multi_lines:
            wrap_lines.extend(textwrap.wrap(line, int(box_width / single_char_width)))

        box_x1, box_y1, box_x2, box_y2 = (
            box_x,
            box_y,
            box_x + box_width,
            box_y + box_height,
        )
        self.__cr.rectangle((box_x1, box_y1, box_x2, box_y2), fill=box_fill_colour)

        pad = 4
        line_count = len(wrap_lines)

        for i, line in enumerate(wrap_lines):
            font_width, font_height = self.get_text_dimension(
                line, text_font, text_font_size
            )

            match text_alignment:
                case "centre":
                    x = box_x1 + (box_width - font_width) / 2
                case "left":
                    x = box_x1 + 15
                case "right":
                    x = box_x2 - font_width - 15
                case _:
                    x = box_x1 + (box_width - font_width) / 2

            total_line_height = (font_height * line_count) + (pad * (line_count - 1))

            single_line_height = font_height

            y = (
                box_y1
                + ((box_height - total_line_height) / 2)
                + ((single_line_height * i) + (pad * i))
            )

            self.__cr.text((x, y), line, fill=text_font_colour, anchor="la", font=font)

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
            anchor="la",
            fill=(font_colour),
        )

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

    def draw_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        line_colour: str,
        line_transparency: int,
        line_width: int,
        line_style: str = "dashed",
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
        r, g, b = ImageColor.getrgb(line_colour)

        def linspace(start, stop, n):
            if n == 1:
                yield stop
                return
            h = (stop - start) / (n - 1)
            for i in range(n):
                yield start + h * i

        if line_style == "solid":
            self.__cr.line(
                (x1, y1, x2, y2),
                width=line_width,
                fill=(r, g, b, int(255 * line_transparency)),
            )
        elif line_style == "dashed":
            # given a line between x1, y1 and x2, y2, divide it into multiple shorter lines
            # and draw them with a gap in between
            for i, (x, y) in enumerate(
                zip(
                    linspace(x1, x2, 20),
                    linspace(y1, y2, 20),
                )
            ):
                if i % 2 == 0:
                    self.__cr.line(
                        (x, y, x, y + 10),
                        width=line_width,
                        fill=(r, g, b, int(255 * line_transparency)),
                    )

    def draw_cross_on_box(
        self, x1: int, y1: int, x2: int, y2: int, colour: str
    ) -> None:
        """Draw a cross (vertical and horizontal lines) on a box

        Args:
            x1 (int): x coordinate of top left corner of box
            y1 (int): y coordinate of top left corner of box
            x2 (int): x coordinate of bottom right corner of box
            y2 (int): y coordinate of bottom right corner of box
            colour (str): Colour of cross in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
        """
        self.__cr.line(
            (
                x1,
                y1 + (y2 - y1) / 2,
                x2,
                y2 - (y2 - y1) / 2,
            ),
            fill="red",
        )
        self.__cr.line((x1 + ((x2 - x1) / 2), y1, x1 + ((x2 - x1) / 2), y2), fill="red")

    def get_text_dimension(self, text: str, font: str, font_size: int) -> tuple:
        """Get text dimension

        Args:
            text (str): Text that is used to calculate dimension
            font (str): Font name
            font_size (int): Font size

        Returns:
            (text_width (int), text_height (int)): Text dimension (width, height)
        """
        # Use Pillow's ImageFont module to get the dimensions of the text.
        image_font = ImageFont.truetype(font, font_size)

        ascent, descent = image_font.getmetrics()

        left, _, right, bottom = image_font.getbbox(text)
        font_width = right
        font_height = bottom

        return font_width, font_height

    def set_background_colour(self) -> None:
        """Set surface background colour"""
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
        height += 100
        left, top, right, bottom = 0, 0, width, height
        self.__surface = self.__surface.crop((left, top, right, bottom))

    def save_surface(self, filename: str) -> None:
        """Save surface to PNG file

        Args:
            filename (str): PNG file name
        """
        if self.output_type == "PNG":
            if self.__surface is not None:
                self.__surface.save(filename)
