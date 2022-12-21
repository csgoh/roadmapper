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
from roadmapper.painter import Painter


@dataclass(kw_only=True)
class SubTitle:
    """Roadmap subtitle class"""

    text: str
    x: int = field(init=False)
    y: int = field(init=False)
    width: int = field(init=False)
    height: int = field(init=False)
    font: str = field(default="Arial")
    font_size: int = 12
    font_colour: str = "Black"

    def __calculate_draw_position(self, painter: Painter) -> tuple:
        """Calculate the draw position of the title

        Args:
            painter (Painter): PyCairo wrapper class instance

        Returns:
            tuple(int, int): x, y position of the title
        """

        self.width, self.height = painter.get_text_dimension(
            self.text, self.font, self.font_size
        )
        return (
            painter.width / 2
        ) - self.width / 2, painter.last_drawn_y_pos + self.height + 10

    def set_draw_position(self, painter: Painter) -> None:
        """Set the draw position of the title

        Args:
            painter (Painter): PyCairo wrapper class instance
        """
        self.x, self.y = self.__calculate_draw_position(painter)
        painter.last_drawn_y_pos = self.y

    def draw(self, painter: Painter) -> None:
        """Draw the title

        Args:
            painter (Painter): PyCairo wrapper class instance
        """
        painter.draw_text(
            self.x, self.y, self.text, self.font, self.font_size, self.font_colour
        )
