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
from task import Task


@dataclass
class Group:
    text: str
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    font: str = "Arial"
    font_size: int = 10
    font_colour: str = "black"
    fill_colour: str = "lightgrey"
    

    def __post_init__(self):
        self.tasks = []
        
    @contextmanager
    def add_task(self, text, start, end, font="Arial", font_size=12, font_colour="Black", fill_colour="LightGreen"):
        try:
            task = Task(text=text, start=start, end=end, font=font, font_size=font_size, font_colour=font_colour, fill_colour=fill_colour)
            self.tasks.append(task)
            yield task
        finally:
            task = None

    def set_draw_position(self, painter: Painter):
        additional_height_for_milestone = 6
        # Calculate number of milestones in group
        milestone_count = 0
        tasks = self.__roadmap_input[group_text].get("tasks", {})
        for task in tasks:
            for milestone in tasks[task].get("milestones", {}):
                if milestone != {}:
                    milestone_count += 1
                    break

        # Calc group height
        task_count = len(self.__roadmap_input[group_text].get("tasks"))
        group_total_height = (
            (20 * task_count)
            + (additional_height_for_milestone * milestone_count)
            + (2 * (task_count - 1))
        )
        group_total_width = max_width + 10

        self.__painter.set_colour(self.__roadmap_input[group_text].get("colour"))
        # self.__painter.draw_box(x, y, group_total_width, group_total_height)

        # print(
        #     f"-->draw_group {group_text} {x=} {y=} {group_total_width=} {max_height=}"
        # )

        self.__painter.draw_box(x, y, group_total_width, max_height)

        self.__painter.set_colour(self.group_text_colour)
        x_pos, y_pos = self.__painter.get_display_text_position(
            x, y, group_total_width, max_height, group_text, "centre"
        )
        # print(
        #     f"{x=}, {y=}, {group_total_width=}, {max_height=}, {x_pos=} {y_pos=} {group_text=}"
        # )
        if max_height > 0:
            self.__painter.set_font(self.text_font, 12, self.group_text_colour)
            self.__painter.draw_text(x_pos, y_pos, group_text)
            text_width, text_height = self.__painter.get_text_dimension(group_text)
        return y + max_height
        

    def draw(self, painter: Painter):
        # Step 1: draw tasks
        for tasks in self.tasks:
            tasks.draw(painter)

        # Step 2: draw group box

