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
import calendar

from painter import Painter
from timelinemode import TimelineMode


@dataclass(kw_only=True)
class TimelineItem:
    text: str
    value: str
    start: datetime
    end: datetime
    box_x: int = field(init=False)
    box_y: int = field(init=False)
    box_width: int = field(init=False)
    box_height: int = field(init=False)
    text_x: int = field(init=False)
    text_y: int = field(init=False)
    font: str
    font_size: int
    font_colour: str
    fill_colour: str

    def __calculate_text_draw_position(self, painter: Painter):
        painter.set_font(self.font, self.font_size, self.font_colour)
        return painter.get_display_text_position(
            self.box_x, self.box_y, self.box_width, self.box_height, self.text, "centre"
        )

    def set_draw_position(
        self,
        painter: Painter,
        x: int,
        y: int,
        width: int,
        height: int,
    ):
        self.box_x = x
        self.box_y = y
        self.box_width = width
        self.box_height = height
        self.text_x, self.text_y = self.__calculate_text_draw_position(painter)
        painter.last_drawn_y_pos = self.box_y

    def get_timeline_period(self, mode: TimelineMode):
        start_date = self.start
        if mode == TimelineMode.WEEKLY:
            this_year = self.value[0:4]
            this_week = self.value[4:]
            timeline_start_period = date.fromisocalendar(
                int(this_year), int(this_week) + 1, 1
            )
            timeline_end_period = date.fromisocalendar(
                int(this_year), int(this_week) + 1, 7
            )

        if mode == TimelineMode.MONTHLY:

            this_year = int(self.value[0:4])
            this_month = int(self.value[4:])
            _, month_end_day = calendar.monthrange(this_year, this_month)
            timeline_start_period = datetime(this_year, this_month, 1)
            timeline_end_period = datetime(this_year, this_month, month_end_day)

        if mode == TimelineMode.QUARTERLY:
            this_year = self.value[0:4]
            this_quarter = self.value[4:]
            if this_quarter == 1:
                this_month = 1
            elif this_quarter == 2:
                this_month = 4
            elif this_quarter == 3:
                this_month = 7
            elif this_quarter == 4:
                this_month = 10

            timeline_start_period = datetime(
                this_year, 3 * ((this_month - 1) // 3) + 1, 1
            )
            timeline_end_period = datetime(
                this_year + 3 * this_quarter // 12, 3 * this_quarter % 12 + 1, 1
            ) + timedelta(days=-1)

        if mode == TimelineMode.HALF_YEARLY:
            this_year = self.value[0:4]
            this_half = self.value[4:]
            if this_half == 1:
                timeline_start_period = datetime(this_year, 1, 1)
                timeline_end_period = datetime(this_year, 6, 30)
            elif this_half == 2:
                timeline_start_period = datetime(this_year, 7, 1)
                timeline_end_period = datetime(this_year, 12, 31)

        if mode == TimelineMode.YEARLY:
            timeline_start_period = datetime(int(self.value), 1, 1)
            timeline_end_period = datetime(int(self.value), 12, 31)

        return timeline_start_period, timeline_end_period

    def get_timeline_pos_percentage(self, mode: TimelineMode, milestone_date):
        correct_timeline = False
        pos_percentage = 0
        timeline_start_period, timeline_end_period = self.get_timeline_period(mode)

        if mode == TimelineMode.WEEKLY:
            pos_percentage = milestone_date.weekday() / 7
            milestone_period = f"{milestone_date.year}{milestone_date.strftime('%W')}"
            this_period = (
                f"{timeline_start_period.year}{timeline_start_period.strftime('%W')}"
            )
            if milestone_period == this_period:
                correct_timeline = True

        if mode == TimelineMode.MONTHLY:
            _, last_day = calendar.monthrange(
                timeline_start_period.year, timeline_start_period.month
            )
            pos_percentage = round(milestone_date.day / last_day, 1)
            # print(f"{pos_percentage} = {milestone_date.day} / {last_day}")
            if (
                milestone_date.year == timeline_start_period.year
                and milestone_date.month == timeline_start_period.month
            ):
                correct_timeline = True

        if mode == TimelineMode.QUARTERLY:
            this_period = self.value

            if this_period[-1] == "1":
                pos_percentage = milestone_date.month / 3
            elif this_period[-1] == "2":
                pos_percentage = (milestone_date.month - 3) / 3
            elif this_period[-1] == "3":
                pos_percentage = (milestone_date.month - 6) / 3
            elif this_period[-1] == "4":
                pos_percentage = (milestone_date.month - 9) / 3

            milestone_period = (
                f"{milestone_date.year}{self.__get_quarter_from_date(milestone_date)}"
            )
            if milestone_period == this_period:
                correct_timeline = True

        if mode == TimelineMode.HALF_YEARLY:
            this_period = self.value

            if this_period[-1] == "1":
                pos_percentage = milestone_date.month / 6
            else:
                pos_percentage = (milestone_date.month - 6) / 6
            milestone_period = (
                f"{milestone_date.year}{self.__get_halfyear_from_date(milestone_date)}"
            )
            # print(f"Matching >> {milestone_period=} == {this_period=}")
            if milestone_period == this_period:
                correct_timeline = True

        if mode == TimelineMode.YEARLY:
            this_period = self.value
            pos_percentage = milestone_date.month / 12
            milestone_period = f"{milestone_date.year}"
            if milestone_period == this_period:
                correct_timeline = True

        return (correct_timeline, pos_percentage)

    def __get_quarter_from_date(self, date):
        return (date.month - 1) // 3 + 1

    def __get_halfyear_from_date(self, date):
        return (date.month - 1) // 6 + 1

    def draw(self, painter: Painter):
        painter.set_colour(self.fill_colour)
        painter.draw_box(
            self.box_x, self.box_y, self.box_width - 1, self.box_height
        )  # -1 is to draw the white line in between timeline items
        painter.set_colour(self.font_colour)
        painter.draw_text(self.text_x, self.text_y, self.text)
