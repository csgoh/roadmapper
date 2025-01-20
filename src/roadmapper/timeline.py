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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass, field
import calendar

from .painter import Painter
from .timelineitem import TimelineItem
from .timelineitemyear import TimelineYear
from .timelinemode import TimelineMode
from .timelinelocale import TimelineLocale
from .helper import Helper


@dataclass(kw_only=True)
class Timeline:
    """Roadmap Timeline Class"""

    mode: str = field(init=True, default=None)
    start: datetime = field(init=True, default=None)
    locale_name: str = field(init=True, default=None)
    number_of_items: int = field(init=True, default=None)
    show_generic_dates: bool = field(init=True, default=None)
    show_first_day_of_week: bool = field(init=True, default=None)

    year_font: str = field(init=True, default=None)
    year_font_size: int = field(init=True, default=None)
    year_font_colour: str = field(init=True, default=None)
    year_fill_colour: str = field(init=True, default=None)
    item_font: str = field(init=True, default=None)
    item_font_size: int = field(init=True, default=None)
    item_font_colour: str = field(init=True, default=None)
    item_fill_colour: str = field(init=True, default=None)

    x: int = field(init=False, default=0)
    y: int = field(init=False, default=0)
    width: int = field(init=False, default=0)
    timeline_years: list[TimelineYear] = field(init=False, default_factory=list)
    timeline_items: list[TimelineItem] = field(init=False, default_factory=list)

    year_text_format: str = field(init=False)
    year_generic_text_format: str = field(init=False)
    half_year_text_format: str = field(init=False)
    quarter_text_format: str = field(init=False)
    month_text_format: str = field(init=False)
    month_generic_text_format: str = field(init=False)
    week_text_format: str = field(init=False)
    week_generic_text_format: str = field(init=False)

    def __calculate_draw_position(self, painter: Painter) -> tuple[int, int, int]:
        """Calculate the draw position of the timeline

        Args:
            painter (Painter): Pillow wrapper class instance

        Returns:
            tuple[int, int, int]: Timeline x, y, width
        """
        ### Determine group box width
        group_box_width = (
            painter.width - (painter.left_margin + painter.right_margin)
        ) * painter.group_box_width_percentage

        ### Determine timeline total width
        timeline_width = (
            painter.width
            - (painter.left_margin + painter.right_margin)
            - painter.gap_between_group_box_and_timeline
        ) * painter.timeline_width_percentage

        ### Determine timeline starting x position
        timeline_x = (
            painter.left_margin
            + painter.gap_between_group_box_and_timeline
            + group_box_width
        )

        ### Determine timeline starting y position
        timeline_y = painter.next_y_pos + painter.gap_between_timeline_and_title

        return timeline_x, timeline_y, timeline_width

    def set_locale(self, locale: str) -> None:
        """Set the locale of the timeline

        Args:
            locale (str): Locale
        """
        self.locale_settings = TimelineLocale(locale)
        (
            self.year_text_format,
            self.year_generic_text_format,
        ) = self.locale_settings.get_timeline_locale_settings("year")
        self.half_year_text_format = self.locale_settings.get_timeline_locale_settings(
            "half_year"
        )
        self.quarter_text_format = self.locale_settings.get_timeline_locale_settings(
            "quarter"
        )
        (
            self.month_text_format,
            self.month_generic_text_format,
        ) = self.locale_settings.get_timeline_locale_settings("month")
        (
            self.week_text_format,
            self.week_generic_text_format,
        ) = self.locale_settings.get_timeline_locale_settings("week")

    def set_draw_position(self, painter: Painter) -> None:
        """Set the draw position of the timeline

        Args:
            painter (Painter): Pillow wrapper class instance
        """
        self.set_locale(self.locale_name)
        self.x, self.y, self.width = self.__calculate_draw_position(painter)

        ### Calculate timelineitemgroup positions
        year_groups = {}

        for index in range(self.number_of_items):
            index_year = self.__get_timeline_item_value(index)[:4]
            Helper.printc(
                f"=>{index=}, {index_year=}",
                show_level="timeline1",
            )
            (
                timelineitemgroup_start,
                timelineitemgroup_end,
            ) = self.__get_timeline_item_dates(index)

            Helper.printc(
                f"Step 1 =>{timelineitemgroup_start=}, {timelineitemgroup_end=}",
                show_level="timeline1",
            )

            if self.show_generic_dates is False:
                if index_year in year_groups:
                    year_groups[index_year] += 1
                else:
                    year_groups[index_year] = 1
            else:
                generic_year = 1
                if self.mode == TimelineMode.WEEKLY:
                    if index >= 52:
                        generic_year += index // 52
                elif self.mode == TimelineMode.MONTHLY:
                    if index >= 12:
                        generic_year += index // 12
                elif self.mode == TimelineMode.QUARTERLY:
                    if index >= 4:
                        generic_year += index // 4
                elif self.mode == TimelineMode.HALF_YEARLY:
                    if index >= 2:
                        generic_year += index // 2
                elif self.mode == TimelineMode.YEARLY:
                    if index >= 1:
                        generic_year += index // 1

                if generic_year in year_groups:
                    year_groups[generic_year] += 1
                else:
                    year_groups[generic_year] = 1

        timelineitem_width = int(self.width / self.number_of_items) - (
            painter.gap_between_timeline_item / 2
        )

        # -- Get drawing positions for timeline items --
        if self.mode != TimelineMode.YEARLY:
            timelineitemgroup_y = self.y + painter.timeline_height
            timelineitemgroup_height = painter.timeline_height
            index = 0
            for year in year_groups:

                ##------------
                timelineitemgroup_x = (
                    self.x
                    + (index * timelineitem_width)
                    + (index * (painter.gap_between_timeline_item / 2))
                )
                ##------------

                timelineitemgroup_width = timelineitem_width * year_groups[year] + (
                    (painter.gap_between_timeline_item / 2) * (year_groups[year] - 1)
                )

                index += year_groups[year]

                timelinetimegroup = TimelineYear(
                    # text="Year " + str(year),
                    text=(
                        self.year_text_format.format(year)
                        if self.show_generic_dates is False
                        else self.year_generic_text_format.format(year)
                    ),
                    value=year,
                    start=timelineitemgroup_start,
                    end=timelineitemgroup_end,
                    font=self.year_font,
                    font_size=self.year_font_size,
                    font_colour=self.year_font_colour,
                    fill_colour=self.year_fill_colour,
                )
                timelinetimegroup.set_draw_position(
                    painter,
                    timelineitemgroup_x,
                    timelineitemgroup_y,
                    timelineitemgroup_width,
                    timelineitemgroup_height,
                )
                self.timeline_years.append(timelinetimegroup)

            painter.next_y_pos = (
                timelineitemgroup_y
                + timelineitemgroup_height
                + painter.gap_between_timeline_group_item
            )

        timelineitem_y = painter.next_y_pos
        timelineitem_height = painter.timeline_height

        for index in range(self.number_of_items):
            timelineitem_x = (
                self.x
                + (index * timelineitem_width)
                + (index * (painter.gap_between_timeline_item / 2))
            )
            timelineitem_text = self.__get_timeline_item_text(index)
            timelineitem_value = self.__get_timeline_item_value(index)
            Helper.printc(
                f"Step 2 A => {timelineitem_text=}, {timelineitem_value=}, {timelineitem_text=}, {timelineitem_value=}",
                show_level="timeline",
            )
            timelineitem_start, timelineitem_end = self.__get_timeline_item_dates(index)

            Helper.printc(
                f"Step 2 B => {timelineitem_text=}, {timelineitem_value=}, {timelineitem_start=}, {timelineitem_end=}",
                show_level="timeline",
            )

            timelineitem = TimelineItem(
                text=timelineitem_text,
                value=timelineitem_value,
                start=timelineitem_start,
                end=timelineitem_end,
                font=self.item_font,
                font_size=self.item_font_size,
                font_colour=self.item_font_colour,
                fill_colour=self.item_fill_colour,
            )
            timelineitem.set_draw_position(
                painter,
                timelineitem_x,
                timelineitem_y,
                timelineitem_width,
                timelineitem_height,
            )

            self.timeline_items.append(timelineitem)
        painter.next_y_pos = timelineitem_y + timelineitem_height

    def __get_monday_from_calendar_week(self, year, calendar_week):
        return datetime.strptime(f"{year}-{calendar_week}-1", "%Y-%W-%w").date()

    def __get_timeline_item_text(self, index: int) -> str:
        """Get the text of the timeline item

        Args:
            index (int): Index of the timeline item

        Returns:
            str: Timeline item text
        """
        timeline_text = ""
        if self.mode == TimelineMode.WEEKLY:
            if self.show_generic_dates is False:
                if self.show_first_day_of_week is False:
                    this_week = self.__find_first_day_of_week(
                        self.start
                    ) + relativedelta(weeks=+index)
                    this_week_number = int(this_week.strftime("%W"))

                    timeline_text = self.week_generic_text_format.format(
                        this_week_number
                    )
                else:
                    this_week = self.__find_first_day_of_week(
                        self.start
                    ) + relativedelta(weeks=+index)

                    this_week_number = int(this_week.strftime("%W"))
                    first_day_of_week = self.__get_monday_from_calendar_week(
                        this_week.year, this_week_number
                    )
                    this_day = first_day_of_week.strftime("%d")
                    this_month = first_day_of_week.strftime("%b")
                    timeline_text = self.week_text_format.format(this_day, this_month)

            else:
                ### show_generic_dates is True ###

                this_week = index + 1
                timeline_text = f"W {this_week}"
                timeline_text = self.week_generic_text_format.format(this_week)

        elif self.mode == TimelineMode.MONTHLY:
            if self.show_generic_dates is False:
                this_month = self.start + relativedelta(months=+index)
                # timeline_text = f"{this_month.strftime('%b')}"
                timeline_text = self.month_text_format.format(this_month.strftime("%b"))
            else:
                this_month = index + 1
                # timeline_text = f"Month {this_month}"
                timeline_text = self.month_generic_text_format.format(this_month)
        elif self.mode == TimelineMode.QUARTERLY:
            if self.show_generic_dates is False:
                this_month = self.start + relativedelta(months=+(index * 3))
                this_quarter = (this_month.month - 1) // 3 + 1
                # timeline_text = f"Q{this_quarter}"
            else:
                this_month = index * 3 + 1
                this_quarter = (this_month - 1) // 3 + 1
                # timeline_text = f"Quarter {this_quarter}"
            timeline_text = self.quarter_text_format.format(this_quarter)
        elif self.mode == TimelineMode.HALF_YEARLY:
            if self.show_generic_dates is False:
                this_month = self.start + relativedelta(months=+(index * 6))
                this_halfyear = (this_month.month - 1) // 6 + 1
                # timeline_text = f"H{this_halfyear}"
            else:
                this_month = index * 6 + 1
                this_halfyear = (this_month - 1) // 6 + 1
                # timeline_text = f"H{this_halfyear}"
            timeline_text = self.half_year_text_format.format(this_halfyear)
        elif self.mode == TimelineMode.YEARLY:
            if self.show_generic_dates is False:
                this_month = self.start + relativedelta(months=+(index * 12))
                # timeline_text = f"{this_month.year}"
                timeline_text = self.year_text_format.format(this_month.year)
            else:
                this_month = index * 12 + 1
                this_year = (this_month - 1) // 12 + 1
                # timeline_text = f"Year {this_year}"
                timeline_text = self.year_generic_text_format.format(this_year)

        return timeline_text

    def __find_first_day_of_week(self, this_date: datetime) -> datetime:
        _, _, day_of_week = this_date.isocalendar()
        Helper.printc(
            f"__find_first_day_of_week\t\t\t=={this_date=}, {day_of_week=}, return: {this_date - timedelta(days=day_of_week - 1)}",
            show_level="timeline",
        )
        return this_date - timedelta(days=day_of_week - 1)

    def __get_timeline_item_value(self, index: int) -> str:
        """Get the value of the timeline item

        Args:
            index (int): Index of the timeline item

        Returns:
            str: Value of the timeline item
        """

        timeline_value = ""
        if self.mode == TimelineMode.WEEKLY:
            ### When dealing with weeks, the actual week number is used regardless of whether show_generic_dates is set.

            ### if index > 52, then reset the index number to 1
            # index = index % 52

            this_week = self.__find_first_day_of_week(self.start) + relativedelta(
                weeks=+index
            )

            week_value = int(this_week.strftime("%W"))  # + 1

            Helper.printc(
                f"__get_timeline_item_value\t\t\t{self.start=}, {this_week=}, {week_value=}",
                show_level="timeline",
            )
            # calculate number of weeks for the year

            if week_value > 52:
                week_value = 1
                year_value = this_week.year + 1
            else:
                year_value = this_week.year
            timeline_value = f"{year_value}{week_value}"
            Helper.printc(
                f"__get_timeline_item_value\t\t\t{index} = {this_week=}, {week_value=}, {timeline_value=}",
                show_level="timeline",
            )
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
            ### timeline_period is in the format YYYYWW
            this_year = timeline_period[0:4]  ### First 4 characters
            this_week = timeline_period[4:]  ### Last 2 characters

            timeline_start_period = datetime.strptime(
                f"{this_year} {this_week} 1", "%G %V %u"
            )

            timeline_end_period = datetime.strptime(
                f"{this_year} {this_week} 7", "%G %V %u"
            )
            Helper.printc(
                f"\t#{this_week=}, {timeline_start_period=}, {timeline_end_period=}",
                show_level="timeline1",
            )
        elif self.mode == TimelineMode.MONTHLY:
            this_month = (self.start + relativedelta(months=+index)).month
            this_year = (self.start + relativedelta(months=+index)).year
            _, month_end_day = calendar.monthrange(this_year, this_month)
            timeline_start_period = datetime(this_year, this_month, 1)
            timeline_end_period = datetime(this_year, this_month, month_end_day)
        elif self.mode == TimelineMode.QUARTERLY:
            timeline_period = self.__get_timeline_item_value(index)
            this_year = int(timeline_period[0:4])
            this_quarter = int(timeline_period[4:])
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
            painter (Painter): Pillow wrapper class instance
        """
        for timelinegroup in self.timeline_years:
            timelinegroup.draw(painter)

        ### No longer needed.
        # for index, timelinegroup in enumerate(self.timeline_items_group):
        #     if index > 0:
        #         timelinegroup.draw_vertical_line(painter)

        for i in range(self.number_of_items):
            timelineitem = self.timeline_items[i]
            timelineitem.draw(painter)

    def draw_vertical_lines(self, painter: Painter) -> None:
        """Draw the timeline's vertical lines

        Args:
            painter (Painter): Pillow wrapper class instance
        """
        for i in range(self.number_of_items):
            if i > 0:
                timelineitem = self.timeline_items[i]
                timelineitem.draw_vertical_line(painter)
