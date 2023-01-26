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
from contextlib import contextmanager

from roadmapper.painter import Painter
from roadmapper.timeline import Timeline
from roadmapper.milestone import Milestone


@dataclass(kw_only=True)
class Task:
    """Roadmap Task class"""

    text: str = field(init=True, default=None)
    start: datetime = field(init=True, default=None)
    end: datetime = field(init=True, default=None)
    font: str = field(init=True, default=None)
    font_size: int = field(init=True, default=0)
    font_colour: str = field(init=True, default=None)
    fill_colour: str = field(init=True, default=None)
    text_alignment: str = field(init=True, default=None)
    style: str = field(init=True, default=None)
    painter: Painter = field(init=True, default=None)

    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)
    tasks: list = field(init=False, default_factory=list)
    boxes: list = field(init=False, default_factory=list)
    milestones: list = field(init=False, default_factory=list)
    box_x: int = field(init=False, default=0)
    box_y: int = field(init=False, default=0)
    box_width: int = field(init=False, default=0)
    box_height: int = field(init=False, default=0)
    text_x: int = field(init=False, default=0)
    text_y: int = field(init=False, default=0)

    # def __post_init__(self):
    #     """This method is called after __init__() is called"""
    #     self.milestones = []
    #     self.tasks = []
    #     self.boxes = []
    #     self.box_x = 0
    #     self.box_y = 0
    #     self.box_width = 0
    #     self.box_height = 0
    #     self.text_x = 0
    #     self.text_y = 0

    def add_parallel_task(
        self,
        text: str,
        start: datetime,
        end: datetime,
        font: str = "",
        font_size: int = 0,
        font_colour: str = "",
        fill_colour: str = "",
        text_alignment: str = "centre",
        style: str = "rectangle",
    ):
        """Add a parallel task to this task

        Args:
            text (str): Task text
            start (datetime): Task start date
            end (datetime): Task end date
            font (str, optional): Task text font. Defaults to "Arial".
            font_size (int, optional): Task text font size. Defaults to 12.
            font_colour (str, optional): Task text font colour. Defaults to "Black".
            fill_colour (str, optional): Task fill colour. Defaults to "LightGreen".

        Return:
            Task: A task object that can be used to add milestones
        """
        if font == "":
            font = self.painter.task_font
        if font_size == 0:
            font_size = self.painter.task_font_size
        if font_colour == "":
            font_colour = self.painter.task_font_colour
        if fill_colour == "":
            fill_colour = self.painter.task_fill_colour

        if style == "":
            style = self.painter.task_style

        task = Task(
            text=text,
            start=start,
            end=end,
            font=font,
            font_size=font_size,
            font_colour=font_colour,
            fill_colour=fill_colour,
            text_alignment=text_alignment,
            style=style,
            painter=self.painter,
        )
        self.tasks.append(task)

        return task

    def add_milestone(
        self,
        text: str,
        date: datetime,
        font: str = "",
        font_size: int = 0,
        font_colour: str = "",
        fill_colour: str = "",
        text_alignment: str = "centre",
    ) -> None:
        """Add a new milestone to this task

        Args:
            text (str): Milestone text
            date (datetime): Milestone date
            font (str, optional): Milestone text font. Defaults to "Arial".
            font_size (int, optional): Milestone text font size. Defaults to 12.
            font_colour (str, optional): Milestone text font colour. Defaults to "Red". HTML colour name or hex code. Eg. #FFFFFF or LightGreen
            fill_colour (str, optional): Milestone fill colour. Defaults to "Red". HTML colour name or hex code. Eg. #FFFFFF or LightGreen
            text_alignment (str, optional): Milestone text alignment. Defaults to "centre". Options are "left", "centre", "right"
        """

        if self.painter is None:
            print("Painter is None")
        if font == "":
            font = self.painter.milestone_font
        if font_size == 0:
            font_size = self.painter.milestone_font_size
        if font_colour == "":
            font_colour = self.painter.milestone_font_colour
        if fill_colour == "":
            fill_colour = self.painter.milestone_fill_colour

        self.milestones.append(
            Milestone(
                text=text,
                date=date,
                font=font,
                font_size=font_size,
                font_colour=font_colour,
                fill_colour=fill_colour,
                text_alignment=text_alignment,
            )
        )

    def set_draw_position(
        self,
        painter: Painter,
        group_x: int,
        last_drawn_y: int,
        timeline: Timeline,
        milestone_exists_in_parent: bool = False,
    ) -> None:
        """Set the draw position of this task

        Args:
            painter (Painter): Pillow wrapper class instance
            group_x (int): Parent group x position
            last_drawn_y (int): Last drawn y position
            timeline (Timeline): Timeline object
        """
        task_y = last_drawn_y

        milestone_in_tasks = False
        if len(self.milestones) > 0:
            milestone_in_tasks = True
        else:
            for task in self.tasks:
                if len(task.milestones) > 0:
                    milestone_in_tasks = True

        if milestone_exists_in_parent == False:
            if milestone_in_tasks == True:
                self.box_y = task_y + painter.additional_height_for_milestone
            else:
                self.box_y = task_y
        else:
            self.box_y = task_y

        for_parallel_tasks_y = self.box_y

        task_start_period = datetime.strptime(self.start, "%Y-%m-%d")
        task_end_period = datetime.strptime(self.end, "%Y-%m-%d")

        self.set_task_position(painter, timeline, task_start_period, task_end_period)

        ### Set parallel tasks position
        for task in self.tasks:
            task.set_draw_position(
                painter,
                self.box_x,
                for_parallel_tasks_y,
                timeline,
                milestone_exists_in_parent=milestone_in_tasks,
            )

        ### Set milestones position
        self.set_milestones_position(painter, timeline)

    def set_milestones_position(
        self,
        painter: Painter,
        timeline: Timeline,
    ) -> None:
        """Set the draw position of this task's milestones

        Args:
            painter (Painter): Pillow wrapper class instance
            timeline (Timeline): Timeline object
            task_start_period (datetime): Task start date
            task_end_period (datetime): Task end date
        """
        for timeline_item in timeline.timeline_items:
            (
                timeline_start_period,
                timeline_end_period,
            ) = timeline_item.get_timeline_period(timeline.mode)

            bar_x_pos = timeline_item.box_x
            for milestone in self.milestones:
                milestone_date = datetime.strptime(milestone.date, "%Y-%m-%d")
                (
                    _,
                    milestone_pos_percentage,
                ) = timeline_item.get_timeline_pos_percentage(
                    timeline.mode, milestone_date
                )

                if timeline_start_period <= milestone_date <= timeline_end_period:
                    milestone.diamond_x = (
                        bar_x_pos
                        + (timeline_item.box_width * milestone_pos_percentage)
                        - 8
                        - 3
                    )
                    milestone.diamond_y = self.box_y - 3
                    milestone.diamond_width = 26
                    milestone.diamond_height = 26

                    width, _ = painter.get_text_dimension(
                        milestone.text, milestone.font, milestone.font_size
                    )
                    milestone.text_x = (
                        bar_x_pos
                        + (timeline_item.box_width * milestone_pos_percentage)
                        - (width / 3)
                    )
                    milestone.text_y = self.box_y - 18

    def is_task_begins_here_ends_here(
        self,
        timeline_start_period,
        timeline_end_period,
        task_start_period,
        task_end_period,
    ):
        """Determine whether the task begins and ends within the timeline period

        Args:
            timeline_start_period (_type_): timeline start period
            timeline_end_period (_type_): timeline end period
            task_start_period (_type_): task_start_period
            task_end_period (_type_): task_end_period

        Returns:
            bool: True if task begins and ends within the timeline period
        """
        return (
            timeline_start_period <= task_start_period <= timeline_end_period
            and timeline_start_period <= task_end_period <= timeline_end_period
        )

    def is_task_begins_here_ends_future(
        self,
        timeline_start_period,
        timeline_end_period,
        task_start_period,
        task_end_period,
    ):
        """Determine whether the task begins within the timeline period and ends in the future

        Args:
            timeline_start_period (_type_): timeline start period
            timeline_end_period (_type_): timeline end period
            task_start_period (_type_): task_start_period
            task_end_period (_type_): task_end_period

        Returns:
            bool: True if task begins within the timeline period and ends in the future
        """
        return (
            timeline_start_period <= task_start_period <= timeline_end_period
            and timeline_end_period <= task_end_period
        )

    def is_task_begins_past_ends_here(
        self,
        timeline_start_period,
        timeline_end_period,
        task_start_period,
        task_end_period,
    ):
        """Determine whether the task begins in the past and ends within the timeline period

        Args:
            timeline_start_period (_type_): timeline start period
            timeline_end_period (_type_): timeline end period
            task_start_period (_type_): task_start_period
            task_end_period (_type_): task_end_period

        Returns:
            bool: True if task begins in the past and ends within the timeline period
        """
        return (
            task_start_period < timeline_start_period
            and timeline_start_period <= task_end_period <= timeline_end_period
        )

    def is_task_begins_past_ends_future(
        self,
        timeline_start_period,
        timeline_end_period,
        task_start_period,
        task_end_period,
    ):
        """Determine whether the task begins in the past and ends in the future

        Args:
            timeline_start_period (_type_): timeline start period
            timeline_end_period (_type_): timeline end period
            task_start_period (_type_): task_start_period
            task_end_period (_type_): task_end_period

        Returns:
            bool: True if task begins in the past and ends in the future
        """
        return (
            task_start_period < timeline_start_period
            and timeline_end_period < task_end_period
        )

    def is_task_in_range(
        self,
        timeline_start_period,
        timeline_end_period,
        task_start_period,
        task_end_period,
    ):
        """Determine whether the task is within the timeline period

        Args:
            timeline_start_period (_type_): timeline start period
            timeline_end_period (_type_): timeline end period
            task_start_period (_type_): task_start_period
            task_end_period (_type_): task_end_period

        Returns:
            bool: True if task is within the timeline period
        """
        return (
            self.is_task_begins_here_ends_here(
                timeline_start_period,
                timeline_end_period,
                task_start_period,
                task_end_period,
            )
            or self.is_task_begins_here_ends_future(
                timeline_start_period,
                timeline_end_period,
                task_start_period,
                task_end_period,
            )
            or self.is_task_begins_past_ends_here(
                timeline_start_period,
                timeline_end_period,
                task_start_period,
                task_end_period,
            )
            or self.is_task_begins_past_ends_future(
                timeline_start_period,
                timeline_end_period,
                task_start_period,
                task_end_period,
            )
        )

    def set_task_position(
        self,
        painter: Painter,
        timeline: Timeline,
        task_start_period: datetime,
        task_end_period: datetime,
    ) -> None:
        """Set the draw position of this task

        Args:
            painter (Painter): Pillow wrapper class instance
            timeline (Timeline): Timeline object
            task_start_period (datetime): Task start date
            task_end_period (datetime): Task end date
        """
        self.box_x = 0
        row_match = 0
        bar_start_x_pos = 0

        for timeline_item in timeline.timeline_items:
            ### Get the start and end period of the timeline item
            (
                timeline_start_period,
                timeline_end_period,
            ) = timeline_item.get_timeline_period(timeline.mode)

            ### Check if the task is within the timeline period
            if (
                self.is_task_in_range(
                    timeline_start_period,
                    timeline_end_period,
                    task_start_period,
                    task_end_period,
                )
                == True
            ):
                (_, start_pos_percentage,) = timeline_item.get_timeline_pos_percentage(
                    timeline.mode,
                    task_start_period,
                )
                (_, end_pos_percentage,) = timeline_item.get_timeline_pos_percentage(
                    timeline.mode, task_end_period
                )
                row_match += 1

                ## Check condition 1
                if (
                    self.is_task_begins_here_ends_here(
                        timeline_start_period,
                        timeline_end_period,
                        task_start_period,
                        task_end_period,
                    )
                    == True
                ):
                    self.box_x = timeline_item.box_x + (
                        timeline_item.box_width * start_pos_percentage
                    )
                    self.box_width = (timeline_item.box_width * end_pos_percentage) - (
                        timeline_item.box_width * start_pos_percentage
                    )
                    bar_start_x_pos = self.box_x

                ## Check condition 2
                if (
                    self.is_task_begins_past_ends_here(
                        timeline_start_period,
                        timeline_end_period,
                        task_start_period,
                        task_end_period,
                    )
                    == True
                ):
                    self.box_x = timeline_item.box_x
                    if bar_start_x_pos == 0:
                        bar_start_x_pos = self.box_x
                    self.box_width = timeline_item.box_width * end_pos_percentage

                ## Check condition 3
                if (
                    self.is_task_begins_here_ends_future(
                        timeline_start_period,
                        timeline_end_period,
                        task_start_period,
                        task_end_period,
                    )
                    == True
                ):
                    self.box_x = timeline_item.box_x + (
                        timeline_item.box_width * start_pos_percentage
                    )
                    self.box_width = timeline_item.box_width - (
                        timeline_item.box_width * start_pos_percentage
                    )
                    bar_start_x_pos = self.box_x

                ## Check condition 4
                if (
                    self.is_task_begins_past_ends_future(
                        timeline_start_period,
                        timeline_end_period,
                        task_start_period,
                        task_end_period,
                    )
                    == True
                ):
                    self.box_x = timeline_item.box_x
                    self.box_width = timeline_item.box_width

                    if bar_start_x_pos == 0:
                        bar_start_x_pos = self.box_x

                self.box_height = 20

                box_coordinates = [
                    int(self.box_x),
                    int(self.box_y),
                    int(self.box_width),
                    int(self.box_height),
                ]
                self.boxes.append(box_coordinates)

                bar_width = self.box_x + self.box_width - bar_start_x_pos
                painter.next_y_pos = self.box_y + self.box_height + 5

        if row_match > 0:
            text_x_pos, text_y_pos = painter.get_display_text_position(
                bar_start_x_pos,
                self.box_y,
                bar_width,
                self.box_height,
                self.text,
                self.text_alignment,
                self.font,
                self.font_size,
            )
            self.text_x = text_x_pos
            self.text_y = text_y_pos

    def draw(self, painter: Painter) -> None:
        """Draw the task

        Args:
            painter (Painter): Pillow wrapper class instance
        """
        box_x = 0
        box_y = 0
        width = 0
        height = 0

        for i, box in enumerate(self.boxes):
            # painter.draw_box(box[0], box[1], box[2], box[3], self.fill_colour)
            # painter.draw_rounded_box(box[0], box[1], box[2], box[3], self.fill_colour)
            if i == 0:
                box_x = box[0]
                box_y = box[1]
            width += int(box[2])
            height = box[3]

        box_width, box_height = (
            width,
            height,
        )

        if (box_x == 0 and box_y == 0 and box_width == 0 and box_height == 0) != True:
            painter.draw_box_with_text(
                box_x,
                box_y,
                box_width,
                box_height,
                self.fill_colour,
                self.text,
                "centre",
                self.font,
                self.font_size,
                self.font_colour,
                style=self.style,
            )

            for task in self.tasks:
                task.draw(painter)

            for milestone in self.milestones:
                milestone.draw(painter)
