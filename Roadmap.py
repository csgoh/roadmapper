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
from painter import Painter
import calendar
import pprint


@dataclass(kw_only=True)
class Title:
    text: str
    x: int = field(init=False)
    y: int = field(init=False)
    width: int = field(init=False)
    height: int = field(init=False)
    font: str = field(default="Arial")
    font_size: int = 12
    font_colour: str = "Black"

    # CONSTANT
    __TITLE_Y_POS = 30

    def __calculate_draw_position(self, painter: Painter):
        self.width, self.height = painter.get_text_dimension(self.text)
        return (painter.width / 2) - self.width / 2, self.__TITLE_Y_POS + self.height

    def set_draw_position(self, painter: Painter):
        painter.set_font(self.font, self.font_size, self.font_colour)
        self.x, self.y = self.__calculate_draw_position(painter)
        painter.last_drawn_y_pos = self.y

    def draw(self, painter: Painter):
        painter.set_font(self.font, self.font_size, self.font_colour)
        painter.draw_text(self.x, self.y, self.text)


@dataclass(kw_only=True)
class Footer:
    text: str
    font: str = "Arial"
    font_size: int = 12
    font_colour: str = "Black"
    x: int = field(init=False)
    y: int = field(init=False)

    def __calculate_draw_position(self, painter: Painter):
        self.width, self.height = painter.get_text_dimension(self.text)
        # 20px is the marging between the last drawn item and the footer
        return (
            painter.width / 2
        ) - self.width / 2, painter.last_drawn_y_pos + self.height + 20

    def set_draw_position(self, painter: Painter, last_y_pos: int):
        painter.set_font(self.font, self.font_size, self.font_colour)
        self.x, self.y = self.__calculate_draw_position(painter)
        painter.last_drawn_y_pos = self.y

    def draw(self, painter: Painter):
        painter.set_font(self.font, self.font_size, self.font_colour)
        painter.draw_text(self.x, self.y, self.text)


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

    def draw(self, painter: Painter):
        painter.set_colour(self.fill_colour)
        painter.draw_box(self.box_x, self.box_y, self.box_width, self.box_height)
        painter.set_colour(self.font_colour)
        painter.draw_text(self.text_x, self.text_y, self.text)


@dataclass
class TimelineMode:
    WEEKLY = "W"
    MONTHLY = "M"
    QUARTERLY = "Q"
    HALF_YEARLY = "H"
    YEARLY = "Y"


@dataclass(kw_only=True)
class Timeline:
    mode: str = TimelineMode.MONTHLY
    start: datetime = datetime.today()
    number_of_items: int = 12
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

    def __calculate_draw_position(self, painter: Painter):
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

    def set_draw_position(self, painter: Painter):
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
        painter.last_drawn_y_pos = self.y + timelineitem_height

    def __get_timeline_item_text(self, index: int):
        timeline_text = ""
        if self.mode == TimelineMode.WEEKLY:
            this_week = self.start + relativedelta(weeks=+index)
            timeline_text = f"W{this_week.strftime('%W')} {this_week.year}"
        elif self.mode == TimelineMode.MONTHLY:
            this_month = self.start + relativedelta(months=+index)
            timeline_text = f"{this_month.strftime('%b')} {this_month.year}"
        elif self.mode == TimelineMode.QUARTERLY:
            this_month = self.start + relativedelta(months=+(index * 3))
            this_quarter = (this_month.month - 1) // 3 + 1
            timeline_text = f"Q{this_quarter} {this_month.year}"
        elif self.mode == TimelineMode.HALF_YEARLY:
            this_month = self.start + relativedelta(months=+(index * 6))
            this_halfyear = (this_month.month - 1) // 6 + 1
            timeline_text = f"H{this_halfyear} {this_month.year}"
        elif self.mode == TimelineMode.YEARLY:
            this_month = self.start + relativedelta(months=+(index * 12))
            timeline_text = f"{this_month.year}"
            timeline_value = f"{this_month.year}"

        return timeline_text

    def __get_timeline_item_value(self, index: int):
        timeline_value = ""
        if self.mode == TimelineMode.WEEKLY:
            this_week = self.start + relativedelta(weeks=+index)
            timeline_value = f"{this_week.year}{this_week.strftime('%W')}"
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

    def __get_timeline_item_dates(self, index: int):
        timeline_start_period = ""
        timeline_end_period = ""
        if self.mode == TimelineMode.WEEKLY:
            timeline_period = self.__get_timeline_item_value(index)
            this_year = timeline_period[0:4]
            this_week = timeline_period[4:]
            # print(f"{timeline_period=}, this_year={this_year} this_week={this_week}")
            timeline_start_period = date.fromisocalendar(
                int(this_year), int(this_week) + 1, 1
            )
            timeline_end_period = date.fromisocalendar(
                int(this_year), int(this_week) + 1, 7
            )
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

    def draw(self, painter: Painter):
        painter.set_font(self.font, self.font_size, self.font_colour)
        for i in range(0, self.number_of_items):

            timelineitem = self.timeline_items[i]
            timelineitem.draw(painter)


