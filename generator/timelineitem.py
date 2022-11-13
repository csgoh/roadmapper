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

from generator.painter import Painter
from generator.timelinemode import TimelineMode


@dataclass(kw_only=True)
class TimelineItem:
    """Roadmap TimelineItem class"""

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

    def __calculate_text_draw_position(self, painter: Painter) -> tuple:
        """Calculate the text draw position based on the box position and size

        A Args:
            painter (Painter): PyCairo wrapper class instance

        Returns:
            tuple(int, int): (x, y) position of the text
        """

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
    ) -> None:
        """Set the draw position of the timeline item

        Args:
            painter (Painter): PyCairo wrapper class instance
            x (int): x position of the box
            y (int): y position of the box
            width (int): width of the box
            height (int): height of the box
        """
        self.box_x = x
        self.box_y = y
        self.box_width = width
        self.box_height = height
        self.text_x, self.text_y = self.__calculate_text_draw_position(painter)
        painter.last_drawn_y_pos = self.box_y

    def get_timeline_period(self, mode: TimelineMode) -> tuple:
        """Get the timeline period based on the timeline mode

        Args:
            mode (TimelineMode): Timeline mode

        Returns:
            tuple(datetime, datetime): start datetime and end datetime of the timeline period
        """
        start_date = self.start
        if mode == TimelineMode.WEEKLY:
            this_year = self.value[0:4]
            this_week = self.value[4:]
            timeline_start_period = datetime.combine(
                date.fromisocalendar(int(this_year), int(this_week), 1),
                datetime.min.time(),
            )
            timeline_start_period = timeline_start_period.replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            timeline_end_period = datetime.combine(
                date.fromisocalendar(int(this_year), int(this_week), 7),
                datetime.min.time(),
            )
            timeline_end_period = timeline_end_period.replace(
                hour=0, minute=0, second=0, microsecond=0
            )

        if mode == TimelineMode.MONTHLY:

            this_year = int(self.value[0:4])
            this_month = int(self.value[4:])
            _, month_end_day = calendar.monthrange(this_year, this_month)
            timeline_start_period = datetime(this_year, this_month, 1)
            timeline_end_period = datetime(this_year, this_month, month_end_day)

        if mode == TimelineMode.QUARTERLY:
            this_year = int(self.value[0:4])
            this_quarter = int(self.value[4:])
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
            this_year = int(self.value[0:4])
            this_half = int(self.value[4:])
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

    def get_timeline_pos_percentage(
        self, mode: TimelineMode, task_or_milestone_date: datetime
    ) -> float:
        """Get the timeline position percentage based on the task or milestone date

        Args:
            mode (TimelineMode): Timeline mode
            task_or_milestone_date (datetime): Task or milestone date

        Returns:
            float: Timeline position percentage
        """
        correct_timeline = False
        pos_percentage = 0
        timeline_start_period, timeline_end_period = self.get_timeline_period(mode)

        if mode == TimelineMode.WEEKLY:
            pos_percentage = task_or_milestone_date.weekday() / 7
            milestone_period = (
                f"{task_or_milestone_date.year}{task_or_milestone_date.strftime('%W')}"
            )
            this_period = (
                f"{timeline_start_period.year}{timeline_start_period.strftime('%W')}"
            )
            if milestone_period == this_period:
                correct_timeline = True

        if mode == TimelineMode.MONTHLY:
            _, last_day = calendar.monthrange(
                timeline_start_period.year, timeline_start_period.month
            )
            pos_percentage = round(task_or_milestone_date.day / last_day, 1)
            if (
                task_or_milestone_date.year == timeline_start_period.year
                and task_or_milestone_date.month == timeline_start_period.month
            ):
                correct_timeline = True

        if mode == TimelineMode.QUARTERLY:
            this_period = self.value
            this_year = int(this_period[0:4])
            this_quarter = int(this_period[4:])

            date_of_first_day_of_quarter = date(this_year, 1, 1)
            date_of_last_day_of_quarter = date(
                this_year, 3, calendar.monthrange(this_year, 3)[1]
            )

            if this_period[-1] == "1":
                date_of_first_day_of_quarter = datetime(this_year, 1, 1)
                date_of_last_day_of_quarter = datetime(
                    this_year, 3, calendar.monthrange(this_year, 3)[1]
                )
                days_in_quarter = (
                    date_of_last_day_of_quarter - date_of_first_day_of_quarter
                ).days
                days_progress_in_quarter = (
                    days_in_quarter
                    - (date_of_last_day_of_quarter - task_or_milestone_date).days
                )
                pos_percentage = days_progress_in_quarter / days_in_quarter
            elif this_period[-1] == "2":
                date_of_first_day_of_quarter = datetime(this_year, 4, 1)
                date_of_last_day_of_quarter = datetime(
                    this_year, 6, calendar.monthrange(this_year, 6)[1]
                )
                days_in_quarter = (
                    date_of_last_day_of_quarter - date_of_first_day_of_quarter
                ).days
                days_progress_in_quarter = (
                    days_in_quarter
                    - (date_of_last_day_of_quarter - task_or_milestone_date).days
                )
                pos_percentage = days_progress_in_quarter / days_in_quarter
            elif this_period[-1] == "3":
                date_of_first_day_of_quarter = datetime(this_year, 7, 1)
                date_of_last_day_of_quarter = datetime(
                    this_year, 9, calendar.monthrange(this_year, 9)[1]
                )
                days_in_quarter = (
                    date_of_last_day_of_quarter - date_of_first_day_of_quarter
                ).days
                days_progress_in_quarter = (
                    days_in_quarter
                    - (date_of_last_day_of_quarter - task_or_milestone_date).days
                )
                pos_percentage = days_progress_in_quarter / days_in_quarter
            elif this_period[-1] == "4":
                date_of_first_day_of_quarter = datetime(this_year, 10, 1)
                date_of_last_day_of_quarter = datetime(
                    this_year, 12, calendar.monthrange(this_year, 12)[1]
                )
                days_in_quarter = (
                    date_of_last_day_of_quarter - date_of_first_day_of_quarter
                ).days
                days_progress_in_quarter = (
                    days_in_quarter
                    - (date_of_last_day_of_quarter - task_or_milestone_date).days
                )
                pos_percentage = days_progress_in_quarter / days_in_quarter

            milestone_period = f"{task_or_milestone_date.year}{self.__get_quarter_from_date(task_or_milestone_date)}"
            if milestone_period == this_period:
                correct_timeline = True

        if mode == TimelineMode.HALF_YEARLY:
            this_period = self.value
            this_year = int(this_period[0:4])

            if this_period[-1] == "1":
                date_of_first_day_of_halfyear = datetime(this_year, 1, 1)
                date_of_last_day_of_halfyear = datetime(
                    this_year, 6, calendar.monthrange(this_year, 6)[1]
                )
                # calc number of days between first day of quarter and last day of quarter
                days_in_halfyear = (
                    date_of_last_day_of_halfyear - date_of_first_day_of_halfyear
                ).days
                days_progress_in_halfyear = (
                    days_in_halfyear
                    - (date_of_last_day_of_halfyear - task_or_milestone_date).days
                )
                pos_percentage = days_progress_in_halfyear / days_in_halfyear
            else:
                date_of_first_day_of_halfyear = datetime(this_year, 7, 1)
                date_of_last_day_of_halfyear = datetime(
                    this_year, 12, calendar.monthrange(this_year, 12)[1]
                )
                # calc number of days between first day of quarter and last day of quarter
                days_in_halfyear = (
                    date_of_last_day_of_halfyear - date_of_first_day_of_halfyear
                ).days
                days_progress_in_halfyear = (
                    days_in_halfyear
                    - (date_of_last_day_of_halfyear - task_or_milestone_date).days
                )
                pos_percentage = days_progress_in_halfyear / days_in_halfyear
            milestone_period = f"{task_or_milestone_date.year}{self.__get_halfyear_from_date(task_or_milestone_date)}"
            if milestone_period == this_period:
                correct_timeline = True

        if mode == TimelineMode.YEARLY:
            this_period = self.value
            this_year = int(this_period[0:4])
            date_of_first_day_of_year = datetime(this_year, 1, 1)
            date_of_last_day_of_year = datetime(
                this_year, 12, calendar.monthrange(this_year, 12)[1]
            )
            # calc number of days between first day of quarter and last day of quarter
            days_in_year = (date_of_last_day_of_year - date_of_first_day_of_year).days
            days_progress_in_year = (
                days_in_year - (date_of_last_day_of_year - task_or_milestone_date).days
            )
            pos_percentage = days_progress_in_year / days_in_year
            milestone_period = f"{task_or_milestone_date.year}"
            if milestone_period == this_period:
                correct_timeline = True

        return (correct_timeline, pos_percentage)

    def __get_quarter_from_date(self, date: datetime) -> int:
        """Returns the quarter of a given date

        Args:
            date (datetime): date

        Returns:
            int: quarter
        """
        return (date.month - 1) // 3 + 1

    def __get_halfyear_from_date(self, date: datetime) -> int:
        """Returns the halfyear of a given date

        Args:
            date (datetime): date

        Returns:
            int: halfyear
        """
        return (date.month - 1) // 6 + 1

    def draw(self, painter: Painter) -> None:
        """Draws the timeline

        Args:
            painter (Painter): PyCairo wrapper class instance
        """
        painter.set_colour(self.fill_colour)
        painter.draw_box(
            self.box_x, self.box_y, self.box_width - 1, self.box_height
        )  # -1 is to draw the white line in between timeline items
        painter.set_colour(self.font_colour)
        painter.draw_text(self.text_x, self.text_y, self.text)
