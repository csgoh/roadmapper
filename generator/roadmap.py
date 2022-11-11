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

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass, field
from contextlib import contextmanager

from generator.painter import Painter
from generator.title import Title
from generator.footer import Footer
from generator.timelinemode import TimelineMode
from generator.timeline import Timeline
from generator.group import Group


@dataclass()
class Roadmap:
    width: int = field(default=1200)
    height: int = field(default=600)
    title: Title = field(default=None, init=False)
    timeline: Timeline = field(default=None, init=False)
    # groups: list[Group] = field(default_factory=list, init=False)
    footer: Footer = field(default=None, init=False)

    def __post_init__(self):
        self.__painter = Painter(self.width, self.height, "test.png")
        self.__painter.set_background_colour("White")
        self.groups = []
        self.__last_y_pos = 0
        self.__mode = TimelineMode.MONTHLY

    def set_title(
        self,
        text: str,
        font: str = "Arial",
        font_size: int = 18,
        font_colour: str = "Black",
    ):
        self.title = Title(
            text=text, font=font, font_size=font_size, font_colour=font_colour
        )
        self.title.text = text

        self.title.set_draw_position(self.__painter)

    def set_footer(
        self,
        text: str,
        font: str = "Arial",
        font_size: int = 18,
        font_colour: str = "Black",
    ):
        self.footer = Footer(
            text=text, font=font, font_size=font_size, font_colour=font_colour
        )
        self.footer.text = text
        self.footer.set_draw_position(self.__painter, self.__last_y_pos)

    def set_timeline(
        self,
        mode=TimelineMode.MONTHLY,
        start=datetime.strptime(
            datetime.strftime(datetime.today(), "%Y-%m-%d"), "%Y-%m-%d"
        ),
        number_of_items=12,
        font="Arial",
        font_size=10,
        font_colour="Black",
        fill_colour="lightgrey",
    ):
        start_date = datetime.strptime(start, "%Y-%m-%d")
        self.timeline = Timeline(
            mode=mode,
            start=start_date,
            number_of_items=number_of_items,
            font=font,
            font_size=font_size,
            font_colour=font_colour,
            fill_colour=fill_colour,
        )
        self.timeline.set_draw_position(self.__painter)
        return None

    @contextmanager
    def add_group(
        self,
        text: str,
        font="Arial",
        font_size=10,
        font_colour="Black",
        fill_colour="lightgrey",
    ):
        try:
            group = Group(
                text=text, font=font, font_size=font_size, font_colour=font_colour
            )
            self.groups.append(group)
            yield group
        finally:
            group.set_draw_position(self.__painter, self.timeline)
            group = None

    def draw(self):
        self.title.draw(self.__painter)
        self.timeline.draw(self.__painter)
        for group in self.groups:
            group.draw(self.__painter)
        self.footer.draw(self.__painter)

    def save(self):
        self.__painter.save_surface()

    def print_roadmap(self, print_area: str = "all"):
        if print_area == "all" or print_area == "title":
            print(f"Title={self.title.text}")

        if print_area == "all" or print_area == "timeline":
            print("Timeline:")
            for timeline_item in self.timeline.timeline_items:
                print(
                    f"       text={timeline_item.text}, value={timeline_item.value}, box_x={round(timeline_item.box_x,2)}, box_y={timeline_item.box_y}, box_w={round(timeline_item.box_width,2)}, box_h={timeline_item.box_height}, text_x={round(timeline_item.text_x,2)}, text_y={timeline_item.text_y}"
                )

        if print_area == "all" or print_area == "groups":
            for group in self.groups:
                print(
                    f"Group: text={group.text}, x={round(group.box_x,2)}, y={group.box_y}, w={group.box_width}, h={group.box_height}"
                )
                for task in group.tasks:
                    print(
                        f"        {task.text}, start={task.start}, end={task.end}, x={task.box_x}, y={task.box_y}, w={task.box_width}, h={task.box_height}"
                    )
                    for milestone in task.milestones:
                        print(
                            f"                {milestone.text}, date={milestone.date}, x={milestone.x}, y={milestone.y}, w={milestone.width}, h={milestone.height}, font_colour={milestone.font_colour}, fill_colour={milestone.fill_colour}"
                        )
                    for parellel_task in task.tasks:
                        print(
                            f"             Parellel Task: {parellel_task.text}, start={parellel_task.start}, end={parellel_task.end}, x={parellel_task.box_x}, y={parellel_task.box_y}, w={parellel_task.box_width}, h={parellel_task.box_height}"
                        )
                        for parellel_task_milestone in parellel_task.milestones:
                            print(
                                f"                        {parellel_task_milestone.text}, date={parellel_task_milestone.date}, x={parellel_task_milestone.x}, y={parellel_task_milestone.y}, w={parellel_task_milestone.width}, h={parellel_task_milestone.height}"
                            )
        if print_area == "all" or print_area == "footer":
            print(
                f"Footer: {self.footer.text} x={self.footer.x} y={self.footer.y} w={self.footer.width} h={self.footer.height}"
            )
