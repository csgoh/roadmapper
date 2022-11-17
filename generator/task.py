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
from generator.timeline import Timeline
from generator.milestone import Milestone


@dataclass(kw_only=True)
class Task:
    """Roadmap Task class"""

    text: str
    start: datetime
    end: datetime
    width: int = 0
    height: int = 0
    font: str = "Arial"
    font_size: int = 12
    font_colour: str = "Black"
    fill_colour: str = "LightGreen"
    text_alignment: str = "centre"

    def __post_init__(self):
        """This method is called after __init__() is called"""
        self.milestones = []
        self.tasks = []
        self.boxes = []
        self.box_x = 0
        self.box_y = 0
        self.box_width = 0
        self.box_height = 0
        self.text_x = 0
        self.text_y = 0

    @contextmanager
    def add_parellel_task(
        self,
        text: str,
        start: datetime,
        end: datetime,
        font: str = "Arial",
        font_size: int = 12,
        font_colour: str = "Black",
        fill_colour: str = "LightGreen",
        text_alignment: str = "centre",
    ) -> None:
        """Add a parallel task to this task

        Args:
            text (str): Task text
            start (datetime): Task start date
            end (datetime): Task end date
            font (str, optional): Task text font. Defaults to "Arial".
            font_size (int, optional): Task text font size. Defaults to 12.
            font_colour (str, optional): Task text font colour. Defaults to "Black".
            fill_colour (str, optional): Task fill colour. Defaults to "LightGreen".

        Yields:
            Task: A task object that can be used to add milestones
        """
        try:
            task = Task(
                text=text,
                start=start,
                end=end,
                font=font,
                font_size=font_size,
                font_colour=font_colour,
                fill_colour=fill_colour,
                text_alignment=text_alignment,
            )
            self.tasks.append(task)
            yield task
        finally:
            task = None

    def add_milestone(
        self,
        text: str,
        date: datetime,
        font: str = "Arial",
        font_size: int = 10,
        font_colour: str = "Red",
        fill_colour: str = "Red",
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
        self, painter: Painter, group_x: int, last_drawn_y: int, timeline: Timeline
    ) -> None:
        """Set the draw position of this task

        Args:
            painter (Painter): PyCairo wrapper class instance
            group_x (int): Parent group x position
            last_drawn_y (int): Last drawn y position
            timeline (Timeline): Timeline object
        """
        if len(self.milestones) > 0:
            self.box_y = last_drawn_y + 15
        else:
            self.box_y = last_drawn_y + 5

        task_start_period = datetime.strptime(self.start, "%Y-%m-%d")
        task_end_period = datetime.strptime(self.end, "%Y-%m-%d")

        for_parallel_tasks_y = last_drawn_y
        self.set_task_position(painter, timeline, task_start_period, task_end_period)

        self.set_milestones_position(
            painter, timeline, task_start_period, task_end_period
        )

        for task in self.tasks:
            task.set_draw_position(painter, self.box_x, for_parallel_tasks_y, timeline)

    def set_milestones_position(
        self,
        painter: Painter,
        timeline: Timeline,
        task_start_period: datetime,
        task_end_period: datetime,
    ) -> None:
        """Set the draw position of this task's milestones

        Args:
            painter (Painter): PyCairo wrapper class instance
            timeline (Timeline): Timeline object
            task_start_period (datetime): Task start date
            task_end_period (datetime): Task end date
        """
        for timeline_item in timeline.timeline_items:
            (
                timeline_start_period,
                timeline_end_period,
            ) = timeline_item.get_timeline_period(timeline.mode)
            if (
                (  # Check [timeline_start....<task_start>....timeline_end]
                    task_start_period >= timeline_start_period
                    and task_start_period <= timeline_end_period
                )
                or (  # Check [timeline_start....<task_end>....timeline_end]
                    task_end_period >= timeline_start_period
                    and task_end_period <= timeline_end_period
                )
                or (  # Check [<task_start>....[timeline_start....<task_end>.....timeline_end]
                    task_start_period <= timeline_start_period
                    and task_end_period >= timeline_end_period
                )
            ):
                (_, start_pos_percentage,) = timeline_item.get_timeline_pos_percentage(
                    timeline.mode,
                    task_start_period,
                )
                (_, end_pos_percentage,) = timeline_item.get_timeline_pos_percentage(
                    timeline.mode, task_end_period
                )

                bar_x_pos = timeline_item.box_x
                for milestone in self.milestones:
                    milestone_date = datetime.strptime(milestone.date, "%Y-%m-%d")
                    (
                        correct_timeline,
                        milestone_pos_percentage,
                    ) = timeline_item.get_timeline_pos_percentage(
                        timeline.mode, milestone_date
                    )

                    if correct_timeline == True:
                        # Draw milestone diamond
                        painter.set_font(
                            milestone.font,
                            10,
                            milestone.fill_colour,
                        )
                        milestone.diamond_x = (
                            bar_x_pos
                            + (timeline_item.box_width * milestone_pos_percentage)
                            - 8
                            - 3
                        )
                        milestone.diamond_y = self.box_y - 3
                        milestone.diamond_width = 26
                        milestone.diamond_height = 26

                        width, _ = painter.get_text_dimension(milestone.text)
                        milestone.text_x = (
                            bar_x_pos
                            + (timeline_item.box_width * milestone_pos_percentage)
                            - (width / 3)
                        )
                        milestone.text_y = self.box_y - 6

    def set_task_position(
        self,
        painter: Painter,
        timeline: Timeline,
        task_start_period: datetime,
        task_end_period: datetime,
    ) -> None:
        """Set the draw position of this task

        Args:
            painter (Painter): PyCairo wrapper class instance
            timeline (Timeline): Timeline object
            task_start_period (datetime): Task start date
            task_end_period (datetime): Task end date
        """
        self.box_x = 0
        row_match = 0
        bar_start_x_pos = 0

        for timeline_item in timeline.timeline_items:
            (
                timeline_start_period,
                timeline_end_period,
            ) = timeline_item.get_timeline_period(timeline.mode)
            if (
                (  # Check [timeline_start....<task_start>....timeline_end]
                    task_start_period >= timeline_start_period
                    and task_start_period <= timeline_end_period
                )
                or (  # Check [timeline_start....<task_end>....timeline_end]
                    task_end_period >= timeline_start_period
                    and task_end_period <= timeline_end_period
                )
                or (  # Check [<task_start>....[timeline_start....<task_end>.....timeline_end]
                    task_start_period <= timeline_start_period
                    and task_end_period >= timeline_end_period
                )
            ):
                (_, start_pos_percentage,) = timeline_item.get_timeline_pos_percentage(
                    timeline.mode,
                    task_start_period,
                )
                (_, end_pos_percentage,) = timeline_item.get_timeline_pos_percentage(
                    timeline.mode, task_end_period
                )
                row_match += 1

                # If this is the last period, calculate the width of the bar
                if (  # Check [timeline_start....<task_end>....timeline_end]
                    task_end_period >= timeline_start_period
                    and task_end_period <= timeline_end_period
                ):
                    # print("-->task_end is in this timeline")
                    if (
                        task_start_period >= timeline_start_period
                        and task_start_period <= timeline_end_period
                        and task_end_period >= timeline_start_period
                        and task_end_period <= timeline_end_period
                    ):
                        # print("-->task falls within this timeline")
                        self.box_x = timeline_item.box_x + (
                            timeline_item.box_width * start_pos_percentage
                        )
                        self.box_width = (
                            timeline_item.box_width * end_pos_percentage
                        ) - (timeline_item.box_width * start_pos_percentage)
                        # print(
                        #     f"[END] {self.box_x=}, {self.box_width=} = {timeline_item.box_width=} * {end_pos_percentage=}"
                        # )
                        bar_start_x_pos = self.box_x
                    else:
                        # print("-->task starts before this timeline")
                        self.box_x = timeline_item.box_x
                        if bar_start_x_pos == 0:
                            bar_start_x_pos = self.box_x
                        self.box_width = timeline_item.box_width * end_pos_percentage
                elif (  # Check [timeline_start....<task_start>.....timeline_end]
                    task_start_period >= timeline_start_period
                    and task_start_period <= timeline_end_period
                ):
                    # print("-->task_start is in this timeline")
                    self.box_x = timeline_item.box_x + (
                        timeline_item.box_width * start_pos_percentage
                    )
                    self.box_width = timeline_item.box_width - (
                        timeline_item.box_width * start_pos_percentage
                    )
                    bar_start_x_pos = self.box_x
                else:
                    # print("-->full bar")
                    self.box_x = timeline_item.box_x
                    self.box_width = timeline_item.box_width

                    if bar_start_x_pos == 0:
                        bar_start_x_pos = self.box_x

                    # print(f"[MIDDLE] {self.box_x=} {self.width=}")

                self.box_width += 1

                painter.set_colour(self.fill_colour)
                self.box_height = 20

                box_coordinates = [
                    self.box_x,
                    self.box_y,
                    self.box_width,
                    self.box_height,
                ]
                self.boxes.append(box_coordinates)

                bar_width = self.box_x + self.box_width - bar_start_x_pos
                painter.last_drawn_y_pos = self.box_y + self.box_height

        if row_match > 0:
            painter.set_font(self.font, self.font_size, self.font_colour)
            text_x_pos, text_y_pos = painter.get_display_text_position(
                bar_start_x_pos,
                self.box_y,
                bar_width,
                self.box_height,
                self.text,
                self.text_alignment,
            )
            self.text_x = text_x_pos
            self.text_y = text_y_pos

    def draw(self, painter: Painter) -> None:
        """Draw the task

        Args:
            painter (Painter): PyCairo wrapper class instance
        """
        painter.set_colour(self.fill_colour)
        for box in self.boxes:
            painter.draw_box(box[0], box[1], box[2], box[3])

        painter.set_font(self.font, self.font_size, self.font_colour)
        painter.draw_text(self.text_x, self.text_y, self.text)
        for milestone in self.milestones:
            milestone.draw(painter)

        for task in self.tasks:
            task.draw(painter)
