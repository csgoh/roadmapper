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

from dataclasses import dataclass, field
from datetime import datetime

from .painter import Painter


@dataclass(kw_only=True)
class TimelineYear:
    """Roadmap TimelineYear class"""

    text: str = field(init=True, default=None)
    value: str = field(init=True, default=None)
    start: datetime = field(init=True, default=None)
    end: datetime = field(init=True, default=None)
    font: str = field(init=True, default=None)
    font_size: int = field(init=True, default=None)
    font_colour: str = field(init=True, default=None)
    fill_colour: str = field(init=True, default=None)

    box_x: int = field(init=False, default=0)
    box_y: int = field(init=False, default=0)
    box_width: int = field(init=False, default=0)
    box_height: int = field(init=False, default=0)
    text_x: int = field(init=False, default=0)
    text_y: int = field(init=False, default=0)

    def __calculate_text_draw_position(self, painter: Painter) -> tuple:
        """Calculate the text draw position based on the box position and size

        A Args:
            painter (Painter): Pillow wrapper class instance

        Returns:
            tuple(int, int): (x, y) position of the text
        """

        return painter.get_display_text_position(
            self.box_x,
            self.box_y,
            self.box_width,
            self.box_height,
            self.text,
            "centre",
            self.font,
            self.font_size,
        )

    def set_draw_position(
        self,
        painter: Painter,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        """Set the draw position of the timeline item group

        Args:
            painter (Painter): Pillow wrapper class instance
            x (int): x position of the box
            y (int): y position of the box
            width (int): width of the box
            height (int): height of the box
        """
        self.box_x = x
        self.box_y = y
        self.box_width = width
        self.box_height = height
        self.text_x, self.text_y = self.__calculate_text_draw_position(painter)
        painter.next_y_pos = self.box_y

    def draw(self, painter: Painter) -> None:
        """Draw the timeline

        Args:
            painter (Painter): Pillow wrapper class instance
        """
        painter.draw_box_with_text(
            self.box_x,
            self.box_y,
            self.box_width,
            self.box_height,
            self.fill_colour,
            self.text,
            "centre",
            self.font,
            self.font_size,
            self.font_colour,
        )
