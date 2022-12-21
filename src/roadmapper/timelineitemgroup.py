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
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass, field
import calendar

from roadmapper.painter import Painter
from roadmapper.timelinemode import TimelineMode


@dataclass(kw_only=True)
class TimelineItemGroup:
    """Roadmap TimelineItemGroup class"""

    text: str
    value: str
    start: datetime
    end: datetime
    box_x: int = field(init=False)
    box_y: int = field(init=False)
    box_width: int = field(init=False)
    box_height: int = field(init=False)
    text_x: int = field(init=False)
    text_y: int = field(init=False)
    font: str
    font_size: int
    font_colour: str
    fill_colour: str

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
        painter.last_drawn_y_pos = self.box_y

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

    def draw_vertical_line(self, painter: Painter) -> None:

        x_pos = self.box_x - 1
        # painter.draw_line(
        #     x_pos,
        #     self.box_y,
        #     x_pos,
        #     self.box_y + self.box_height,
        #     "#e6e6e6",
        #     50,
        #     1,
        #     "solid",
        # )

        # painter.draw_line(
        #     self.box_x + self.box_width,
        #     self.box_y,
        #     self.box_x + self.box_width,
        #     self.box_y + self.box_height,
        #     "#e6e6e6",
        #     50,
        #     1,
        #     "solid",
        # )
        
