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
import calendar

from roadmapper.painter import Painter
from roadmapper.timelineitem import TimelineItem
from roadmapper.timelinemode import TimelineMode


@dataclass(kw_only=True)
class Timeline:
    """Roadmap Timeline Class"""

    mode: str = TimelineMode.MONTHLY
    start: datetime = datetime.today()
    number_of_items: int = 12
    show_generic_dates: bool = False
    x: int = field(init=False)
    y: int = field(init=False)
    width: int = field(init=False)
    # height: int = field(init=False)
    font: str = "Arial"
    font_size: int = 12
    font_colour: str = "Black"
    fill_colour: str = "LightGray"
    timeline_items: list[TimelineItem] = field(default_factory=list)

    # Constant Variables
    __timeline_height = 20

    def __calculate_draw_position(self, painter: Painter) -> tuple[int, int, int]:
        """Calculate the draw position of the timeline

        Args:
            painter (Painter): PyCairo wrapper class instance

        Returns:
            tuple[int, int, int]: Timeline x, y, width
        """
        # Determine group box width
        group_box_width = (
            painter.width - (painter.left_margin + painter.right_margin)
        ) * painter.group_box_width_percentage

        # Determine timeline total width
        timeline_width = (
            painter.width
            - (painter.left_margin + painter.right_margin)
            - painter.gap_between_group_box_and_timeline
        ) * painter.timeline_width_percentage

        # Determine timeline starting x position
        timeline_x = (
            painter.left_margin
            + painter.gap_between_group_box_and_timeline
            + group_box_width
        )

        # Determine timeline starting y position
        timeline_y = painter.last_drawn_y_pos + painter.gap_between_timeline_and_title

        return timeline_x, timeline_y, timeline_width

    def set_draw_position(self, painter: Painter) -> None:
        """Set the draw position of the timeline

        Args:
            painter (Painter): PyCairo wrapper class instance
        """
        # painter.set_font(self.font, self.font_size, self.font_colour)
        self.x, self.y, self.width = self.__calculate_draw_position(painter)
        timelineitem_width = self.width / self.number_of_items
        timelineitem_y = self.y + painter.timeline_height
        timelineitem_height = self.__timeline_height

        for i in range(0, self.number_of_items):
            timelineitem_x = self.x + (i * timelineitem_width)
            timelineitem_text = self.__get_timeline_item_text(i)
            timelineitem_value = self.__get_timeline_item_value(i)
            timelineitem_start, timelineitem_end = self.__get_timeline_item_dates(i)

            timelineitem = TimelineItem(
                text=timelineitem_text,
                value=timelineitem_value,
                start=timelineitem_start,
                end=timelineitem_end,
                font=self.font,
                font_size=self.font_size,
                font_colour=self.font_colour,
                fill_colour=self.fill_colour,
            )

            timelineitem.set_draw_position(
                painter,
                timelineitem_x,
                timelineitem_y,
                timelineitem_width,
                timelineitem_height,
            )

            self.timeline_items.append(timelineitem)
        painter.last_drawn_y_pos = timelineitem_y + timelineitem_height

    def __get_timeline_item_text(self, index: int) -> str:
        """Get the text of the timeline item

        Args:
            index (int): Index of the timeline item

        Returns:
            str: Timeline item text
        """
        timeline_text = ""
        if self.mode == TimelineMode.WEEKLY:
            if self.show_generic_dates == False:
                this_week = self.start + relativedelta(weeks=+index)
                timeline_text = f"W{this_week.strftime('%W')} {this_week.year}"
            else:
                this_week = index + 1
                this_year = 1
                timeline_text = f"Week {this_week}"
        elif self.mode == TimelineMode.MONTHLY:
            if self.show_generic_dates == False:
                this_month = self.start + relativedelta(months=+index)
                timeline_text = f"{this_month.strftime('%b')} {this_month.year}"
            else:
                this_month = index + 1
                timeline_text = f"Month {this_month}"
        elif self.mode == TimelineMode.QUARTERLY:
            if self.show_generic_dates == False:
                this_month = self.start + relativedelta(months=+(index * 3))
                this_quarter = (this_month.month - 1) // 3 + 1
                timeline_text = f"Q{this_quarter} {this_month.year}"
            else:
                this_month = index * 3 + 1
                this_quarter = (this_month - 1) // 3 + 1
                timeline_text = f"Quarter {this_quarter}"
        elif self.mode == TimelineMode.HALF_YEARLY:
            if self.show_generic_dates == False:
                this_month = self.start + relativedelta(months=+(index * 6))
                this_halfyear = (this_month.month - 1) // 6 + 1
                timeline_text = f"H{this_halfyear} {this_month.year}"
            else:
                this_month = index * 6 + 1
                this_halfyear = (this_month - 1) // 6 + 1
                timeline_text = f"H{this_halfyear}"
        elif self.mode == TimelineMode.YEARLY:
            if self.show_generic_dates == False:
                this_month = self.start + relativedelta(months=+(index * 12))
                timeline_text = f"{this_month.year}"
            else:
                this_month = index * 12 + 1
                this_year = (this_month - 1) // 12 + 1
                timeline_text = f"Year {this_year}"

        return timeline_text

    def __get_timeline_item_value(self, index: int) -> str:
        """Get the value of the timeline item

        Args:
            index (int): Index of the timeline item

        Returns:
            str: Value of the timeline item
        """

        timeline_value = ""
        if self.mode == TimelineMode.WEEKLY:
            this_week = self.start + relativedelta(weeks=+index)
            week_value = int(this_week.strftime("%W"))
            timeline_value = f"{this_week.year}{week_value}"
            # print("week value: " + timeline_value)
        elif self.mode == TimelineMode.MONTHLY:
            this_month = self.start + relativedelta(months=+index)
            timeline_value = f"{this_month.year}{this_month.strftime('%m')}"
        elif self.mode == TimelineMode.QUARTERLY:
            this_month = self.start + relativedelta(months=+(index * 3))
            this_quarter = (this_month.month - 1) // 3 + 1
            timeline_value = f"{this_month.year}{this_quarter}"
        elif self.mode == TimelineMode.HALF_YEARLY:
            this_month = self.start + relativedelta(months=+(index * 6))
            this_halfyear = (this_month.month - 1) // 6 + 1
            timeline_value = f"{this_month.year}{this_halfyear}"
        elif self.mode == TimelineMode.YEARLY:
            this_month = self.start + relativedelta(months=+(index * 12))
            timeline_value = f"{this_month.year}"

        return timeline_value

    def __get_timeline_item_dates(self, index: int) -> tuple[datetime, datetime]:
        """Get the start and end dates of the timeline item

        Args:
            index (int): Index of the timeline item

        Returns:
            tuple[datetime, datetime]: Start and end dates of the timeline item
        """
        timeline_start_period = ""
        timeline_end_period = ""
        if self.mode == TimelineMode.WEEKLY:
            timeline_period = self.__get_timeline_item_value(index)
            this_year = timeline_period[0:4]
            this_week = timeline_period[4:]
            # print(f"{timeline_period=}, this_year={this_year} this_week={this_week}")
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
            # print(f"{timeline_start_period=}, {timeline_end_period=}")
        elif self.mode == TimelineMode.MONTHLY:
            this_month = (self.start + relativedelta(months=+index)).month
            this_year = (self.start + relativedelta(months=+index)).year
            _, month_end_day = calendar.monthrange(this_year, this_month)
            timeline_start_period = datetime(this_year, this_month, 1)
            timeline_end_period = datetime(this_year, this_month, month_end_day)
        elif self.mode == TimelineMode.QUARTERLY:
            timeline_period = self.__get_timeline_item_value(index)
            # print(f"timeline_period={timeline_period}")
            this_year = int(timeline_period[0:4])
            this_quarter = int(timeline_period[4:])
            # print(f"{this_year=}, {this_quarter=}")
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
        elif self.mode == TimelineMode.HALF_YEARLY:
            timeline_period = self.__get_timeline_item_value(index)
            this_year = int(timeline_period[0:4])
            this_half = int(timeline_period[4:])
            if this_half == 1:  # First Half
                timeline_start_period = datetime(this_year, 1, 1)
                timeline_end_period = datetime(this_year, 6, 30)
            elif this_half == 2:  # Second Half
                timeline_start_period = datetime(this_year, 7, 1)
                timeline_end_period = datetime(this_year, 12, 31)
        elif self.mode == TimelineMode.YEARLY:
            timeline_period = self.__get_timeline_item_value(index)
            timeline_start_period = datetime(int(timeline_period), 1, 1)
            timeline_end_period = datetime(int(timeline_period), 12, 31)
        return timeline_start_period, timeline_end_period

    def draw(self, painter: Painter) -> None:
        """Draw the timeline

        Args:
            painter (Painter): PyCairo wrapper class instance
        """
        painter.set_font(self.font, self.font_size, self.font_colour)
        for i in range(0, self.number_of_items):

            timelineitem = self.timeline_items[i]
            timelineitem.draw(painter)
