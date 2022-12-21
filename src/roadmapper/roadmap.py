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
import time

# from contextlib import contextmanager

from roadmapper.painter import Painter
from roadmapper.title import Title
from roadmapper.subtitle import SubTitle
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
    auto_height: bool = field(default=True)
    colour_theme: str = field(default="DEFAULT")
    show_marker: bool = field(default=True)

    title: Title = field(default=None, init=False)
    subtitle: SubTitle = field(default=None, init=False)
    timeline: Timeline = field(default=None, init=False)
    groups: list[Group] = field(default_factory=list, init=False)
    footer: Footer = field(default=None, init=False)
    marker: Marker = field(default=None, init=False)
    show_generic_dates: bool = field(default=False, init=False)

    __version__ = "v0.2.0"

    def __post_init__(self):
        """This method is called after __init__() is called"""
        self.__painter = Painter(self.width, self.height)
        self.__set_colour_palette(self.colour_theme)
        self.groups = []
        if self.show_marker == True:
            self.__create_marker()

    def __set_colour_palette(self, palette: str) -> None:
        """This method sets the colour palette"""
        self.__painter.set_colour_palette(palette)

    def __create_marker(
        self,
        label_text_font: str = "",
        label_text_colour: str = "",
        label_text_size: int = 0,
        line_colour: str = "",
        line_width: int = 2,
        line_style: str = "dashed",
    ) -> None:
        """Add and configure the marker settings

        Args:
            label_text_font (str, optional): Label text font. Defaults to "Arial".
            label_text_colour (str, optional): Label text colour. Defaults to "Black".
            label_text_size (int, optional): Label text size. Defaults to 10.
            line_colour (str, optional): Line colour. Defaults to "Black".
            line_width (int, optional): Line width. Defaults to 2.
            line_style (str, optional): Line style. Defaults to "solid". Options are "solid", "dashed"
        """
        if label_text_font == "":
            label_text_font = self.__painter.marker_font
        if label_text_size == 0:
            label_text_size = self.__painter.marker_font_size
        if label_text_colour == "":
            label_text_colour = self.__painter.marker_font_colour
        if line_colour == "":
            line_colour = self.__painter.marker_line_colour

        self.marker = Marker(
            font=label_text_font,
            font_size=label_text_size,
            font_colour=label_text_colour,
            line_colour=line_colour,
            line_width=line_width,
            line_style=line_style,
        )

    def set_marker(
        self,
        label_text_font: str = "",
        label_text_colour: str = "",
        label_text_size: int = 0,
        line_colour: str = "",
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
        if label_text_font == "":
            label_text_font = self.__painter.marker_font
        if label_text_size == 0:
            label_text_size = self.__painter.marker_font_size
        if label_text_colour == "":
            label_text_colour = self.__painter.marker_font_colour
        if line_colour == "":
            line_colour = self.__painter.marker_line_colour

        self.marker.font = label_text_font
        self.marker.font_size = label_text_size
        self.font_colour = label_text_colour
        self.line_colour = line_colour
        self.line_width = line_width
        self.line_style = line_style

    def set_title(
        self,
        text: str,
        font: str = "",
        font_size: int = 0,
        font_colour: str = "",
    ) -> None:
        """Configure the title settings

        Args:
            text (str): Title text
            font (str, optional): Title font. Defaults to "Arial".
            font_size (int, optional): Title font size. Defaults to 18.
            font_colour (str, optional): Title font colour. Defaults to "Black".
        """
        if font == "":
            font = self.__painter.title_font
        if font_size == 0:
            font_size = self.__painter.title_font_size
        if font_colour == "":
            font_colour = self.__painter.title_font_colour

        self.title = Title(
            text=text, font=font, font_size=font_size, font_colour=font_colour
        )
        self.title.text = text

        self.title.set_draw_position(self.__painter)

    def set_subtitle(
        self,
        text: str,
        font: str = "",
        font_size: int = 0,
        font_colour: str = "",
    ) -> None:
        """Configure the subtitle settings

        Args:
            text (str): Title text
            font (str, optional): Title font. Defaults to "Arial".
            font_size (int, optional): Title font size. Defaults to 18.
            font_colour (str, optional): Title font colour. Defaults to "Black".
        """
        if font == "":
            font = self.__painter.subtitle_font
        if font_size == 0:
            font_size = self.__painter.subtitle_font_size
        if font_colour == "":
            font_colour = self.__painter.subtitle_font_colour

        self.subtitle = SubTitle(
            text=text, font=font, font_size=font_size, font_colour=font_colour
        )
        self.subtitle.text = text

        self.subtitle.set_draw_position(self.__painter)

    def set_footer(
        self,
        text: str,
        font: str = "",
        font_size: int = 0,
        font_colour: str = "",
    ) -> None:
        """Configure the footer settings

        Args:
            text (str): Footer text
            font (str, optional): Footer font. Defaults to "Arial".
            font_size (int, optional): Footer font size. Defaults to 18.
            font_colour (str, optional): Footer font colour. Defaults to "Black".
        """
        if font == "":
            font = self.__painter.footer_font
        if font_size == 0:
            font_size = self.__painter.footer_font_size
        if font_colour == "":
            font_colour = self.__painter.footer_font_colour

        self.footer = Footer(
            text=text, font=font, font_size=font_size, font_colour=font_colour
        )
        self.footer.text = text

    def set_timeline(
        self,
        mode: TimelineMode = TimelineMode.MONTHLY,
        start: datetime = datetime.strptime(
            datetime.strftime(datetime.today(), "%Y-%m-%d"), "%Y-%m-%d"
        ),
        number_of_items: int = 12,
        show_generic_dates: bool = False,
        font: str = "",
        font_size: int = 0,
        font_colour: str = "",
        fill_colour: str = "",
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
        if font == "":
            font = self.__painter.timeline_font
        if font_size == 0:
            font_size = self.__painter.timeline_font_size
        if font_colour == "":
            font_colour = self.__painter.timeline_font_colour
        if fill_colour == "":
            fill_colour = self.__painter.timeline_fill_colour

        self.show_generic_dates = show_generic_dates
        start_date = datetime.strptime(start, "%Y-%m-%d")
        self.timeline = Timeline(
            mode=mode,
            start=start_date,
            number_of_items=number_of_items,
            show_generic_dates=show_generic_dates,
            font=font,
            font_size=font_size,
            font_colour=font_colour,
            fill_colour=fill_colour,
        )
        self.timeline.set_draw_position(self.__painter)
        if self.marker != None:
            self.marker.set_label_draw_position(self.__painter, self.timeline)

    def add_group(
        self,
        text: str,
        font: str = "",
        font_size: int = 0,
        font_colour: str = "",
        fill_colour: str = "",
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
        if font == "":
            font = self.__painter.group_font
        if font_size == 0:
            font_size = self.__painter.group_font_size
        if font_colour == "":
            font_colour = self.__painter.group_font_colour
        if fill_colour == "":
            fill_colour = self.__painter.group_fill_colour

        group = Group(
            text=text,
            font=font,
            font_size=font_size,
            font_colour=font_colour,
            fill_colour=fill_colour,
            text_alignment=text_alignment,
            painter=self.__painter,
        )
        self.groups.append(group)
        return group

    def draw(self) -> None:
        """Draw the roadmap"""

        start_time = time.time()

        self.__painter.set_background_colour()

        if self.title == None:
            raise ValueError("Title is not set. Please call set_title() to set title.")
        self.title.draw(self.__painter)

        if self.subtitle != None:
            self.subtitle.draw(self.__painter)

        if self.timeline == None:
            raise ValueError(
                "Timeline is not set. Please call set_timeline() to set timeline."
            )
        self.timeline.draw(self.__painter)

        for group in self.groups:
            group.set_draw_position(self.__painter, self.timeline)

        self.timeline.draw_vertical_lines(self.__painter)

        for group in self.groups:
            group.draw(self.__painter)

        if self.marker != None and self.show_generic_dates == False:
            self.marker.set_line_draw_position(self.__painter)
            self.marker.draw(self.__painter)

        if self.footer != None:
            self.footer.set_draw_position(self.__painter)
            self.footer.draw(self.__painter)

        if self.auto_height == True:
            self.__painter.set_surface_size(
                self.__painter.width, int(self.__painter.last_drawn_y_pos)
            )

        elapsed_time = (time.time() - start_time) * 1000
        print("Drawing time: %.3f ms" % elapsed_time)

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
