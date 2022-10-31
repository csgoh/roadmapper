# Mahere Kaihanga / Roadmap Generator
# Copyright (C) 2022 Cheng Soon Goh
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

""" To do
        * Show milestones
        * Proporsion task bar according to the start and end date
        * Display current date marker
        * Allow task text to wrap around multiple lines, hence auto enlarge the task bar height
        * Auto expand surface canvas size if the task bar is too long
        * Implement logging
        * Implement class methods to allow user to add task, group, milestone, etc
        * Custom timeline start date

        Done * Make timeline 'colour' element optional
        Done * Make group 'colour' element optional
        Done * Make timeline 'colour' element optional
        Done * Option to turn off footer
        Done * Modularise method lines
        Done * Display task text on top of bar
        Done * Display group text as a block
        Done * Week, Quarter, Half Year, Year timeline mode support
        Done * Save as PDF
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
from painter import Painter
import glom
from print_dict import pd


class Mahere:
    # Private variables
    __VSPACER = 12
    __HSPACER = 2
    __DEFAULT_TITLE_TEXT_COLOUR = "Black"

    __DEFAULT_TIMELINE_FILL_COLOUR = "#006699"
    __DEFAULT_TIMELINE_TEXT_COLOUR = "White"

    __DEFAULT_GROUP_FILL_COLOUR = "#4dc3ff"
    __DEFAULT_GROUP_TEXT_COLOUR = "Black"

    __DEFAULT_TASK_FILL_COLOUR = "#b3e6ff"
    __DEFAULT_TASK_TEXT_COLOUR = "Black"

    __DEFAULT_FOOTER_TEXT_COLOUR = "Black"

    # Constant variables
    VERSION = "0.1"
    WEEKLY = "W"
    MONTHLY = "M"
    QUARTERLY = "Q"
    HALF_YEARLY = "H"
    YEARLY = "Y"

    class __RoadMapDict:
        roadmap_dict = {}

        def __init__(self) -> None:
            self.roadmap_dict["recommended_height"] = 0

        def add_to_recommended_height(self, height):
            self.roadmap_dict["recommended_height"] = height

        def set_title_coordinates(self, x, y, width, height, title_text):
            self.roadmap_dict["title"] = {
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                "text": title_text,
            }
            self.add_to_recommended_height(y + height)

        def set_timeline_coordinates(self, x, y, width, height):
            if self.roadmap_dict.get("timeline", {}).get("x", 0) == 0:
                self.roadmap_dict["timeline"] = {
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    "timeline_items": {},
                }
            self.add_to_recommended_height(y + height)

        def set_timeline_item_coordinates(self, item_id, x, y, width, height):
            # print (f"item: {item}, x: {x}, y: {y}, width: {width}, height: {height}")

            (
                current_x,
                current_y,
                current_width,
                current_height,
            ) = self.get_timeline_coordinates()

            if current_x == 0:
                current_x = x
            if current_y == 0:
                current_y = y
            if current_width < width:
                current_width = x + width
            if current_height < height:
                current_height = y + height

            self.set_timeline_coordinates(
                current_x, current_y, current_width, current_height
            )

            item = {"x": x, "y": y, "width": width, "height": height}

            self.roadmap_dict["timeline"]["timeline_items"][item_id] = item
            self.add_to_recommended_height(y + height)

        def get_timeline_item_text(self, item_id):
            return self.roadmap_dict["timeline"]["timeline_items"][item_id]["text"]

        def set_timeline_item_text(self, item_id, text):
            self.roadmap_dict["timeline"]["timeline_items"][item_id]["text"] = text

        def get_timeline_item_value(self, item_id):
            return self.roadmap_dict["timeline"]["timeline_items"][item_id]["value"]

        def set_timeline_item_value(self, item_id, value):
            self.roadmap_dict["timeline"]["timeline_items"][item_id]["value"] = value

        def get_timeline_item_position(self, item_id):
            return (
                self.roadmap_dict["timeline"]["timeline_items"][item_id]["x"],
                self.roadmap_dict["timeline"]["timeline_items"][item_id]["y"],
                self.roadmap_dict["timeline"]["timeline_items"][item_id]["width"],
                self.roadmap_dict["timeline"]["timeline_items"][item_id]["height"],
            )

        def set_groups_coordinates(self, x, y, width, height):
            if self.roadmap_dict.get("groups", {}).get("x", 0) == 0:
                self.roadmap_dict["groups"] = {
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    "group_items": {},
                }
            self.add_to_recommended_height(y + height)

        def set_groups_item_coordinates(self, item_id, x, y, width, height):

            (
                current_x,
                current_y,
                current_width,
                current_height,
            ) = self.get_groups_coordinates()
            if current_x == 0:
                current_x = x
            if current_y == 0:
                current_y = y
            if current_width < width:
                current_width = x + width
            if current_height < height:
                current_height = y + height

            self.set_groups_coordinates(
                current_x, current_y, current_width, current_height
            )
            if self.roadmap_dict["groups"]["group_items"].get(item_id, None) == None:
                self.roadmap_dict["groups"]["group_items"][item_id] = {
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    "tasks": {},
                }
            # self.roadmap_dict["groups"]["group_items"][item_id] = {"x": x, "y": y, "width": width, "height": height, "tasks": {}}

        def set_groups_item_task_coordinates(
            self, item_id, task_id, x, y, width, height, task_text
        ):
            current_x = 0
            current_y = 0
            current_width = 0
            current_height = 0
            if item_id > 0:
                (
                    current_x,
                    current_y,
                    current_width,
                    current_height,
                ) = self.get_groups_item_coordinates(item_id)
            if current_x == 0:
                current_x = x
            if current_y == 0:
                current_y = y
            if current_width < width:
                current_width = x + width
            if current_height < height:
                current_height = y + height

            self.set_groups_item_coordinates(
                item_id, current_x, current_y, current_width, current_height
            )

            # task_id -= 1

            # print(f"item_id {item_id}, task_id {task_id}, {task_text}")
            self.roadmap_dict["groups"]["group_items"][item_id]["tasks"][task_id] = {
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                "text": task_text,
            }
            # print(">>", self.roadmap_dict["groups"]["group_items"][item_id]["tasks"])

        def set_footer_coordinates(self, x, y, width, height):
            self.roadmap_dict["footer"] = {
                "x": x,
                "y": y,
                "width": width,
                "height": height,
            }
            self.roadmap_dict["recommended_height"] = y + height

        def get_recommended_height(self):
            return self.roadmap_dict.get("recommended_height", 0)

        def get_title_coordinates(self):
            return (
                self.roadmap_dict.get("title", "").get("x", 0),
                self.roadmap_dict.get("title", "").get("y", 0),
                self.roadmap_dict.get("title", "").get("width", 0),
                self.roadmap_dict.get("title", "").get("height", 0),
            )

        def get_timeline_coordinates(self):
            return (
                self.roadmap_dict.get("timeline", {}).get("x", 0),
                self.roadmap_dict.get("timeline", {}).get("y", 0),
                self.roadmap_dict.get("timeline", {}).get("width", 0),
                self.roadmap_dict.get("timeline", {}).get("height", 0),
            )

        def get_timeline_item_coordinates(self, item):
            return (
                self.roadmap_dict.get("timeline", {})
                .get("timeline_items", {})
                .get(item, {})
                .get("x", 0),
                self.roadmap_dict.get("timeline", {})
                .get("timeline_items", {})
                .get(item, {})
                .get("y", 0),
                self.roadmap_dict.get("timeline", {})
                .get("timeline_items", {})
                .get(item, {})
                .get("width", 0),
                self.roadmap_dict.get("timeline", {})
                .get("timeline_items", {})
                .get(item, {})
                .get("height", 0),
            )

        def get_timeline_item_text(self, item):
            return self.roadmap_dict.get("timeline", {}).get("timeline_items", {}).get(
                item, {}
            ).get("text", ""), self.roadmap_dict.get("timeline", {}).get(
                "timeline_items", {}
            ).get(
                item, {}
            ).get(
                "value", ""
            )

        def get_timeline_item_value(self, item):
            return (
                self.roadmap_dict.get("timeline", {})
                .get("timeline_items", {})
                .get(item, {})
                .get("value", "")
            )

        def get_groups_coordinates(self):
            return (
                self.roadmap_dict.get("groups", {}).get("x", 0),
                self.roadmap_dict.get("groups", {}).get("y", 0),
                self.roadmap_dict.get("groups", {}).get("width", 0),
                self.roadmap_dict.get("groups", {}).get("height", 0),
            )

        def get_groups_item_coordinates(self, item_id):
            x, y, width, height = 0, 0, 0, 0
            x = (
                self.roadmap_dict.get("groups", {})
                .get("group_items", {})
                .get(item_id, {})
                .get("x", 0)
            )
            y = (
                self.roadmap_dict.get("groups", {})
                .get("group_items", {})
                .get(item_id, {})
                .get("y", 0)
            )
            width = (
                self.roadmap_dict.get("groups", {})
                .get("group_items", {})
                .get(item_id, {})
                .get("width", 0)
            )
            height = (
                self.roadmap_dict.get("groups", {})
                .get("group_items", {})
                .get(item_id, {})
                .get("height", 0)
            )
            return (x, y, width, height)

        def get_groups_item_task_coordinates(self, item, task):
            return (
                self.roadmap_dict.get("groups", {})
                .get("group_items", {})
                .get(item, {})
                .get("tasks", {})
                .get(task, 0)
                .get("x", 0),
                self.roadmap_dict.get("groups", {})
                .get("group_items", {})
                .get(item, {})
                .get("tasks", {})
                .get(task, 0)
                .get("y", 0),
                self.roadmap_dict.get("groups", {})
                .get("group_items", {})
                .get(item, {})
                .get("tasks", {})
                .get(task, 0)
                .get("width", 0),
                self.roadmap_dict.get("groups", {})
                .get("group_items", {})
                .get(item, {})
                .get("tasks", {})
                .get(task, 0)
                .get("height", 0),
            )

        def get_footer_coordinates(self):
            return (
                self.roadmap_dict.get("footer", {}).get("x", 0),
                self.roadmap_dict.get("footer", {}).get("y", 0),
                self.roadmap_dict.get("footer", {}).get("width", 0),
                self.roadmap_dict.get("footer", {}).get("height", 0),
            )

    def __init__(self, width, height, output_file_name) -> None:
        self.__painter = Painter(width, height, output_file_name)
        self.__roadmap_dict = self.__RoadMapDict()
        self.__width = width
        self.__height = height
        self.__output_file_name = output_file_name

        # Initialise settings
        self.text_font = ""
        self.background_colour = ""
        self.title_text = ""
        self.title_font = ""
        self.title_font_size = 0
        self.title_colour = ""
        self.show_footer = True
        self.footer_text = ""
        self.footer_font = ""
        self.footer_font_size = 0
        self.footer_colour = ""
        self.timeline_mode = ""
        self.timeline_item = 0
        self.timeline_fill_colour = ""
        self.timeline_text_colour = ""
        self.group_text_colour = ""
        self.task_text_colour = ""
        self.__tasks = []
        self.__today = datetime.today()

    def __set_default_settings(self):
        """
        Set default settings
        """
        if self.text_font == "":
            self.text_font = "Arial"
        if self.background_colour == "":
            self.background_colour = "White"
        if self.title_text == "":
            self.title_text = "This is the default title"
        if self.title_font == "":
            self.text_font
        if self.title_font_size == 0:
            self.title_font_size = 18
        if self.title_colour == "":
            self.title_colour = self.__DEFAULT_TITLE_TEXT_COLOUR
        if self.footer_text == "":
            self.footer_text = f"Generated by Kaihanga Mahere v{self.VERSION}"
        if self.footer_font == "":
            self.footer_font = self.text_font
        if self.footer_font_size == 0:
            self.footer_font_size = 12
        if self.footer_colour == "":
            self.footer_colour = self.__DEFAULT_FOOTER_TEXT_COLOUR
        if self.timeline_mode == "":
            self.timeline_mode = self.MONTHLY
        if self.timeline_item == 0:
            self.timeline_item = 12
        if self.timeline_fill_colour == "":
            self.timeline_fill_colour = self.__DEFAULT_TIMELINE_FILL_COLOUR
        if self.timeline_text_colour == "":
            self.timeline_text_colour = self.__DEFAULT_TIMELINE_TEXT_COLOUR
        if self.group_text_colour == "":
            self.group_text_colour = self.__DEFAULT_GROUP_TEXT_COLOUR
        if self.task_text_colour == "":
            self.task_text_colour = self.__DEFAULT_TASK_TEXT_COLOUR

    def __generate_sample_data(self):
        if len(self.__tasks) == 0:
            task_data = [
                {
                    "group": "Stream 1",
                    "colour": "green",
                    "tasks": [
                        {
                            "task": "Feature 1",
                            "start": datetime(2022, 10, 24),
                            "end": datetime(2022, 11, 24),
                            "colour": "lightgreen",
                        },
                        {
                            "task": "Feature 2",
                            "start": datetime(2022, 12, 24),
                            "end": datetime(2023, 4, 24),
                            "colour": "lightgreen",
                        },
                    ],
                },
                {
                    "group": "Stream 2",
                    "colour": "blue",
                    "tasks": [
                        {
                            "task": "Feature 3",
                            "start": datetime(2022, 4, 24),
                            "end": datetime(2022, 12, 24),
                            "colour": "lightblue",
                        },
                        {
                            "task": "Feature 4",
                            "start": datetime(2023, 1, 24),
                            "end": datetime(2024, 12, 24),
                            "colour": "lightblue",
                        },
                    ],
                },
                {
                    "group": "Stream 3",
                    "colour": "grey",
                    "tasks": [
                        {
                            "task": "Feature 5",
                            "start": datetime(2022, 10, 24),
                            "end": datetime(2023, 3, 24),
                            "colour": "lightgrey",
                        },
                        {
                            "task": "Feature 6",
                            "start": datetime(2023, 4, 24),
                            "end": datetime(2023, 7, 24),
                            "colour": "lightgrey",
                        },
                        {
                            "task": "Feature 7",
                            "start": datetime(2023, 8, 24),
                            "end": datetime(2023, 8, 24),
                            "colour": "lightgrey",
                        },
                    ],
                },
            ]
        else:
            task_data = self.__tasks
        return task_data

    def __set_background(self):
        self.__painter.set_background_colour(self.background_colour)

    def __draw_title(self):
        self.__painter.set_font(
            self.title_font, self.title_font_size, self.title_colour
        )
        text_width, text_height = self.__painter.get_text_dimension(self.title_text)
        self.__painter.draw_text(
            (self.__width / 2) - text_width / 2, 30, self.title_text
        )
        self.__roadmap_dict.set_title_coordinates(
            (self.__width / 2) - text_width / 2,
            30,
            text_width,
            text_height,
            self.title_text,
        )

    def __draw_timeline(self, task_data):
        max_group_text_width = 0
        for x in task_data:
            group_text = x.get("group")
            self.__painter.set_font("Arial", 12, x.get("colour"))
            group_text_width, group_text_height = self.__painter.get_text_dimension(
                group_text
            )
            if group_text_width > max_group_text_width:
                max_group_text_width = group_text_width + 20

        # 40px is for right margin
        timeline_width = (
            self.__width
            - max_group_text_width
            - (self.__HSPACER * self.timeline_item)
            - 40
        )

        timeline_y_pos = 40
        timeline_height = 20

        timeline_item_width = timeline_width / self.timeline_item

        timeline_positions = []
        for x in range(self.timeline_item):
            timeline_x_pos = (
                (x * timeline_item_width)
                + max_group_text_width
                + (self.__HSPACER * x)
                + 30
            )

            # Draw timeline box
            self.__painter.set_colour(self.timeline_fill_colour)
            self.__painter.draw_box(
                timeline_x_pos, timeline_y_pos, timeline_item_width, timeline_height
            )
            self.__roadmap_dict.set_timeline_item_coordinates(
                x, timeline_x_pos, timeline_y_pos, timeline_item_width, timeline_height
            )

            # Draw timeline text
            timeline_text = ""
            if self.timeline_mode == self.WEEKLY:
                this_week = self.__today + relativedelta(weeks=+x)
                timeline_text = f"W{this_week.strftime('%W')} {this_week.year}"
                timeline_text_with_year = f"{this_week.year}{this_week.strftime('%W')}"

            if self.timeline_mode == self.MONTHLY:
                this_month = self.__today + relativedelta(months=+x)
                timeline_text = f"{this_month.strftime('%b')} {this_month.year}"
                timeline_text_with_year = (
                    f"{this_month.year}{this_month.strftime('%m')}"
                )

            if self.timeline_mode == self.QUARTERLY:
                this_month = self.__today + relativedelta(months=+(x * 3))
                this_quarter = (this_month.month - 1) // 3 + 1
                timeline_text = f"Q{this_quarter} {this_month.year}"
                timeline_text_with_year = f"{this_month.year}{this_quarter}"

            if self.timeline_mode == self.HALF_YEARLY:
                this_month = self.__today + relativedelta(months=+(x * 6))
                this_halfyear = (this_month.month - 1) // 6 + 1
                timeline_text = f"H{this_halfyear} {this_month.year}"
                timeline_text_with_year = f"{this_month.year}{this_halfyear}"

            if self.timeline_mode == self.YEARLY:
                this_month = self.__today + relativedelta(months=+(x * 12))
                timeline_text = f"{this_month.year}"
                timeline_text_with_year = f"{this_month.year}"

            # timeline_positions.append(
            #     [
            #         timeline_x_pos,
            #         timeline_y_pos,
            #         timeline_item_width,
            #         timeline_height,
            #         timeline_text,
            #         timeline_text_with_year,
            #     ]
            # )

            self.__painter.set_font(self.text_font, 12, self.timeline_text_colour)
            x_pos, y_pos = self.__painter.get_display_text_position(
                timeline_x_pos,
                timeline_y_pos,
                timeline_item_width,
                timeline_height,
                timeline_text,
                "centre",
            )
            self.__painter.draw_text(x_pos, y_pos, timeline_text)
            self.__roadmap_dict.set_timeline_item_text(x, timeline_text)
            self.__roadmap_dict.set_timeline_item_value(x, timeline_text_with_year)

        return max_group_text_width, timeline_positions

    def __draw_footer(self):
        if self.show_footer:
            self.__painter.set_font(
                self.footer_font, self.footer_font_size, self.footer_colour
            )
            footer_width, footer_height = self.__painter.get_text_dimension(
                self.footer_text
            )
            footer_y_pos = self.__roadmap_dict.get_recommended_height()
            self.__painter.draw_text(
                (self.__width / 2) - footer_width / 2,
                # self.__height - 10,
                footer_y_pos,
                self.footer_text,
            )
            self.__roadmap_dict.set_footer_coordinates(
                (self.__width / 2) - footer_width / 2,
                # self.__height - 10,
                footer_y_pos,
                footer_width,
                footer_height,
            )

    def __draw_group(self, x, y, max_width, group):
        group_text = group.get("group")
        last_y_pos = 0

        # Calc group height
        task_count = len(group.get("tasks"))
        group_total_height = (20 * task_count) + (2 * (task_count - 1))
        group_total_width = max_width + 20

        self.__painter.set_colour(group.get("colour"))
        self.__painter.draw_box(x, y, group_total_width, group_total_height)

        self.__painter.set_colour(self.group_text_colour)
        x_pos, y_pos = self.__painter.get_display_text_position(
            x, y, group_total_width, group_total_height, group_text, "left"
        )
        self.__painter.draw_text(x_pos, y_pos, group_text)
        return last_y_pos

    def __draw_groups(self, task_data, max_group_text_width, timeline_positions):
        group_y_start_pos = 70
        group_height = 0

        next_group_y_pos = 0
        group_x_pos = 10
        group_y_pos = 0
        i = 0
        for x in task_data:
            group_text = x.get("group")

            self.__painter.set_font(self.text_font, 12, self.timeline_text_colour)

            if next_group_y_pos == 0:
                group_y_pos = group_y_start_pos
            else:
                group_y_pos = next_group_y_pos + 25

            self.__draw_group(group_x_pos, group_y_pos, max_group_text_width, x)
            next_group_y_pos = group_y_pos

            ###(4) Set Task
            task_y_pos = group_y_pos
            next_group_y_pos = task_y_pos

            j = 0
            for task in x.get("tasks"):
                task_text = task.get("task")
                text_width, text_height = self.__painter.get_text_dimension(task_text)
                y_pos = task_y_pos + text_height * j + (self.__VSPACER * j)
                next_group_y_pos = y_pos
                text_height = 20

                # Draw task bar
                bar_start_x_pos = 0
                total_bar_width = 0
                row_match = 0
                for z in range(self.timeline_item):
                    if self.timeline_mode == self.WEEKLY:
                        (
                            task_start_period,
                            task_end_period,
                            this_period,
                        ) = self.__get_weekly_dates(timeline_positions, task, z)

                    if self.timeline_mode == self.MONTHLY:
                        (
                            task_start_period,
                            task_end_period,
                            this_period,
                        ) = self.__get_monthly_dates(task, z)

                    if self.timeline_mode == self.QUARTERLY:
                        (
                            task_start_period,
                            task_end_period,
                            this_period,
                        ) = self.__get_quarterly_dates(timeline_positions, task, z)

                    if self.timeline_mode == self.HALF_YEARLY:
                        (
                            task_start_period,
                            task_end_period,
                            this_period,
                        ) = self.__get_half_yearly_dates(timeline_positions, task, z)

                    if self.timeline_mode == self.YEARLY:
                        (
                            task_start_period,
                            task_end_period,
                            this_period,
                        ) = self.__get_yearly_dates(timeline_positions, task, z)

                    if (
                        task_start_period <= this_period
                        and task_end_period >= this_period
                    ):
                        (
                            task_box_x_pos,
                            task_box_y_pos,
                            task_box_width,
                            task_box_height,
                        ) = self.__roadmap_dict.get_timeline_item_position(z)
                        if bar_start_x_pos == 0:
                            bar_start_x_pos = task_box_x_pos

                        row_match += 1

                if row_match > 0:
                    task_box_y_pos = y_pos
                    task_box_height = text_height
                    total_bar_width = task_box_width * row_match + (
                        self.__HSPACER * row_match - 1
                    )

                    self.__painter.set_colour(task.get("colour"))
                    self.__painter.draw_box(
                        bar_start_x_pos,
                        task_box_y_pos,
                        total_bar_width,
                        task_box_height,
                    )

                    self.__roadmap_dict.set_groups_item_task_coordinates(
                        i,
                        j,
                        bar_start_x_pos,
                        task_box_y_pos,
                        total_bar_width,
                        task_box_height,
                        task_text,
                    )

                    self.__painter.set_font(self.text_font, 12, self.task_text_colour)
                    x_pos, y_pos = self.__painter.get_display_text_position(
                        bar_start_x_pos,
                        task_box_y_pos,
                        total_bar_width,
                        text_height,
                        task_text,
                        "centre",
                    )
                    self.__painter.draw_text(x_pos, y_pos, f"{task_text}")

                j += 1
            i += 1

    def __get_yearly_dates(self, timeline_positions, task, z):
        task_start_date = datetime(
            task.get("start").year,
            task.get("start").month,
            task.get("start").day,
        )
        task_end_date = datetime(
            task.get("end").year,
            task.get("end").month,
            task.get("end").day,
        )
        task_start_period = f"{task_start_date.year}"
        task_end_period = f"{task_end_date.year}"

        this_period = timeline_positions[z][5]
        return task_start_period, task_end_period, this_period

    def __get_half_yearly_dates(self, timeline_positions, task, z):
        task_start_date = datetime(
            task.get("start").year,
            task.get("start").month,
            task.get("start").day,
        )
        task_end_date = datetime(
            task.get("end").year,
            task.get("end").month,
            task.get("end").day,
        )
        task_start_period = f"{task_start_date.year}{task_start_date.month // 6 + 1}"
        task_end_period = f"{task_end_date.year}{task_end_date.month // 6 + 1}"

        # this_period = timeline_positions[z][5]
        this_period = self.__roadmap_dict.get_timeline_item_value(z)
        return task_start_period, task_end_period, this_period

    def __get_quarterly_dates(self, timeline_positions, task, z):
        task_start_date = datetime(
            task.get("start").year,
            task.get("start").month,
            task.get("start").day,
        )
        task_end_date = datetime(
            task.get("end").year,
            task.get("end").month,
            task.get("end").day,
        )
        task_start_period = f"{task_start_date.year}{task_start_date.month // 3 + 1}"
        task_end_period = f"{task_end_date.year}{task_end_date.month // 3 + 1}"

        # this_period = timeline_positions[z][5]
        this_period = self.__roadmap_dict.get_timeline_item_value(z)
        return task_start_period, task_end_period, this_period

    def __get_monthly_dates(self, task, z):
        task_start_period = datetime(task.get("start").year, task.get("start").month, 1)
        task_end_period = datetime(task.get("end").year, task.get("end").month, 1)

        this_month = (self.__today + relativedelta(months=+z)).month
        this_year = (self.__today + relativedelta(months=+z)).year
        this_period = datetime(this_year, this_month, 1)

        return task_start_period, task_end_period, this_period

    def __get_weekly_dates(self, timeline_positions, task, z):
        task_start_date = datetime(
            task.get("start").year,
            task.get("start").month,
            task.get("start").day,
        )
        task_end_date = datetime(
            task.get("end").year,
            task.get("end").month,
            task.get("end").day,
        )
        task_start_period = f"{task_start_date.year}{task_start_date.strftime('%W')}"
        task_end_period = f"{task_end_date.year}{task_end_date.strftime('%W')}"

        # this_period = timeline_positions[z][4]
        this_period = self.__roadmap_dict.get_timeline_item_value(z)

        return task_start_period, task_end_period, this_period

    def add_group(self, group_text, colour=None) -> str:
        tasks = []
        if colour is None:
            colour = self.__DEFAULT_GROUP_FILL_COLOUR
        group = {"group": group_text, "colour": colour, "tasks": tasks}
        self.__tasks.append(group)
        return group_text

    def add_task(
        self, group_text, task_text, start_date, end_date, colour=None
    ) -> None:
        # Expecting YYYY-MM-DD format. E.g 2022-08-29
        start_date_object = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_object = datetime.strptime(end_date, "%Y-%m-%d")

        if colour is None:
            colour = self.__DEFAULT_TASK_FILL_COLOUR
        task = {
            "task": task_text,
            "start": start_date_object,
            "end": end_date_object,
            "colour": colour,
        }
        for group in self.__tasks:
            if group.get("group") == group_text:
                group.get("tasks").append(task)

    def render(self) -> None:
        # Default settings
        self.__set_default_settings()

        # Create a sample data structure if none is provided
        task_data = self.__generate_sample_data()

        # Set backgroud
        self.__set_background()

        # Set Title
        self.__draw_title()

        # Draw Timeline
        max_group_text_width, timeline_positions = self.__draw_timeline(task_data)

        # Draw Group
        self.__draw_groups(task_data, max_group_text_width, timeline_positions)

        # Draw footer
        self.__draw_footer()
        pd(self.__roadmap_dict.roadmap_dict)

        # Save
        self.__painter.save_surface()

        return self.__roadmap_dict.get_recommended_height()
