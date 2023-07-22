# Painter class - Wrapper for Pillow library
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

import os
import sys
from .colourtheme import ColourTheme
from PIL import Image, ImageDraw, ImageFont, ImageColor
import drawsvg as dw

import textwrap


class UnsupportedOSException(Exception):
    pass


class Painter:
    width = 0
    height = 0
    next_y_pos = 0

    top_margin = 30
    bottom_margin = 30
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

    timeline_year_font: str
    timeline_year_font_size: int
    timeline_year_font_colour: str
    timeline_year_fill_colour: str

    timeline_item_font: str
    timeline_item_font_size: int
    timeline_item_font_colour: str
    timeline_item_fill_colour: str

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
    task_style: str

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

    def __init__(self, width: int, height: int):
        """__init__ method

        Args:
            width (int): Width of the surface
            height (int): Height of the surface
        """
        self.width = width
        self.height = height
        self.next_y_pos = 0

    def set_colour_theme(self, colour_theme: str) -> None:
        """Set colour palette

        Args:
            colour_palette (str): Name of the colour palette. Eg. OrangePeel
        """
        self.colour_theme = ColourTheme(colour_theme)
        (self.background_colour,) = self.colour_theme.get_colour_theme_settings(
            "background"
        )
        (
            self.title_font,
            self.title_font_size,
            self.title_font_colour,
            self.subtitle_font,
            self.subtitle_font_size,
            self.subtitle_font_colour,
        ) = self.colour_theme.get_colour_theme_settings("title")
        (
            self.timeline_year_font,
            self.timeline_year_font_size,
            self.timeline_year_font_colour,
            self.timeline_year_fill_colour,
            self.timeline_item_font,
            self.timeline_item_font_size,
            self.timeline_item_font_colour,
            self.timeline_item_fill_colour,
        ) = self.colour_theme.get_colour_theme_settings("timeline")
        (
            self.marker_font,
            self.marker_font_size,
            self.marker_font_colour,
            self.marker_line_colour,
        ) = self.colour_theme.get_colour_theme_settings("marker")
        (
            self.group_font,
            self.group_font_size,
            self.group_font_colour,
            self.group_fill_colour,
        ) = self.colour_theme.get_colour_theme_settings("group")
        (
            self.task_font,
            self.task_font_size,
            self.task_font_colour,
            self.task_fill_colour,
            self.task_style,
        ) = self.colour_theme.get_colour_theme_settings("task")
        (
            self.milestone_font,
            self.milestone_font_size,
            self.milestone_font_colour,
            self.milestone_fill_colour,
        ) = self.colour_theme.get_colour_theme_settings("milestone")
        (
            self.footer_font,
            self.footer_font_size,
            self.footer_font_colour,
        ) = self.colour_theme.get_colour_theme_settings("footer")

    def get_font_path(self, font_name: str) -> str:
        """Get the path to the font file"""
        if font_name.endswith(".ttf") or font_name.endswith(".otf"):
            return font_name
        if sys.platform.startswith("win"):  # Windows
            return os.path.join("C:\\", "Windows", "Fonts", f"{font_name}.ttf")
        elif sys.platform.startswith("darwin"):  # macOS
            return os.path.join(
                "/", "System", "Library", "Fonts", "Supplemental", f"{font_name}.ttf"
            )
        elif sys.platform.startswith("linux"):  # Linux
            font_dir = "/usr/share/fonts/truetype/msttcorefonts"

            if os.path.exists(os.path.join(font_dir, f"{font_name}.ttf")):
                return os.path.join(font_dir, f"{font_name}.ttf")
            ### This is cater for cases where msttcorefonts is not installed
            linux_font_name = "DejaVuSans"  # Default font for Linux
            return os.path.join(
                "/",
                "usr",
                "share",
                "fonts",
                "truetype",
                "dejavu",  # Use the DejaVu font directory instead of msttcorefonts
                f"{linux_font_name}.ttf",
            )
        else:
            raise UnsupportedOSException("Unsupported operating system")

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

    def get_text_dimension(self, text: str, font: str, font_size: int) -> tuple:
        raise NotImplementedError

    def set_line_style(self, style: str = "solid") -> None:
        """Set line style

        Args:
            style (str, optional): Line style. Defaults to "solid". Options: "solid", "dashed"
        """
        self.dash = (10.0, 5.0) if style == "dashed" else None

    def draw_box(
        self, x: int, y: int, width: int, height: int, box_fill_colour: str
    ) -> list:
        """Draw a rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """
        return [(x, y), (x + width, y + height)]

    def draw_rounded_box(
        self, x: int, y: int, width: int, height: int, box_fill_colour: str
    ) -> list:
        """Draw a rounded rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """
        return [(x, y), (x + width, y + height)]

    def draw_arrowhead_box(
        self, x: int, y: int, width: int, height: int, box_fill_colour: str
    ) -> list:
        """Draw a rounded rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """
        arrowhead_width = 10
        width -= arrowhead_width
        box_shape = [(x, y), (x + width, y + height)]

        # Set the coordinates of the arrowhead
        vertical_midpoint = (height / 2) + y
        arrowhead_endpoint = x + width + arrowhead_width
        arrowhead_shape = [
            (x + width, y),
            (arrowhead_endpoint, vertical_midpoint),
            (x + width, y + height),
        ]

        return box_shape, arrowhead_shape

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
        style: str = "rectangle",
    ) -> tuple:
        return (
            box_x,
            box_y,
            box_x + box_width,
            box_y + box_height,
        )

    def draw_diamond(
        self, x: int, y: int, width: int, height: int, fill_colour: str
    ) -> list:
        """Draw a diamond

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Diamond width
            height (int): Diamond height
            fill_colour (str): Diamond fill colour in HTML colour name or hex code. Eg. #FFFFFF or LightGreen
        """

        # Calculate the coordinates of the four points of the diamond.
        return [
            (x + width / 2, y),
            (x + width, y + height / 2),
            (x + width / 2, y + height),
            (x, y + height / 2),
        ]

    def draw_text(
        self, x: int, y: int, text: str, font: str, font_size: int, font_colour: str
    ) -> None:
        raise NotImplementedError

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
        raise NotImplementedError

    def draw_cross_on_box(
        self, x1: int, y1: int, x2: int, y2: int, colour: str
    ) -> None:
        raise NotImplementedError

    def draw_logo(self, image: str, x: int, y: int, width: int, height: int) -> None:
        raise NotImplementedError

    def get_text_dimension(self, text: str, font: str, font_size: int) -> tuple:
        raise NotImplementedError

    def set_background_colour(self) -> None:
        raise NotImplementedError

    def set_surface_size(self, width: int, height: int) -> tuple:
        """Set surface size

        Args:
            width (int): Surface width
            height (int): Surface height
        """
        height += self.bottom_margin
        return 0, 0, width, height

    def get_image_size(self, image: str) -> tuple:
        raise NotImplementedError

    def save_surface(self, filename: str) -> None:
        raise NotImplementedError


