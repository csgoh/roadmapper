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

from .painter import PainterFactory
from .title import Title
from .subtitle import SubTitle
from .footer import Footer
from .timelinemode import TimelineMode
from .timeline import Timeline
from .group import Group
from .marker import Marker
from .logo import Logo

import logging


@dataclass()
class Roadmap:
    """The main Roadmap class"""

    width: int = field(default=1200, init=True)
    height: int = field(default=600, init=True)
    auto_height: bool = field(default=True, init=True)
    colour_theme: str = field(default="DEFAULT", init=True)
    show_marker: bool = field(default=True, init=True)
    painter_type: str = field(default="png", init=True)

    _title: Title = field(default=None, init=False)
    _subtitle: SubTitle = field(default=None, init=False)
    _timeline: Timeline = field(default=None, init=False)
    _groups: list[Group] = field(default_factory=list, init=False)
    _footer: Footer = field(default=None, init=False)
    _marker: Marker = field(default=None, init=False)
    _show_generic_dates: bool = field(default=False, init=False)
    _logo: Logo = field(default=None, init=False)

    def __post_init__(self):
        """This method is called after __init__() is called"""
        logging.basicConfig(
            # filename="roadmapper.log",
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] : %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        self.start_time = time.time()
        factory = PainterFactory()
        self._painter = factory.get_painter(self.painter_type, self.width, self.height)
        self._set_colour_theme(self.colour_theme)
        self._groups = []
        if self.show_marker is True:
            self._create_marker()

    def _set_colour_theme(self, palette: str) -> None:
        """This method sets the colour palette"""
        self._painter.set_colour_theme(palette)

    def set_background_colour(self, colour: str) -> None:
        """This method sets the background colour"""
        self._painter.background_colour = colour
        self._painter.set_background_colour()

    def _create_marker(
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
        label_text_font = label_text_font or self._painter.marker_font
        label_text_size = label_text_size or self._painter.marker_font_size
        label_text_colour = label_text_colour or self._painter.marker_font_colour
        line_colour = line_colour or self._painter.marker_line_colour

        self._marker = Marker(
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

        label_text_font = label_text_font or self._painter.marker_font
        label_text_size = label_text_size or self._painter.marker_font_size
        label_text_colour = label_text_colour or self._painter.marker_font_colour
        line_colour = line_colour or self._painter.marker_line_colour

        self._marker.font = label_text_font
        self._marker.font_size = label_text_size
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

        font = font or self._painter.title_font
        font_size = font_size or self._painter.title_font_size
        font_colour = font_colour or self._painter.title_font_colour

        self._title = Title(
            text=text, font=font, font_size=font_size, font_colour=font_colour
        )
        self._title.text = text

        self._title.set_draw_position(self._painter)

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

        font = font or self._painter.subtitle_font
        font_size = font_size or self._painter.subtitle_font_size
        font_colour = font_colour or self._painter.subtitle_font_colour

        self._subtitle = SubTitle(
            text=text, font=font, font_size=font_size, font_colour=font_colour
        )
        self._subtitle.text = text

        self._subtitle.set_draw_position(self._painter)

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

        font = font or self._painter.footer_font
        font_size = font_size or self._painter.footer_font_size
        font_colour = font_colour or self._painter.footer_font_colour

        self._footer = Footer(
            text=text, font=font, font_size=font_size, font_colour=font_colour
        )
        self._footer.text = text

    def set_timeline(
        self,
        mode: TimelineMode = TimelineMode.MONTHLY,
        *,
        start: datetime = datetime.strptime(
            datetime.strftime(datetime.today(), "%Y-%m-%d"),
            "%Y-%m-%d",
        ),
        number_of_items: int = 12,
        show_generic_dates: bool = False,
        show_first_day_of_week: bool = False,
        ### v1.1.1 Remove default locale "en_US"
        timeline_locale: str = "",
        year_font: str = "",
        year_font_size: int = 0,
        year_font_colour: str = "",
        year_fill_colour: str = "",
        item_font: str = "",
        item_font_size: int = 0,
        item_font_colour: str = "",
        item_fill_colour: str = "",
    ) -> None:
        """Configure the timeline settings

        Args:
            mode (TimelineMode, optional): Timeline mode. Defaults to TimelineMode.MONTHLY.
                                            Options are WEEKLY, MONTHLY, QUARTERLY, HALF_YEARLY, YEARLY
            start (datetime, optional): Timeline start date. Defaults to current date
            number_of_items (int, optional): Number of time periods to display on the timeline. Defaults to 12.
            show_generic_dates (bool, optional): Show generic dates. Defaults to False.
            show_first_day_of_week (bool, optional): Show first day of week. Defaults to False. For this to work, show_generic_dates must set to False.
            timeline_locale (str, optional): Timeline locale file. Defaults to "en_US".
            font (str, optional): Timelinegroup font. Defaults to "DEFAULT" colour theme.
            font_size (int, optional): Timelinegroup font size. Defaults to "DEFAULT" colour theme.
            font_colour (str, optional): Timelinegroup font colour. Defaults to "DEFAULT" colour theme.
            fill_colour (str, optional): Timelinegroup fill colour. Defaults to "DEFAULT" colour theme.
            font (str, optional): Timeline font. Defaults to "DEFAULT" colour theme.
            font_size (int, optional): Timeline font size. Defaults to "DEFAULT" colour theme.
            font_colour (str, optional): Timeline font colour. Defaults to "DEFAULT" colour theme.
            fill_colour (str, optional): Timeline fill colour. Defaults to "DEFAULT" colour theme.
        """

        year_font = year_font or self._painter.timeline_year_font
        year_font_size = year_font_size or self._painter.timeline_year_font_size
        year_font_colour = year_font_colour or self._painter.timeline_year_font_colour
        year_fill_colour = year_fill_colour or self._painter.timeline_year_fill_colour

        item_font = item_font or self._painter.timeline_item_font
        item_font_size = item_font_size or self._painter.timeline_item_font_size
        item_font_colour = item_font_colour or self._painter.timeline_item_font_colour
        item_fill_colour = item_fill_colour or self._painter.timeline_item_fill_colour

        self._show_generic_dates = show_generic_dates
        start_date = datetime.strptime(start, "%Y-%m-%d")
        self._timeline = Timeline(
            mode=mode,
            start=start_date,
            locale_name=timeline_locale,
            number_of_items=number_of_items,
            show_generic_dates=show_generic_dates,
            show_first_day_of_week=show_first_day_of_week,
            year_font=year_font,
            year_font_size=year_font_size,
            year_font_colour=year_font_colour,
            year_fill_colour=year_fill_colour,
            item_font=item_font,
            item_font_size=item_font_size,
            item_font_colour=item_font_colour,
            item_fill_colour=item_fill_colour,
        )
        self._timeline.set_draw_position(self._painter)
        if self._marker is not None:
            self._marker.set_label_draw_position(self._painter, self._timeline)

    def add_logo(
        self,
        image: str,
        position: str = "top-right",
        width: int = 0,
        height: int = 0,
    ) -> None:
        """Add a logo to the roadmap

        Args:
            image (str): Image file path. See this page for supported image formats: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
            position (str): Position of the logo. Defaults to "top_right".
                            Options are top_left, top_centre, top_right, bottom_left, bottom_centre, bottom_right
            width (int, optional): Logo width. Defaults to image width.
            height (int, optional): Logo height. Defaults to image height.
        """
        self._logo = Logo(image=image, position=position, width=width, height=height)
        if self._logo is not None and self._logo.position[:10] == "top-centre":
            self._logo.set_draw_position(self._painter, self.auto_height)

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
        font = font or self._painter.group_font
        font_size = font_size or self._painter.group_font_size
        font_colour = font_colour or self._painter.group_font_colour
        fill_colour = fill_colour or self._painter.group_fill_colour

        group = Group(
            text=text,
            font=font,
            font_size=font_size,
            font_colour=font_colour,
            fill_colour=fill_colour,
            text_alignment=text_alignment,
            painter=self._painter,
        )
        self._groups.append(group)
        return group

    def draw(self) -> None:
        """Draw the roadmap"""

        ### Set the surface background colour
        self._painter.set_background_colour()

        ### Draw the roadmap title
        if self._title is None:
            raise ValueError("Title is not set. Please call set_title() to set title.")
        self._title.draw(self._painter)

        ### Draw the roadmap subtitle
        if self._subtitle is not None:
            self._subtitle.draw(self._painter)

        ### Draw the roadmap timeline
        if self._timeline is None:
            raise ValueError(
                "Timeline is not set. Please call set_timeline() to set timeline."
            )
        self._timeline.draw(self._painter)

        ### Set the roadmap groups draw position
        for group in self._groups:
            group.set_draw_position(self._painter, self._timeline)

        ### Draw timeline vertical lines on the roadmap
        self._timeline.draw_vertical_lines(self._painter)

        ### Draw the roadmap groups
        for group in self._groups:
            group.draw(self._painter)

        ### Draw the roadmap marker
        if self._marker is not None and self._show_generic_dates is False:
            self._marker.set_line_draw_position(self._painter)
            self._marker.draw(self._painter)

        ### Draw the roadmap footer
        if self._footer is not None:
            self._footer.set_draw_position(self._painter)
            self._footer.draw(self._painter)

        ### Draw logo

        if self._logo is not None:
            if self._logo.position[:10] != "top-centre":
                self._logo.set_draw_position(self._painter, self.auto_height)
            self._logo.draw(self._painter)

        ### Auto adjust the surface height
        if self.auto_height is True:
            self._painter.set_surface_size(
                self._painter.width, int(self._painter.next_y_pos)
            )

    def save(self, filename: str) -> None:
        """Save surface to file. The file type is determined by the Painter being used.

        Args:
            filename (str): result file name
        """

        try:
            self._painter.save_surface(filename)
        except Exception as e:
            print(f"Error saving roadmap to file...[{filename}]")
            print(f"Error: {e}")

        elapsed_time = (time.time() - self.start_time) * 1000
        print(f"Took [{elapsed_time:.2f}ms] to generate '{filename}' roadmap")

    def __enter__(self):
        """This method is called when the 'with' statement is used"""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """This method is called when the 'with' statement is used"""
        pass
