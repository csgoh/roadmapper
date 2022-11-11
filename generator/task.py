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

from painter import Painter
from timeline import Timeline
from milestone import Milestone


@dataclass(kw_only=True)
class Task:

    text: str
    start: datetime
    end: datetime
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    font: str = "Arial"
    font_size: int = 12
    font_colour: str = "Black"
    fill_colour: str = "LightGreen"

    def __post_init__(self):
        self.milestones = []
        self.tasks = []

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
    ):
        self.milestones.append(
            Milestone(text, date, font, font_size, font_colour, fill_colour)
        )
        # pd(self.milestones)

    def set_draw_position(
        self, painter: Painter, group_x, last_drawn_y, timeline: Timeline
    ):
        if len(self.milestones) > 0:
            self.y = last_drawn_y + 15
        else:
            self.y = last_drawn_y

        # task_x = group_x + group_width + painter.gap_between_group_box_and_timeline

        task_start_period = datetime.strptime(self.start, "%Y-%m-%d")
        task_end_period = datetime.strptime(self.end, "%Y-%m-%d")

        bar_x_pos = 0
        row_match = 0
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
                if bar_x_pos == 0:
                    # Check if task starts before timeline
                    if task_start_period < timeline_start_period:
                        bar_x_pos = timeline_item.box_x
                    else:
                        bar_x_pos = timeline_item.box_x + (
                            timeline_item.box_width * start_pos_percentage
                        )
                    bar_start_x_pos = bar_x_pos
                else:
                    bar_x_pos = timeline_item.box_x

                print(f"{start_pos_percentage=},{end_pos_percentage=}")
                # If this is the last period, calculate the width of the bar
                if (  # Check [timeline_start....<task_end>....timeline_end]
                    task_end_period >= timeline_start_period
                    and task_end_period <= timeline_end_period
                ):
                    print("-->task_end is in this timeline")
                    task_timeline_width = timeline_item.box_width * end_pos_percentage
                elif (
                    task_start_period >= timeline_start_period
                    and task_start_period <= timeline_end_period
                ):
                    print("-->task_start is in this timeline")
                    bar_x_pos = timeline_item.box_x + (
                        timeline_item.box_width * start_pos_percentage
                    )
                    task_timeline_width = timeline_item.box_width - (
                        timeline_item.box_width * start_pos_percentage
                    )
                    # bar_x_pos = (
                    #     timeline_item.box_x
                    #     + timeline_item.box_width
                    #     - task_timeline_width
                    # )
                    print(
                        f"{bar_x_pos} = {timeline_item.box_x} + {timeline_item.box_width} - {task_timeline_width}"
                    )
                else:
                    print("-->full bar")
                    task_timeline_width = timeline_item.box_width

                task_timeline_width += 1

                # task_timeline_width += self.__HSPACER * (row_match)
                # print(f"bar {bar_x_pos=}, {task_timeline_width=}")

                painter.set_colour(self.fill_colour)
                # task_box_y_pos = next_task_y_pos
                # task_box_height = text_height
                _, text_height = painter.get_text_dimension(self.text)
                text_height = 20
                painter.draw_box(
                    bar_x_pos,
                    self.y,
                    task_timeline_width,
                    text_height,
                )
                print(
                    f"{self.text}: {timeline_start_period=}, {timeline_end_period=}, {task_start_period=}, {task_end_period=}, {bar_x_pos=}, {self.y=}, {task_timeline_width=}"
                )

                bar_width = bar_x_pos + task_timeline_width - bar_start_x_pos
                painter.last_drawn_y_pos = self.y + text_height

        # painter.draw_box(task_x, task_y, task_width, task_height)

    def draw(self, painter: Painter):
        pass