@dataclass(kw_only=True)
class Milestone:
    text: str
    date: datetime
    x: int
    y: int
    width: int
    height: int
    font: str
    font_size: int
    font_colour: str
    fill_colour: str

    def __init__(self, text, date, font, font_size, font_colour, fill_colour) -> None:
        self.text = text
        self.date = date
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.font = font
        self.font_size = font_size
        self.font_colour = font_colour
        self.fill_colour = fill_colour


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
    milestones: list[Milestone] = field(default_factory=list)

    def __enter__(self):
        print(f"Entering {self.text}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Exiting {self.text}")
        pass

    def add_milestone(
        self,
        text,
        date,
        font="Arial",
        font_size=12,
        font_colour="Red",
        fill_colour="Red",
    ):
        # print(f"Adding milestone {text}")
        self.milestones.append(
            Milestone(text, date, font, font_size, font_colour, fill_colour)
        )
        # pd(self.milestones)

    def draw(self, painter: Painter):
        pass


@dataclass
class Group:
    text: str
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    font: str = "Arial"
    font_size: int = 10
    font_colour: str = "black"
    fill_colour: str = "lightgrey"
    tasks: list[Task] = field(default_factory=list)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def add_task(self, task: Task):
        self.tasks.append(task)

    def draw(self, painter: Painter):
        # Step 1: draw tasks
        for tasks in self.tasks:
            tasks.draw(painter)

        # Step 2: draw group box


@dataclass()
class Roadmap:
    width: int = field(default=1200)
    height: int = field(default=600)
    title: Title = field(default=None, init=False)
    timeline: Timeline = field(default=None, init=False)
    groups: list[Group] = field(default_factory=list, init=False)
    footer: Footer = field(default=None, init=False)

    def __post_init__(self):
        self.__painter = Painter(self.width, self.height, "test.png")
        self.__painter.set_background_colour("White")
        self.__last_y_pos = 0

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
            mode=mode, start=start_date, number_of_items=number_of_items
        )
        (mode, start_date, number_of_items, font, font_size, font_colour, fill_colour)
        self.timeline.set_draw_position(self.__painter)
        return None

    def add_group(self, group: Group):
        self.groups.append(group)

    def draw(self):
        self.title.draw(self.__painter)
        self.timeline.draw(self.__painter)
        for group in self.groups:
            group.draw(self.__painter)
        self.footer.draw(self.__painter)

    def save(self):
        self.__painter.save_surface()


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=1, width=120, compact=True)

    my_roadmap = Roadmap(width=1000, height=512)
    my_roadmap.set_title("My Three Year Roadmap 2023-2025", font_size=18)
    my_roadmap.set_timeline(TimelineMode.MONTHLY, "2023-01-01", 12)

    with Task(text="Task1", start="2023-01-01", end="2023-10-31") as task1:
        task1.add_milestone(text="Milestone 1", date="2023-01-01", fill_colour="Red")
        task1.add_milestone("Milestone 2", "2023-02-01", fill_colour="Green")
        task1.add_milestone("Milestone 3", "2023-03-01", fill_colour="Blue")

    with Task(text="Task2", start="2023-01-01", end="2023-10-31") as task2:
        task2.add_milestone("Milestone 4", "2023-01-01")
        task2.add_milestone("Milestone 5", "2023-02-01")
        task2.add_milestone("Milestone 6", "2023-03-01")

    with Group("Group 1", "Arial", 18, "Black", "White") as group1:
        group1.add_task(task1)
        group1.add_task(task2)

    my_roadmap.add_group(group1)

    my_roadmap.set_footer("this is footer!!!!!", font_size=10)
    my_roadmap.draw()
    my_roadmap.save()
    pp.pprint(my_roadmap.groups)
