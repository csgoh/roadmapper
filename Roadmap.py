from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass
import calendar
from painter import Painter
from print_dict import pd
from contextlib import contextmanager


@dataclass
class Title:
    text: str
    x: int
    y: int
    width: int
    height: int
    font: str
    font_size: int
    font_colour: str

    # CONSTANT
    __TITLE_Y_POS = 30

    def __init__(self, text: str, font="Arial", font_size=12, font_colour="Black"):
        self.text = text
        self.font = font
        self.font_size = font_size
        self.font_colour = font_colour
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

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


@dataclass
class Footer:
    text: str
    font: str
    font_size: int
    font_colour: str

    def __init__(self, text: str, font="Arial", font_size=12, font_colour="Black"):
        self.text = text
        self.font = font
        self.font_size = font_size
        self.font_colour = font_colour

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


@dataclass
class TimelineItem:
    text: str
    value: str
    start: datetime
    end: datetime
    box_x: int
    box_y: int
    box_width: int
    box_height: int
    text_x: int
    text_y: int
    text_width: int
    text_height: int
    font: str
    font_size: int
    font_colour: str

    def __init__(
        self,
        text: str,
        value: str,
        start: datetime,
        end: datetime,
        font: str,
        font_size: int,
        font_colour: str,
        fill_colour: str,
    ):
        self.text = text
        self.value = value
        self.start = start
        self.end = end

        self.box_x = 0
        self.box_y = 0
        self.box_width = 0
        self.box_height = 0
        self.text_x = 0
        self.text_y = 0
        self.text_width = 0
        self.text_height = 0

        self.font = font
        self.font_colour = font_colour
        self.font_size = font_size
        self.fill_colour = fill_colour

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


@dataclass
class Timeline:
    mode: str
    start: datetime
    number_of_items: int
    x: int
    y: int
    width: int
    height: int
    font: str
    font_size: int
    font_colour: str
    fill_colour: str
    timeline_items: list[TimelineItem]

    # Constant Variables
    __timeline_height = 20

    def __init__(
        self,
        timeline_dict: dict,
        mode=TimelineMode.MONTHLY,
        start=datetime.today(),
        number_of_items=12,
        font="Arial",
        font_size=10,
        font_colour="Black",
        fill_colour="lightgrey",
    ):
        self.mode = mode
        self.start = start
        self.number_of_items = number_of_items
        self.font = font
        self.font_size = font_size
        self.font_colour = font_colour
        self.fill_colour = fill_colour

        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.timeline_items = []

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
                timelineitem_text,
                timelineitem_value,
                timelineitem_start,
                timelineitem_end,
                self.font,
                self.font_size,
                self.font_colour,
                self.fill_colour,
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


@dataclass
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


@dataclass
class Task:
    text: str
    start: datetime
    end: datetime
    x: int
    y: int
    width: int
    height: int
    font: str
    font_size: int
    font_colour: str
    fill_colour: str
    milestones: list[Milestone]

    def __init__(
        self,
        text,
        start,
        end,
        font="Arial",
        font_size=12,
        font_colour="black",
        fill_colour="lightgreen",
    ) -> None:
        self.text = text
        self.start = start
        self.end = end
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.font = font
        self.font_size = font_size
        self.font_colour = font_colour
        self.fill_colour = fill_colour
        self.milestones = []

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


@dataclass
class Group:
    text: str
    x: int
    y: int
    weight: int
    height: int
    font: str
    font_size: int
    font_colour: str
    fill_colour: str
    tasks = list[Task]

    def __init__(self, text, font, font_size, font_colour, fill_colour) -> None:
        self.text = text
        self.font = font
        self.font_size = font_size
        self.font_colour = font_colour
        self.fill_colour = fill_colour

        self.x = 0
        self.y = 0
        self.weight = 0
        self.height = 0
        self.tasks = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def add_task(self, task: Task):
        self.tasks.append(task)
        # pd(self.tasks)


@dataclass
class Roadmap:
    width: int
    height: int
    title: Title
    timeline: Timeline
    groups: list[Group]
    footer: Footer

    # Private Variables
    __last_y_pos = 0

    # DEFAULT SETTINGS
    __TITLE_FONT = "Arial"
    __TITLE_FONT_SIZE = 18
    __TITLE_FONT_COLOUR = "Black"

    __FOOTER_FONT = "Arial"
    __FOOTER_FONT_SIZE = 18
    __FOOTER_FONT_COLOUR = "Black"

    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.__painter = Painter(width, height, "test.png")
        self.__painter.set_background_colour("White")

        self.timeline = []
        self.groups = []

    def set_title(
        self,
        text: str,
        font=__TITLE_FONT,
        font_size=__TITLE_FONT_SIZE,
        font_colour=__TITLE_FONT_COLOUR,
    ):
        self.title = Title(text, font, font_size, font_colour)
        self.title.text = text
        self.title.set_draw_position(self.__painter)

    def set_footer(
        self,
        text: str,
        font=__FOOTER_FONT,
        font_size=__FOOTER_FONT_SIZE,
        font_colour=__FOOTER_FONT_COLOUR,
    ):
        self.footer = Footer(text, font, font_size, font_colour)
        self.footer.text = text
        self.footer.set_draw_position(self.__painter, self.__last_y_pos)

    def set_timeline(self):
        timeline_dict = {}
        self.timeline = Timeline(timeline_dict)
        self.timeline.set_draw_position(self.__painter)
        return None

    def draw(self):
        self.title.draw(self.__painter)
        self.timeline.draw(self.__painter)
        self.footer.draw(self.__painter)

    def save(self):
        self.__painter.save_surface()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def add_group(self, group: Group):
        # pd(group.tasks)
        self.groups.append(group)
        # pd(self.groups)


def obj_to_string(obj, extra="    "):
    return (
        str(obj.__class__)
        + "\n"
        + "\n".join(
            (
                extra
                + (
                    str(item)
                    + " = "
                    + (
                        obj_to_string(obj.__dict__[item], extra + "    ")
                        if hasattr(obj.__dict__[item], "__dict__")
                        else str(obj.__dict__[item])
                    )
                )
                for item in sorted(obj.__dict__)
            )
        )
    )


if __name__ == "__main__":
    my_roadmap = Roadmap(1000, 512)
    my_roadmap.set_title("My Three Year Roadmap 2023~2025", font_size=18)
    my_roadmap.set_timeline()

    with Task("Task1", "2023-01-01", "2023-10-31") as task1:
        task1.add_milestone("Milestone 1", "2023-01-01", "Red")
        task1.add_milestone("Milestone 2", "2023-02-01", "Green")
        task1.add_milestone("Milestone 3", "2023-03-01", "Blue")

    with Task("Task2", "2023-01-01", "2023-10-31") as task2:
        task2.add_milestone("Milestone 4", "2023-01-01", "Red")
        task2.add_milestone("Milestone 5", "2023-02-01", "Green")
        task2.add_milestone("Milestone 6", "2023-03-01", "Blue")
    with Group("Group 1", "Arial", 18, "Black", "White") as group1:
        group1.add_task(task1)
        group1.add_task(task2)
    # pd(group1.tasks)
    my_roadmap.add_group(group1)

    my_roadmap.set_footer("this is footer", font_size=10)
    my_roadmap.draw()
    my_roadmap.save()
    # print(obj_to_string(my_roadmap.groups[0]))
    print(obj_to_string(my_roadmap.timeline))
    # pd(my_roadmap.timeline.timeline_items[0].__dict__["box_y"])

    # print(json.dumps(my_roadmap.__dict__))
