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
from src.roadmapper.painter import Painter


@dataclass(kw_only=True)
class Logo:
    """Logo class - used to show the logo on the roadmap"""

    image: str = field(init=True, default=None)
    position: int = field(init=True, default=None)
    width: str = field(init=True, default=0)
    height: str = field(init=True, default=0)

    def set_draw_position(self, painter: Painter, auto_height: bool) -> None:
        """Set logo draw position

        Args:
            painter (Painter): Pillow wrapper class instance
            auto_height (bool): Auto height flag
        """
        ### Find image width and height
        self.image_width, self.image_height = painter.get_image_size(self.image)

        if self.width == 0 or self.height == 0:
            self.width = self.image_width
            self.height = self.image_height

        ### Calc top right corner position
        logo_offset = 10
        match self.position:
            case "top-left":
                self.x = painter.left_margin
                self.y = painter.top_margin
            case "top-centre":
                self.x = int((painter.width - self.width) / 2)
                self.y = painter.top_margin
                ### Please note that if logo is positioned at the top-centre, we need to update last_drawn_y_pos
                ### to push the Title down.
                painter.next_y_pos = self.y + self.height
            case "top-right":
                self.x = int(painter.width - self.width - painter.right_margin)
                self.y = painter.top_margin
            case "bottom-left":
                self.x = painter.left_margin
                self.y = (
                    painter.next_y_pos + logo_offset
                    if auto_height == True
                    else painter.height - self.height - painter.bottom_margin
                )
                painter.next_y_pos = self.y + self.height
            case "bottom-centre":
                self.x = int((painter.width - self.width) / 2)
                self.y = (
                    painter.next_y_pos + logo_offset
                    if auto_height == True
                    else painter.height - self.height - painter.bottom_margin
                )
                painter.next_y_pos = self.y + self.height
            case "bottom-right":
                self.x = painter.width - self.width - painter.right_margin
                self.y = (
                    painter.next_y_pos + logo_offset
                    if auto_height == True
                    else painter.height - self.height - painter.bottom_margin
                )
                painter.next_y_pos = self.y + self.height
            case _:  # Default to top right
                self.x = painter.width - self.width - painter.right_margin
                self.y = painter.top_margin

    def draw(self, painter: Painter) -> None:
        """Draw logo

        Args:
            painter (Painter): Pillow wrapper class instance
        """

        painter.draw_logo(
            self.image,
            self.x,
            self.y,
            self.width,
            self.height,
        )
