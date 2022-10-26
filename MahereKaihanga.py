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

import datetime
from dateutil.relativedelta import relativedelta
from painter import Painter


class MahereKaihanga():
    # Private variables
    __VSPACER, __HSPACER = 12, 2
    __TODAY = datetime.datetime.today()
    
    # Constant variables
    
    # Default settings
    text_font = "Arial"
    background_colour = "White"
    title = "This is a sample title"    
    title_colour = "Black"
    footer_colour = title_colour
    timeline_mode = "Month"
    timeline_item = 12
    timeline_fill_colour = "Salmon"
    timeline_text_colour = "Black"
    task_text_colour = "Black"

    tasks = []
    
    def __init__(self, width, height) -> None:
        self.painter = Painter(width, height)
        self.width = width
        self.height = height

    def render(self, file_name):
        # create a sample data structure if none is provided
        if (len(self.tasks) == 0):
            task_data = [
                {"group": "Sprint 1", "colour": "green", "tasks": [
                    {"task": "Feature 1", "start": datetime.datetime(2022, 10, 24), "end": datetime.datetime(2022, 11, 24), "colour": "lightgreen"},
                    {"task": "Feature 2", "start": datetime.datetime(2022, 12, 24), "end": datetime.datetime(2023, 4, 24), "colour": "lightgreen"}
                    ]},
                {"group": "Sprint 2", "colour": "blue", "tasks": [
                    {"task": "Feature 3", "start": datetime.datetime(2022, 4, 24), "end": datetime.datetime(2022, 12, 24), "colour": "lightblue"},
                    {"task": "Feature 4", "start": datetime.datetime(2023, 1, 24), "end": datetime.datetime(2024, 12, 24), "colour": "lightblue"}
                    ]},
                {"group": "Sprint 3", "colour": "grey", "tasks": [
                    {"task": "Feature 5", "start": datetime.datetime(2022, 10, 24), "end": datetime.datetime(2023, 3, 24), "colour": "lightgrey"},
                    {"task": "Feature 6", "start": datetime.datetime(2023, 4, 24), "end": datetime.datetime(2023, 7, 24), "colour": "lightgrey"},
                    {"task": "Feature 7", "start": datetime.datetime(2023, 8, 24), "end": datetime.datetime(2023, 8, 24), "colour": "lightgrey"}
                ]}              
            ]
        else:
            task_data = self.tasks


        ###(0) Set backgroud
        self.painter.set_background_colour(self.background_colour)

        ###(1) Set Title      
        self.painter.set_font("Arial", 18, self.title_colour)
        self.painter.draw_title(self.title, self.title_colour)
        
        ###(2) Set Timeline
        # Determine max group text width
        max_group_text_width = 0
        for x in task_data:
            group_text = x.get("group")
            self.painter.set_font("Arial", 12, x.get("colour"))
            group_text_width, group_text_height = self.painter.get_text_dimension(group_text)
            if group_text_width > max_group_text_width:
                max_group_text_width = group_text_width + 20

        # 20px is for right margin
        timeline_width = self.width - max_group_text_width - (self.__HSPACER * self.timeline_item) - 20 - 20
      
        timeline_y_pos = 40
        timeline_height = 20
        
        timeline_item_width = timeline_width / self.timeline_item

        timeline_positions = []
        for x in range(self.timeline_item):
            timeline_x_pos = (x * timeline_item_width) + max_group_text_width + (self.__HSPACER * x) + 30

            # Draw timeline item
            self.painter.set_colour(self.timeline_fill_colour)
            self.painter.draw_box(timeline_x_pos, timeline_y_pos, timeline_item_width, timeline_height)
            timeline_positions.append([timeline_x_pos, timeline_y_pos, timeline_item_width, timeline_height])

            # Draw timeline text
            this_month = self.__TODAY + relativedelta(months=+x)
            timeline_text = f"{this_month.strftime('%b')} {this_month.year}"
            self.painter.set_font(self.text_font, 12, self.timeline_text_colour)
            x_pos, y_pos = self.painter.get_display_text_position(timeline_x_pos, timeline_y_pos, timeline_item_width, timeline_height, timeline_text, "centre")
            self.painter.draw_text(x_pos, y_pos, timeline_text)
        
        ###(3) Set Group
        group_y_start_pos = 70
        group_height = 0

        next_group_y_pos = 0
        group_x_pos = 10
        group_y_pos = 0
        for x in task_data:
            group_text = x.get("group")
                
            self.painter.set_font("Arial", 12, self.timeline_text_colour)
            group_task_width, group_text_height = self.painter.get_text_dimension(group_text)
            if (next_group_y_pos == 0):
                group_y_pos = group_y_start_pos 
            else:
                group_y_pos = next_group_y_pos + 25
            
            self.painter.draw_group(group_x_pos, group_y_pos, max_group_text_width, x)
            next_group_y_pos = group_y_pos
            
            ###(4) Set Task
            task_y_pos = group_y_pos 
            next_group_y_pos = task_y_pos 

            j = 0
            task_x_pos = group_text_width 
            for task in x.get("tasks"):
                task_text = task.get("task")
                text_width, text_height = self.painter.get_text_dimension(task_text)
                y_pos = task_y_pos + text_height * j + (self.__VSPACER * j)
                next_group_y_pos = y_pos
                text_height = 20

                # Draw task bar
                task_start_date = datetime.datetime(task.get("start").year, task.get("start").month, 1)
                task_end_date = datetime.datetime(task.get("end").year, task.get("end").month, 1)
                
                bar_start_x_pos = 0
                total_bar_width = 0
                row_match = 0
                for z in range(self.timeline_item):
                    this_month = (self.__TODAY + relativedelta(months=+z)).month
                    this_year = (self.__TODAY + relativedelta(months=+z)).year
                    this_date = datetime.datetime(this_year, this_month, 1)

                    if (task_start_date <= this_date and task_end_date >= this_date):
                        task_box_x_pos = timeline_positions[z][0]
                        task_box_width = timeline_positions[z][2]
                        if (bar_start_x_pos == 0):
                            bar_start_x_pos = task_box_x_pos
                        
                        row_match += 1

                task_box_y_pos = y_pos
                task_box_height = text_height
                total_bar_width = task_box_width * row_match + (self.__HSPACER * row_match - 1)
                
                self.painter.set_colour(task.get("colour"))
                self.painter.draw_box(bar_start_x_pos,task_box_y_pos, total_bar_width, task_box_height)
                
                self.painter.set_font(self.text_font, 12, self.timeline_text_colour)
                x_pos, y_pos = self.painter.get_display_text_position(bar_start_x_pos, task_box_y_pos, total_bar_width, text_height, task_text, "centre")
                self.painter.draw_text(x_pos, y_pos, task_text)

                j += 1
                    

        """ To do
        Done (1) Display task text on top of bar
        Done (2) Display group text as a block
        (3) Show milestones
        (4) Proporsion task bar according to the start and end date
        """
        footer_text = "Generated by Mahere Kaihanga v0.1"
        self.painter.draw_footer(footer_text, self.footer_colour)

        self.painter.save_surface_to_png(file_name)
        


