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

    text: str
    start: datetime
    end: datetime
    # x: int = 0
    # y: int = 0
    width: int = 0
    height: int = 0
    font: str = "Arial"
    font_size: int = 12
    font_colour: str = "Black"
    fill_colour: str = "LightGreen"
    text_alignment: str = "centre"

    def __post_init__(self):
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
        text,
        start,
        end,
        font="Arial",
        font_size=12,
        font_colour="Black",
        fill_colour="LightGreen",
        text_alignment="centre",
    ):
        """Add a parallel task to this task

        Args:
            text ([type]): [description]
            start ([type]): [description]
            end ([type]): [description]
            font (str, optional): [description]. Defaults to "Arial".
            font_size (int, optional): [description]. Defaults to 12.
            font_colour (str, optional): [description]. Defaults to "Black".
            fill_colour (str, optional): [description]. Defaults to "LightGreen".

        Yields:
            [type]: [description]
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
        text,
        date,
        font="Arial",
        font_size=12,
        font_colour="Red",
        fill_colour="Red",
        text_alignment="centre",
    ):
        self.milestones.append(
            Milestone(
                text, date, font, font_size, font_colour, fill_colour, text_alignment
            )
        )
        # pd(self.milestones)

    def set_draw_position(
        self, painter: Painter, group_x, last_drawn_y, timeline: Timeline
    ):
        if len(self.milestones) > 0:
            self.box_y = last_drawn_y + 15
        else:
            self.box_y = last_drawn_y + 2

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
        self, painter, timeline, task_start_period, task_end_period
    ):
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

                        # painter.draw_diamond(
                        #     bar_x_pos
                        #     + (timeline_item.box_width * milestone_pos_percentage)
                        #     - 8
                        #     - 3,
                        #     self.y - 3,
                        #     26,
                        #     26,
                        # )

                        width, _ = painter.get_text_dimension(milestone.text)
                        milestone.text_x = (
                            bar_x_pos
                            + (timeline_item.box_width * milestone_pos_percentage)
                            - (width / 3)
                        )
                        milestone.text_y = self.box_y - 6

                        painter.set_font(
                            milestone.font,
                            10,
                            milestone.font_colour,
                        )
                        # Draw milestone text
                        # painter.draw_text(
                        #     bar_x_pos
                        #     + (timeline_item.box_width * milestone_pos_percentage)
                        #     - (width / 3),
                        #     self.y - 6,
                        #     milestone.text,
                        # )

    def set_task_position(self, painter, timeline, task_start_period, task_end_period):
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

    def draw(self, painter: Painter):
        painter.set_colour(self.fill_colour)
        for box in self.boxes:
            painter.draw_box(box[0], box[1], box[2], box[3])

        painter.set_font(self.font, self.font_size, self.font_colour)
        painter.draw_text(self.text_x, self.text_y, self.text)
        for milestone in self.milestones:
            milestone.draw(painter)

        for task in self.tasks:
            task.draw(painter)