class PNGPainter(Painter):
    """A wrapper class for Pillow library"""

    # initialise code
    def __init__(self, width: int, height: int):
        """__init__ method

        Args:
            width (int): Width of the surface
            height (int): Height of the surface
        """
        super().__init__(width, height)

        self.__surface = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        self.__cr = ImageDraw.Draw(self.__surface)

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

        shape = super().draw_box(x, y, width, height, box_fill_colour)
        self.__cr.rectangle(shape, fill=box_fill_colour)

    def draw_rounded_box(
        self, x: int, y: int, width: int, height: int, box_fill_colour: str
    ) -> None:
        """Draw a rounded rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """
        shape = super().draw_rounded_box(x, y, width, height, box_fill_colour)
        radius = 20
        self.__cr.rounded_rectangle(shape, radius, fill=box_fill_colour)

    def draw_arrowhead_box(
        self, x: int, y: int, width: int, height: int, box_fill_colour: str
    ) -> None:
        """Draw a rounded rectagle

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            box_fill_colour (str: HTML colour name or hex code. Eg. #FFFFFF or LightGreen)
        """
        box_shape, arrowhead_shape = super().draw_arrowhead_box(
            x, y, width, height, box_fill_colour
        )

        # Draw the rectangle
        self.__cr.rectangle(box_shape, fill=box_fill_colour)

        # Draw the arrowhead
        self.__cr.polygon(arrowhead_shape, fill=box_fill_colour)

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
        style: str = "rectangle",
    ) -> None:
        box_x1, box_y1, box_x2, box_y2 = super().draw_box_with_text(
            box_x,
            box_y,
            box_width,
            box_height,
            box_fill_colour,
            text,
            text_alignment,
            text_font,
            text_font_size,
            text_font_colour,
            style,
        )
        match style:
            case "rectangle":
                self.draw_box(
                    box_x1,
                    box_y1,
                    box_width,
                    box_height,
                    box_fill_colour=box_fill_colour,
                )
            case "rounded":
                self.draw_rounded_box(
                    box_x1, box_y1, box_width, box_height, box_fill_colour
                )
            case "arrowhead":
                self.draw_arrowhead_box(
                    box_x1, box_y1, box_width, box_height, box_fill_colour
                )
            case _:
                raise ValueError("Invalid style")

        font = ImageFont.truetype(self.get_font_path(text_font), size=text_font_size)

        multi_lines = []
        wrap_lines = []

        ### Make '\n' work
        multi_lines = text.splitlines()

        left, _, right, _ = font.getbbox("a")
        single_char_width = right - left

        ### wrap text
        for line in multi_lines:
            wrap_lines.extend(textwrap.wrap(line, int(box_width / single_char_width)))

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
        points = super().draw_diamond(x, y, width, height, fill_colour)

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
            font=ImageFont.truetype(self.get_font_path(font), font_size),
            anchor="la",
            fill=(font_colour),
        )

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
            # and draw them with a gap in between.

            ### Calculate the number of dashes
            gap_counts = int((y2 - y1) / 7)

            for i, (x, y) in enumerate(
                zip(
                    linspace(x1, x2, gap_counts),
                    linspace(y1, y2, gap_counts),
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

    def draw_logo(self, image: str, x: int, y: int, width: int, height: int) -> None:
        """Draw a logo

        Args:
            x (int): x coordinate of logo
            y (int): y coordinate of logo
            logo (str): Logo file name
        """
        logo = Image.open(image)
        logo = logo.resize((width, height))
        logo = logo.convert("RGBA")
        mask = Image.new("L", logo.size, 0)
        mask.paste(255, (0, 0, logo.size[0], logo.size[1]), logo)
        logo.putalpha(mask)

        self.__surface.paste(logo, (x, y))

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
        image_font = ImageFont.truetype(self.get_font_path(font), font_size)

        left, _, right, bottom = image_font.getbbox(text)
        font_width = right
        font_height = bottom

        return font_width, font_height

    def set_background_colour(self) -> None:
        """Set surface background colour"""
        if self.background_colour == "transparent":
            # Set transparent background
            self.__cr.rectangle((0, 0, self.width, self.height), fill=(0, 0, 0, 0))
        else:
            self.__cr.rectangle(
                (0, 0, self.width, self.height), fill=self.background_colour
            )

    def set_surface_size(self, width: int, height: int) -> None:
        """Set surface size

        Args:
            width (int): Surface width
            height (int): Surface height
        """
        left, top, right, bottom = super().set_surface_size(width, height)
        self.__surface = self.__surface.crop((left, top, right, bottom))

    def get_image_size(self, image: str) -> tuple:
        """Get image size

        Args:
            image (str): Image path

        Returns:
            (width (int), height (int)): Image width and height
        """
        with Image.open(image) as img:
            return img.size

    def save_surface(self, filename: str) -> None:
        """Save surface to PNG file

        Args:
            filename (str): PNG file name
        """

        if self.__surface is not None:
            self.__surface.save(filename)


class SVGPainter(Painter):
    def __init__(self, width: int, height: int):
        """__init__ method

        Args:
            width (int): Width of the surface
            height (int): Height of the surface
        """
        super().__init__(width, height)
        self.__cr = None
        self.elements = []

    def draw_box(
        self, x: int, y: int, width: int, height: int, box_fill_colour: str
    ) -> None:
        """Draw a rectagle"""

        # Create a rectangle shape
        rectangle = dw.Rectangle(x, y, width, height, fill=box_fill_colour)

        self.elements.append(rectangle)

    def draw_rounded_box(
        self, x: int, y: int, width: int, height: int, box_fill_colour: str
    ) -> None:
        """Draw a rounded rectagle"""
        shape = super().draw_rounded_box(x, y, width, height, box_fill_colour)
        radius = 20
        rectangle = dw.Rectangle(
            x, y, width, height, rx=radius, ry=radius, fill=box_fill_colour
        )

        self.elements.append(rectangle)

    def draw_arrowhead_box(
        self, x: int, y: int, width: int, height: int, box_fill_colour: str
    ) -> None:
        """Draw a rounded rectagle"""
        box_shape, arrowhead_shape = super().draw_arrowhead_box(
            x, y, width, height, box_fill_colour
        )

        # Draw the rectangle
        rectangle = dw.Rectangle(x, y, width, height, fill=box_fill_colour)

        # Draw the arrowhead
        poly = dw.Lines(arrowhead_shape, fill=box_fill_colour)
        self.elements.append(rectangle)
        self.elements.append(poly)

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
        style: str = "rectangle",
    ) -> None:
        box_x1, box_y1, box_x2, box_y2 = super().draw_box_with_text(
            box_x,
            box_y,
            box_width,
            box_height,
            box_fill_colour,
            text,
            text_alignment,
            text_font,
            text_font_size,
            text_font_colour,
            style,
        )
        match style:
            case "rectangle":
                self.draw_box(
                    box_x1,
                    box_y1,
                    box_width,
                    box_height,
                    box_fill_colour=box_fill_colour,
                )
            case "rounded":
                self.draw_rounded_box(
                    box_x1, box_y1, box_width, box_height, box_fill_colour
                )
            case "arrowhead":
                self.draw_arrowhead_box(
                    box_x1, box_y1, box_width, box_height, box_fill_colour
                )
            case _:
                raise ValueError("Invalid style")

        font = ImageFont.truetype(self.get_font_path(text_font), size=text_font_size)

        multi_lines = []
        wrap_lines = []

        ### Make '\n' work
        multi_lines = text.splitlines()

        left, _, right, _ = font.getbbox("a")
        single_char_width = right - left

        ### wrap text
        for line in multi_lines:
            wrap_lines.extend(textwrap.wrap(line, int(box_width / single_char_width)))

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

            txt = dw.Text(
                line,
                x=x,
                y=y,
                font_size=text_font_size,
                stroke=text_font_colour,
                text_anchor="start",
                dominant_baseline="hanging",
                font_family=text_font,
            )
            self.elements.append(txt)

    def draw_diamond(
        self, x: int, y: int, width: int, height: int, fill_colour: str
    ) -> None:
        """Draw a diamond"""

        # Calculate the coordinates of the four points of the diamond.
        points = super().draw_diamond(x, y, width, height, fill_colour)

        # Use Pillow's ImageDraw module to draw a polygon with the given points and fill color.
        x1, y1 = points[0]
        x2, y2 = points[1]
        x3, y3 = points[2]
        x4, y4 = points[3]
        diamond = dw.Lines(x1, y1, x2, y2, x3, y3, x4, y4, fill=fill_colour)
        self.elements.append(diamond)

    def draw_text(
        self,
        x: int,
        y: int,
        text: str,
        font: str,
        font_size: int,
        font_colour: str,
    ) -> None:
        """Draw text"""
        txt = dw.Text(
            text,
            x=x,
            y=y,
            font_size=font_size,
            text_anchor="start",
            dominant_baseline="middle",
            font_family=font,
            stroke=font_colour,
        )
        self.elements.append(txt)

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
        """Draw a line"""
        r, g, b = ImageColor.getrgb(line_colour)

        def linspace(start, stop, n):
            if n == 1:
                yield stop
                return
            h = (stop - start) / (n - 1)
            for i in range(n):
                yield start + h * i

        if line_style == "solid":
            line = dw.Line(
                x1,
                y1,
                x2,
                y2,
                width=line_width,
                fill=(r, g, b, int(255 * line_transparency)),
            )
            self.elements.append(line)
        elif line_style == "dashed":
            # given a line between x1, y1 and x2, y2, divide it into multiple shorter lines
            # and draw them with a gap in between.

            ### Calculate the number of dashes
            gap_counts = int((y2 - y1) / 7)

            for i, (x, y) in enumerate(
                zip(
                    linspace(x1, x2, gap_counts),
                    linspace(y1, y2, gap_counts),
                )
            ):
                if i % 2 == 0:
                    line = dw.Line(x, y, x, y + 10, stroke=line_colour)
                    self.elements.append(line)

    def draw_cross_on_box(
        self, x1: int, y1: int, x2: int, y2: int, colour: str
    ) -> None:
        """Draw a cross (vertical and horizontal lines) on a box"""

        cross = dw.Line(
            x1 + ((x2 - x1) / 2), y1, x1 + ((x2 - x1) / 2), y2, stroke="red"
        )
        self.elements.append(cross)

    def draw_logo(self, image: str, x: int, y: int, width: int, height: int) -> None:
        """Draw a logo"""
        logo = Image.open(image)
        logo = logo.resize((width, height))
        logo = logo.convert("RGBA")

        logo_image = dw.Image(x, y, width, height, image, embed=True)
        # self.__cr.apped(logo_image)
        self.elements.append(logo_image)

    def get_text_dimension(self, text: str, font: str, font_size: int) -> tuple:
        """Get text dimension"""
        # Use Pillow's ImageFont module to get the dimensions of the text.
        image_font = ImageFont.truetype(self.get_font_path(font), font_size)

        left, _, right, bottom = image_font.getbbox(text)
        font_width = right
        font_height = bottom

        return font_width, font_height

    def set_background_colour(self) -> None:
        """Set surface background colour"""
        if self.background_colour == "transparent":
            # Set transparent background
            bg = dw.Rectangle(0, 0, self.width, self.height, fill="white")
        else:
            bg = dw.Rectangle(
                0, 0, self.width, self.height, fill=self.background_colour
            )

        # self.__cr.append(bg)
        self.elements.append(bg)

    def set_surface_size(self, width: int, height: int) -> None:
        """Set surface size"""
        left, top, right, bottom = super().set_surface_size(width, height)

        self.__cr = dw.Drawing(right, bottom)
        for element in self.elements:
            self.__cr.append(element)

    def get_image_size(self, image: str) -> tuple:
        """Get image size"""
        with Image.open(image) as img:
            return img.size

    def save_surface(self, filename: str) -> None:
        """Save surface to SVG file"""

        if self.__cr is not None:
            self.__cr.save_svg(filename)


class PainterFactory:
    """A factory class to create painter objects"""

    def __init__(self):
        self._painters = {}

    def get_painter(self, painter_name, width, height):
        if painter_name not in self._painters:
            self._painters[painter_name] = self._create_painter(
                painter_name, width, height
            )
        return self._painters[painter_name]

    def _create_painter(self, painter_name, width, height):
        # Return a painter object based on the painter_name without using if statement
        return globals()[f"{painter_name.upper()}Painter"](width, height)
