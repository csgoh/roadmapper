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

from datetime import datetime
from dataclasses import dataclass, field
from contextlib import contextmanager

from roadmapper.painter import Painter
from roadmapper.title import Title
from roadmapper.footer import Footer
from roadmapper.timelinemode import TimelineMode
from roadmapper.timeline import Timeline
from roadmapper.group import Group
from roadmapper.marker import Marker


@dataclass()
class Roadmap:
    """The main Roadmap class"""

    width: int = field(default=1200)
    height: int = field(default=600)
    title: Title = field(default=None, init=False)
    timeline: Timeline = field(default=None, init=False)
    groups: list[Group] = field(default_factory=list, init=False)
    footer: Footer = field(default=None, init=False)
    marker: Marker = field(default=None, init=False)

    __version__ = "v0.1.0-beta3"

    def __post_init__(self):
        """This method is called after __init__() is called"""
        self.__painter = Painter(self.width, self.height)
        self.__painter.set_background_colour("White")
        self.groups = []
        self.__last_y_pos = 0

    def set_marker(
        self,
        label_text_font: str = "Arial",
        label_text_colour: str = "Black",
        label_text_size: int = 10,
        line_colour: str = "Black",
        line_width: int = 2,
        line_style: str = "dashed",
    ) -> None:
        """Configure the marker settings

        Args:
            label_text_font (str, optional): Label text font. Defaults to "Arial".
            label_text_colour (str, optional): Label text colour. Defaults to "Black".
            label_text_size (int, optional): Label text size. Defaults to 10.
            line_colour (str, optional): Line colour. Defaults to "Black".
            line_width (int, optional): Line width. Defaults to 2.
            line_style (str, optional): Line style. Defaults to "solid". Options are "solid", "dashed"
        """
        self.marker = Marker(
            font=label_text_font,
            font_size=label_text_size,
            font_colour=label_text_colour,
            line_colour=line_colour,
            line_width=line_width,
            line_style=line_style,
        )
        self.show_current_date_marker = True

    def set_title(
        self,
        text: str,
        font: str = "Arial",
        font_size: int = 18,
        font_colour: str = "Black",
    ) -> None:
        """Configure the title settings

        Args:
            text (str): Title text
            font (str, optional): Title font. Defaults to "Arial".
            font_size (int, optional): Title font size. Defaults to 18.
            font_colour (str, optional): Title font colour. Defaults to "Black".
        """
        self.title = Title(
            text=text, font=font, font_size=font_size, font_colour=font_colour
        )
        self.title.text = text

        self.title.set_draw_position(self.__painter)

    def set_footer(
        self,
        text: str,
        font: str = "Arial",
        font_size: int = 12,
        font_colour: str = "Black",
    ) -> None:
        """Configure the footer settings

        Args:
            text (str): Footer text
            font (str, optional): Footer font. Defaults to "Arial".
            font_size (int, optional): Footer font size. Defaults to 18.
            font_colour (str, optional): Footer font colour. Defaults to "Black".
        """
        # set marker position first since we know the height of groups
        if self.marker != None:
            self.marker.set_line_draw_position(self.__painter)

        self.footer = Footer(
            text=text, font=font, font_size=font_size, font_colour=font_colour
        )
        self.footer.text = text
        # self.footer.set_draw_position(self.__painter, self.__last_y_pos)

    def set_timeline(
        self,
        mode: TimelineMode = TimelineMode.MONTHLY,
        start: datetime = datetime.strptime(
            datetime.strftime(datetime.today(), "%Y-%m-%d"), "%Y-%m-%d"
        ),
        number_of_items: int = 12,
        font: str = "Arial",
        font_size: int = 10,
        font_colour: str = "Black",
        fill_colour: str = "lightgrey",
    ) -> None:
        """Configure the timeline settings

        Args:
            mode (TimelineMode, optional): Timeline mode. Defaults to TimelineMode.MONTHLY.
                                            Options are WEEKLY, MONTHLY, QUARTERLY, HALF_YEARLY, YEARLY
            start (datetime, optional): Timeline start date. Defaults to current date
            number_of_items (int, optional): Number of time periods to display on the timeline. Defaults to 12.
            font (str, optional): Timeline font. Defaults to "Arial".
            font_size (int, optional): Timeline font size. Defaults to 10.
            font_colour (str, optional): Timeline font colour. Defaults to "Black".
            fill_colour (str, optional): Timeline fill colour. Defaults to "lightgrey".
        """
        start_date = datetime.strptime(start, "%Y-%m-%d")
        self.timeline = Timeline(
            mode=mode,
            start=start_date,
            number_of_items=number_of_items,
            font=font,
            font_size=font_size,
            font_colour=font_colour,
            fill_colour=fill_colour,
        )
        self.timeline.set_draw_position(self.__painter)
        if self.marker != None:
            self.marker.set_label_draw_position(self.__painter, self.timeline)

    # @contextmanager
    # def add_group(
    #     self,
    #     text: str,
    #     font: str = "Arial",
    #     font_size: int = 10,
    #     font_colour: str = "Black",
    #     fill_colour: str = "lightgrey",
    #     text_alignment: str = "centre",
    # ) -> Group:
    #     """Add new group to the roadmap

    #     Args:
    #         text (str): Group text
    #         font (str, optional): Group text font. Defaults to "Arial".
    #         font_size (int, optional): Group text font size. Defaults to 10.
    #         font_colour (str, optional): Group text font colour. Defaults to "Black".
    #         fill_colour (str, optional): Group fill colour. Defaults to "lightgrey".
    #         text_alignment (str, optional): Group text alignment. Defaults to "centre". Options are "left", "centre", "right"

    #     Yields:
    #         Group: A new group instance. Use this to add taks to the group
    #     """
    #     try:
    #         group = Group(
    #             text=text,
    #             font=font,
    #             font_size=font_size,
    #             font_colour=font_colour,
    #             fill_colour=fill_colour,
    #             text_alignment=text_alignment,
    #         )
    #         self.groups.append(group)
    #         yield group
    #     finally:
    #         group.set_draw_position(self.__painter, self.timeline)
    #         group = None

    def add_group(
        self,
        text: str,
        font: str = "Arial",
        font_size: int = 10,
        font_colour: str = "Black",
        fill_colour: str = "lightgrey",
        text_alignment: str = "centre",
    ) -> Group:
        """Add new group to the roadmap

        Args:
            text (str): Group text
            font (str, optional): Group text font. Defaults to "Arial".
            font_size (int, optional): Group text font size. Defaults to 10.
            font_colour (str, optional): Group text font colour. Defaults to "Black".
            fill_colour (str, optional): Group fill colour. Defaults to "lightgrey".
            text_alignment (str, optional): Group text alignment. Defaults to "centre". Options are "left", "centre", "right"

        Return:
            Group: A new group instance. Use this to add taks to the group
        """
        group = Group(
            text=text,
            font=font,
            font_size=font_size,
            font_colour=font_colour,
            fill_colour=fill_colour,
            text_alignment=text_alignment,
        )
        self.groups.append(group)
        # group.set_draw_position(self.__painter, self.timeline)

        return group

    def draw(self) -> None:
        """Draw the roadmap"""
        if self.title == None:
            raise ValueError("Title is not set. Please call set_title() to set title.")
        self.title.draw(self.__painter)

        if self.timeline == None:
            raise ValueError(
                "Timeline is not set. Please call set_timeline() to set timeline."
            )
        self.timeline.draw(self.__painter)

        for group in self.groups:
            group.set_draw_position(self.__painter, self.timeline)
            group.draw(self.__painter)

        if self.marker != None:
            self.marker.draw(self.__painter)

        if self.footer != None:
            self.footer.set_draw_position(self.__painter, self.timeline)
            self.footer.draw(self.__painter)

    def save(self, filename: str) -> None:
        """Save surface to PNG file

        Args:
            filename (str): PNG file name
        """
        self.__painter.save_surface(filename)

    def print_roadmap(self, print_area: str = "all") -> None:
        """Print the content of the roadmap

        Args:
            print_area (str, optional): Roadmap area to print. Defaults to "all". Options are "all", "title", "timeline", "groups", "footer"
        """
        dash = "─"
        space = " "
        if print_area == "all" or print_area == "title":
            print(f"Title={self.title.text}")

        if print_area == "all" or print_area == "timeline":
            print("Timeline:")
            for timeline_item in self.timeline.timeline_items:
                print(
                    f"└{dash*8}{timeline_item.text}, value={timeline_item.value}, "
                    f"box_x={round(timeline_item.box_x,2)}, box_y={timeline_item.box_y}, "
                    f"box_w={round(timeline_item.box_width,2)}, box_h={timeline_item.box_height}, "
                    f"text_x={round(timeline_item.text_x,2)}, text_y={timeline_item.text_y}"
                )

        if print_area == "all" or print_area == "groups":
            for group in self.groups:
                print(
                    f"Group: text={group.text}, x={round(group.box_x, 2)}, y={group.box_y},",
                    f"w={group.box_width}, h={group.box_height}",
                )
                for task in group.tasks:
                    print(
                        f"└{dash*8}{task.text}, start={task.start}, end={task.end}, "
                        f"x={round(task.box_x, 2)}, y={task.box_y}, w={round(task.box_width, 2)}, "
                        f"h={task.box_height}"
                    )
                    for milestone in task.milestones:
                        print(
                            f"{space*9}├{dash*4}{milestone.text}, date={milestone.date}, x={round(milestone.diamond_x, 2)}, "
                            f"y={milestone.diamond_y}, w={milestone.diamond_width}, h={milestone.diamond_height}, "
                            f"font_colour={milestone.font_colour}, fill_colour={milestone.fill_colour}"
                        )
                    for parellel_task in task.tasks:
                        print(
                            f"{space*9}└{dash*4}Parellel Task: {parellel_task.text}, start={parellel_task.start}, "
                            f"end={parellel_task.end}, x={round(parellel_task.box_x,2)}, y={round(parellel_task.box_y, 2)}, "
                            f"w={round(parellel_task.box_width, 2)}, h={round(parellel_task.box_height,2)}"
                        )
                        for parellel_task_milestone in parellel_task.milestones:
                            print(
                                f"{space*14}├{dash*4}{parellel_task_milestone.text}, "
                                f"date={parellel_task_milestone.date}, x={round(parellel_task_milestone.diamond_x, 2)}, "
                                f"y={round(parellel_task_milestone.diamond_y, 2)}, w={parellel_task_milestone.diamond_width}, "
                                f"h={parellel_task_milestone.diamond_height}"
                            )
        if print_area == "all" or print_area == "footer":
            if self.footer != None:
                print(
                    f"Footer: {self.footer.text} x={self.footer.x} "
                    f"y={self.footer.y} w={self.footer.width} "
                    f"h={self.footer.height}"
                )
