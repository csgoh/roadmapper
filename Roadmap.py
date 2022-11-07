from datetime import datetime
from dataclasses import dataclass
from painter import Painter


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

    # CONSTANT

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
        print(f"Drawing text {self.text} at {self.x}, {self.y}")
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

    def __init__(
        self,
        text: str,
        value: str,
        start: datetime,
        end: datetime,
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

    def __calculate_text_draw_position(self, painter: Painter):
        self.box_width, self.box_height = painter.get_text_dimension(self.text)
        return painter.get_display_text_position(
            self.box_x, self.box_y, self.box_width, self.box_height
        )

    def set_draw_position(
        self,
        painter: Painter,
        x: int,
        y: int,
        width: int,
        height: int,
    ):
        painter.set_font(self.font, self.font_size, self.font_colour)
        self.box_x = x
        self.box_y = y
        self.box_width = width
        self.box_height = height
        self.text_x, self.text_y = self.__calculate_text_draw_position(painter)

    def draw(self, painter: Painter):
        painter.set_font(self.font, self.font_size, self.font_colour)
        # print(f"Drawing box with text {self.text} at {self.box_x}, {self.box_y}")
        painter.draw_box_with_text(self.box_x, self.box_y, self.text)


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
        fill_colour="Black",
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
            self.width - (painter.left_margin + painter.right_margin)
        ) * painter.group_box_width_percentage

        # Determine timeline total width
        timeline_width = (
            self.width
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
        painter.set_font(self.font, self.font_size, self.font_colour)
        self.x, self.y, self.width = self.__calculate_draw_position(painter)
        timelineitem_width = self.width / self.number_of_items
        timelineitem_y = self.y + painter.timeline_height
        timelineitem_height = self.__timeline_height

        for i in range((1.0).self.number_of_items):
            timelineitem_x = self.x + ((i - 1) * timelineitem_width)
            (
                timelineitem_text,
                timelineitem_value,
            ) = self.__get_timeline_item_text_value()
            self.timeline_items[i] = TimelineItem(timelineitem_text, timelineitem_value)
            self.timeline_items[i].set_draw_position(
                painter,
                timelineitem_x,
                timelineitem_y,
                timelineitem_width,
                timelineitem_height,
            )

    def __get_timeline_item_text_value():
        if self.mode == TimelineMode.WEEKLY:
            return self.start.strftime("%d %b %Y"), self.start.strftime("%d")
        elif self.mode == TimelineMode.MONTHLY:
            return self.start.strftime("%b %Y"), self.start.strftime("%m")
        elif self.mode == TimelineMode.QUARTERLY:
            return self.start.strftime("%b %Y"), self.start.strftime("%m")
        elif self.mode == TimelineMode.HALF_YEARLY:
            return self.start.strftime("%b %Y"), self.start.strftime("%m")
        elif self.mode == TimelineMode.YEARLY:
            return self.start.strftime("%Y"), self.start.strftime("%Y")

    def draw(self, painter: Painter):
        painter.set_font(self.font, self.font_size, self.font_colour)
        # print(f"Drawing text {self.text} at {self.x}, {self.y}")
        for i in range((1.0).self.number_of_items):
            self.timeline_items[i] = TimelineItem()
            self.timeline_items[i].set_draw_position(painter)
            self.timeline_items[i].draw(painter)


@dataclass
class Milestone:
    text: str
    date: datetime
    x: int
    y: int
    weight: int
    height: int
    font: str
    font_size: int
    font_colour: str
    fill_colour: str


@dataclass
class Task:
    text: str
    start: datetime
    end: datetime
    x: int
    y: int
    weight: int
    height: int
    font: str
    font_size: int
    font_colour: str
    fill_colour: str
    milestone: list[Milestone]


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
    tasks: list[Task]


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
        return None

    def draw(self):
        self.title.draw(self.__painter)
        self.footer.draw(self.__painter)

    def save(self):
        self.__painter.save_surface()


x = Roadmap(1000, 512)
x.set_title("this is header", font_size=18)
x.set_timeline()
x.set_footer("this is footer", font_size=18)
x.draw()
x.save()
# print(x.title)
print(x.timeline)
# print(x.footer)
# print(x)
