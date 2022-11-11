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

    def get_timeline_period(self):
        start_date = self.start
        if self.timeline_mode == self.WEEKLY:
            this_year = self.value[0:4]
            this_week = self.value[4:]
            timeline_start_period = date.fromisocalendar(
                int(this_year), int(this_week) + 1, 1
            )
            timeline_end_period = date.fromisocalendar(
                int(this_year), int(this_week) + 1, 7
            )

        if self.timeline_mode == self.MONTHLY:

            this_year = self.value[0:4]
            this_month = self.value[4:]
            _, month_end_day = calendar.monthrange(this_year, this_month)
            timeline_start_period = datetime(this_year, this_month, 1)
            timeline_end_period = datetime(this_year, this_month, month_end_day)

        if self.timeline_mode == self.QUARTERLY:
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

        if self.timeline_mode == self.HALF_YEARLY:
            this_year = self.value[0:4]
            this_half = self.value[4:]
            if this_half == 1:
                timeline_start_period = datetime(this_year, 1, 1)
                timeline_end_period = datetime(this_year, 6, 30)
            elif this_half == 2:
                timeline_start_period = datetime(this_year, 7, 1)
                timeline_end_period = datetime(this_year, 12, 31)

        if self.timeline_mode == self.YEARLY:
            timeline_start_period = datetime(int(self.value), 1, 1)
            timeline_end_period = datetime(int(self.value), 12, 31)

        return timeline_start_period, timeline_end_period

    def get_timeline_pos_percentage(self, timeline_index, milestone_date):
        correct_timeline = False
        pos_percentage = 0
        timeline_start_period, timeline_end_period = self.__get_timeline_period(
            timeline_index
        )

    def draw(self, painter: Painter):
        painter.set_colour(self.fill_colour)
        painter.draw_box(self.box_x, self.box_y, self.box_width, self.box_height)
        painter.set_colour(self.font_colour)
        painter.draw_text(self.text_x, self.text_y, self.text)
