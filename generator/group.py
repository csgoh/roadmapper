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
from dataclasses import dataclass, field
from contextlib import contextmanager
from painter import Painter
from timeline import Timeline
from task import Task


@dataclass
class Group:
    text: str
    box_x: int = 0
    box_y: int = 0
    box_width: int = 0
    box_height: int = 0
    font: str = "Arial"
    font_size: int = 10
    font_colour: str = "black"
    fill_colour: str = "lightgrey"

    def __post_init__(self):
        self.tasks = []
        self.text_x = 0
        self.text_y = 0

    @contextmanager
    def add_task(
        self,
        text,
        start,
        end,
        font="Arial",
        font_size=12,
        font_colour="Black",
        fill_colour="LightGreen",
    ):
        try:
            task = Task(
                text=text,
                start=start,
                end=end,
                font=font,
                font_size=font_size,
                font_colour=font_colour,
                fill_colour=fill_colour,
            )
            self.tasks.append(task)
            yield task
        finally:
            task = None

    def set_draw_position(self, painter: Painter, timeline: Timeline):
        additional_height_for_milestone = 6

        # Calculate number of milestones in group
        milestone_count = 0
        for task in self.tasks:
            milestone_count += len(task.milestones)

        # Calc group height
        task_count = len(self.tasks)
        # print(f"task count {task_count}")
        self.box_height = (
            (20 * task_count)
            + (additional_height_for_milestone * milestone_count)
            + (2 * (task_count - 1))
        )
        self.box_width = (
            painter.width - (painter.left_margin + painter.right_margin)
        ) * painter.group_box_width_percentage

        painter.set_colour(self.fill_colour)
        self.box_x = painter.left_margin

        self.box_y = painter.last_drawn_y_pos + additional_height_for_milestone
        painter.draw_box(self.box_x, self.box_y, self.box_width, self.box_height)

        painter.set_colour(self.font_colour)
        self.text_x, self.text_y = painter.get_display_text_position(
            self.box_x,
            self.box_y,
            self.box_width,
            self.box_height,
            self.text,
            "centre",
        )
        # painter.draw_text(x_pos, y_pos, self.text)

        painter.last_drawn_y_pos = self.box_y
        for task in self.tasks:
            task.set_draw_position(
                painter, self.box_x, painter.last_drawn_y_pos, timeline
            )

    def draw(self, painter: Painter):
        # Step 1: draw group
        painter.set_colour(self.fill_colour)
        painter.draw_box(self.box_x, self.box_y, self.box_width, self.box_height)
        painter.set_colour(self.font_colour)
        painter.set_font(self.font, self.font_size, self.font_colour)
        painter.draw_text(self.text_x, self.text_y, self.text)

        # Step 2: draw tasks
        for tasks in self.tasks:
            tasks.draw(painter)
