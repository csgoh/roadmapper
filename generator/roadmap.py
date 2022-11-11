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

import calendar
import pprint

from painter import Painter
from title import Title
from footer import Footer
from timelinemode import TimelineMode
from timeline import Timeline
from group import Group


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
                    f"Group: text={group.text}, x={round(group.x,2)}, y={group.y}, w={group.width}, h={group.height}"
                )
                for task in group.tasks:
                    print(
                        f"        {task.text}, start={task.start}, end={task.end}, x={task.x}, y={task.y}, w={task.width}, h={task.height}"
                    )
                    for milestone in task.milestones:
                        print(
                            f"                {milestone.text}, date={milestone.date}, x={milestone.x}, y={milestone.y}, w={milestone.width}, h={milestone.height}"
                        )
                    for parellel_task in task.tasks:
                        print(
                            f"             Parellel Task: {parellel_task.text}, start={parellel_task.start}, end={parellel_task.end}, x={parellel_task.x}, y={parellel_task.y}, w={parellel_task.width}, h={parellel_task.height}"
                        )
                        for parellel_task_milestone in parellel_task.milestones:
                            print(
                                f"                        {parellel_task_milestone.text}, date={parellel_task_milestone.date}, x={parellel_task_milestone.x}, y={parellel_task_milestone.y}, w={parellel_task_milestone.width}, h={parellel_task_milestone.height}"
                            )
        if print_area == "all" or print_area == "footer":
            print(
                f"Footer: {self.footer.text} x={self.footer.x} y={self.footer.y} w={self.footer.width} h={self.footer.height}"
            )


if __name__ == "__main__":
    my_roadmap = Roadmap(width=1000, height=512)
    my_roadmap.set_title("My Three Year Roadmap 2023-2025", font_size=18)
    my_roadmap.set_timeline(TimelineMode.MONTHLY, "2023-01-01", 12, font_size=11)

    with my_roadmap.add_group(
        "Group 1 something long", "Arial", 18, "Black", "White"
    ) as group1:
        with group1.add_task(
            "Task 1", "2023-01-01", "2023-03-01", "Arial", 12, "Black", "LightGreen"
        ) as task1:
            task1.add_milestone("Milestone 1", "2023-01-15", "Arial", 12, "Red", "Red")
            task1.add_milestone("Milestone 2", "2023-02-15", "Arial", 12, "Red", "Red")
            task1.add_milestone("Milestone 3", "2023-03-01", "Arial", 12, "Red", "Red")
            # with task1.add_parellel_task(
            #     "Task 1a", "2023-05-01", "2023-08-31", "Arial", 12, "Black", "LightBlue"
            # ) as task1a:
            #     task1a.add_milestone(
            #         "Milestone 1a", "2023-06-30", "Arial", 12, "Red", "Red"
            #     )
            #     task1a.add_milestone(
            #         "Milestone 2a", "2023-08-30", "Arial", 12, "Red", "Red"
            #     )
        with group1.add_task(
            "Task 2", "2023-03-01", "2023-04-30", "Arial", 12, "Black", "LightGreen"
        ) as task2:
            task2.add_milestone("Milestone 4", "2023-03-15", "Arial", 12, "Red", "Red")
            task2.add_milestone("Milestone 5", "2023-04-01", "Arial", 12, "Red", "Red")

    with my_roadmap.add_group("Stream 2", "Arial", 18, "Black", "White") as group2:
        with group2.add_task(
            "Task 3", "2023-04-01", "2023-08-30", "Arial", 12, "Black", "LightGreen"
        ) as task3:
            task3.add_milestone("Milestone 6", "2023-05-15", "Arial", 12, "Red", "Red")
            task3.add_milestone("Milestone 7", "2023-08-01", "Arial", 12, "Red", "Red")

    my_roadmap.set_footer("this is footer!!", font_size=10)
    my_roadmap.draw()
    my_roadmap.save()
    my_roadmap.print_roadmap("groups")