if __name__ == "__main__":
    x = MahereKaihanga(1024, 512)
    x.title = "This is my roadmap!!!"

    x.tasks = [
                {"group": "Stream 1: Develop base", "colour": "green", "tasks": [
                    {"task": "Feature 1", "start": datetime.datetime(2022, 10, 24), "end": datetime.datetime(2022, 11, 24), "colour": "lightgreen"},
                    {"task": "Feature 2", "start": datetime.datetime(2022, 12, 24), "end": datetime.datetime(2023, 4, 24), "colour": "lightgreen"}
                    ]},
                {"group": "Stream 2: Enable monitoring", "colour": "blue", "tasks": [
                    {"task": "Feature 3", "start": datetime.datetime(2022, 4, 24), "end": datetime.datetime(2022, 12, 24), "colour": "lightblue"},
                    {"task": "Feature 4", "start": datetime.datetime(2023, 1, 24), "end": datetime.datetime(2024, 12, 24), "colour": "lightblue"}
                    ]},
                {"group": "Stream 3: Support reporting", "colour": "grey", "tasks": [
                    {"task": "Feature 5", "start": datetime.datetime(2022, 10, 24), "end": datetime.datetime(2023, 3, 24), "colour": "lightgrey"},
                    {"task": "Feature 6", "start": datetime.datetime(2023, 4, 24), "end": datetime.datetime(2023, 7, 24), "colour": "lightgrey"},
                    {"task": "Feature 7", "start": datetime.datetime(2023, 8, 24), "end": datetime.datetime(2023, 8, 24), "colour": "lightgrey"}
                ]},
                {"group": "Stream 4: Implement ML analytics", "colour": "Purple", "tasks": [
                    {"task": "Feature 8", "start": datetime.datetime(2023, 5, 24), "end": datetime.datetime(2023, 11, 24), "colour": "Orchid"},
                    {"task": "Feature 9", "start": datetime.datetime(2023, 6, 24), "end": datetime.datetime(2023, 7, 24), "colour": "Orchid"},
                    {"task": "Feature 10", "start": datetime.datetime(2023, 8, 24), "end": datetime.datetime(2023, 8, 24), "colour": "Orchid"}
                ]},
                {"group": "Stream 5: Build Mobile App", "colour": "OrangeRed", "tasks": [
                    {"task": "Feature 11", "start": datetime.datetime(2022, 12, 24), "end": datetime.datetime(2023, 3, 24), "colour": "Coral"},
                    {"task": "Feature 12", "start": datetime.datetime(2023, 4, 24), "end": datetime.datetime(2023, 6, 24), "colour": "Coral"},
                    {"task": "Feature 13", "start": datetime.datetime(2023, 7, 24), "end": datetime.datetime(2023, 8, 24), "colour": "Coral"}
                ]}              
            ]
    x.render("my_roadmap.png")




