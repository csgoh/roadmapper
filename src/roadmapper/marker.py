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
from datetime import datetime
from dataclasses import dataclass, field
from roadmapper.painter import Painter
from roadmapper.timeline import Timeline
from roadmapper.group import Group


@dataclass(kw_only=True)
class Marker:
    """A marker used to show the "Now" vertical line on the timeline"""

    font: str = field(default="Arial")
    font_size: int = field(default=12)
    font_colour: str = field(default="#004d80")
    line_colour: str = field(default="#007acc")
    line_width: int = field(default=1)
    line_style: str = field(default="dashed")

    def __post_init__(self):
        """This method is called after __init__() is called"""
        self.text = "Now"
        self.label_x = 0
        self.label_y = 0
        self.label_width = 0
        self.label_height = 0
        self.line_from_x = 0
        self.line_from_y = 0
        self.line_to_x = 0
        self.line_to_y = 0

    def set_label_draw_position(self, painter: Painter, timeline: Timeline) -> None:
        """Set marker label draw position

        Args:
            painter (Painter): PyCairo wrapper class instance
            timeline (Timeline): Timeline instance
        """
        current_date = datetime.today()
        current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        label_pos_percentage = 0
        for timeline_item in timeline.timeline_items:
            if timeline_item.start <= current_date <= timeline_item.end:
                # calc label position
                (
                    correct_timeline,
                    label_pos_percentage,
                ) = timeline_item.get_timeline_pos_percentage(
                    timeline.mode, current_date
                )
                if correct_timeline == True:
                    break

        self.line_from_x = timeline_item.box_x + (
            timeline_item.box_width * label_pos_percentage
        )
        self.label_y = painter.last_drawn_y_pos + 8
        painter.set_font(self.font, self.font_size, self.font_colour)
        self.label_width, self.label_height = painter.get_text_dimension(self.text)
        self.label_x = self.line_from_x - (self.label_width / 2)
        self.line_from_y = self.label_y + self.label_height + 4
        painter.last_drawn_y_pos = self.label_y + self.label_height

    def set_line_draw_position(self, painter: Painter) -> None:
        """Set marker line draw position

        Args:
            painter (Painter): PyCairo wrapper class instance
        """
        self.line_to_x = self.line_from_x
        self.line_to_y = painter.last_drawn_y_pos + 10

    def draw(self, painter: Painter) -> None:
        """Draw marker

        Args:
            painter (Painter): PyCairo wrapper class instance
        """
        # print(
        #     f"marker: {self.line_from_x=}, {self.line_from_y=}, {self.line_to_x=}, {self.line_to_y=}"
        # )
        painter.set_font(self.font, self.font_size, self.font_colour)
        painter.set_colour(self.font_colour)
        painter.draw_text(self.label_x, self.label_y + 10, self.text)
        painter.set_colour_alpha(self.line_colour)
        painter.set_line_width(self.line_width)
        painter.set_line_style(self.line_style)

        painter.draw_line(
            self.line_from_x, self.line_from_y, self.line_to_x, self.line_to_y
        )
