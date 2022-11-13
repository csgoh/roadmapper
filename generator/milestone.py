# MIT License

# Copyright (c) 2022 Cheng Soon Goh

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
from generator.painter import Painter
from generator.timeline import Timeline


@dataclass(kw_only=True)
class Milestone:
    """Roadmap Milestone class"""

    text: str
    date: datetime
    font: str = field(default="Arial")
    font_size: int = field(default=10)
    font_colour: str = field(default="red")
    fill_colour: str = field(default="red")
    text_alignment: str = field(default="centre")

    def __post_init__(self):
        """This method is called after __init__() is called"""
        self.diamond_x = 0
        self.diamond_y = 0
        self.diamond_width = 0
        self.diamond_height = 0
        self.text_x = 0
        self.text_y = 0

    def draw(self, painter: Painter) -> None:
        """Draw milestone

        Args:
            painter (Painter): PyCairo wrapper class instance
        """
        # self.font_size = 10
        painter.set_font(self.font, self.font_size, self.font_colour)
        painter.set_colour(self.fill_colour)
        painter.draw_diamond(
            self.diamond_x, self.diamond_y, self.diamond_width, self.diamond_height
        )
        painter.draw_text(self.text_x, self.text_y, self.text)
