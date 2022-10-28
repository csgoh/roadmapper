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
        * Make 'colour' element optional
        * Implement logging
        * Implement class methods to allow user to add task, group, milestone, etc
        * Custom timeline start date
        * Option to turn off footer
        
        Done * Modularise method lines
        Done * Display task text on top of bar
        Done * Display group text as a block
        Done * Week, Quarter, Half Year, Year timeline mode support
        Done * Save as PDF
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
from painter import Painter

class Mahere():
    # Private variables
    __VSPACER = 12
    __HSPACER = 2
    
    # Constant variables
    VERSION = "0.1"
    WEEKLY = "W"
    MONTHLY = "M"
    QUARTERLY = "Q"
    HALF_YEARLY = "H"
    YEARLY = "Y"
    
    def __init__(self, width, height, output_file_name) -> None:
        self.__painter = Painter(width, height, output_file_name)
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
        self.footer_text = ""    
        self.footer_font = ""
        self.footer_font_size = 0
        self.footer_colour = ""
        self.timeline_mode = ""
        self.timeline_item = 0
        self.timeline_fill_colour = ""
        self.timeline_text_colour = ""
        self.task_text_colour = ""
        self.__tasks = []
        self.__today = datetime.today()
        
    def __set_default_settings(self):
        """
        Set default settings
        """
        if self.text_font == "":            self.text_font = "Arial" 
        if self.background_colour == "":    self.background_colour = "White"
        if self.title_text == "":           self.title_text = "This is the default title"    
        if self.title_font == "":           self.text_font
        if self.title_font_size == 0:       self.title_font_size = 18
        if self.title_colour == "":         self.title_colour = "Black"
        if self.footer_text == "":          self.footer_text = f"Generated by Kaihanga Mahere v{self.VERSION}"
        if self.footer_font == "":          self.footer_font = self.text_font
        if self.footer_font_size == 0:      self.footer_font_size = 12
        if self.footer_colour == "":        self.footer_colour = self.title_colour
        if self.timeline_mode == "":        self.timeline_mode = self.MONTHLY
        if self.timeline_item == 0:         self.timeline_item = 12
        if self.timeline_fill_colour == "": self.timeline_fill_colour = "Salmon"
        if self.timeline_text_colour == "": self.timeline_text_colour = "Black"
        if self.task_text_colour == "":     self.task_text_colour = "Black"
        
    def __generate_sample_data(self):
        if (len(self.__tasks) == 0):
            task_data = [
                {"group": "Stream 1", "colour": "green", "tasks": [
                    {"task": "Feature 1", "start": datetime(2022, 10, 24), "end": datetime(2022, 11, 24), "colour": "lightgreen"},
                    {"task": "Feature 2", "start": datetime(2022, 12, 24), "end": datetime(2023, 4, 24), "colour": "lightgreen"}
                    ]},
                {"group": "Stream 2", "colour": "blue", "tasks": [
                    {"task": "Feature 3", "start": datetime(2022, 4, 24), "end": datetime(2022, 12, 24), "colour": "lightblue"},
                    {"task": "Feature 4", "start": datetime(2023, 1, 24), "end": datetime(2024, 12, 24), "colour": "lightblue"}
                    ]},
                {"group": "Stream 3", "colour": "grey", "tasks": [
                    {"task": "Feature 5", "start": datetime(2022, 10, 24), "end": datetime(2023, 3, 24), "colour": "lightgrey"},
                    {"task": "Feature 6", "start": datetime(2023, 4, 24), "end": datetime(2023, 7, 24), "colour": "lightgrey"},
                    {"task": "Feature 7", "start": datetime(2023, 8, 24), "end": datetime(2023, 8, 24), "colour": "lightgrey"}
                ]}              
            ]
        else:
            task_data = self.__tasks
        return task_data
        
    def __set_background(self):
        self.__painter.set_background_colour(self.background_colour)
        
    def __draw_title(self):
        self.__painter.set_font(self.title_font, self.title_font_size, self.title_colour)
        text_width, text_height = self.__painter.get_text_dimension(self.title_text)
        self.__painter.draw_text((self.__width/2) - text_width/2, 30, self.title_text)
        
    def __draw_timeline(self, task_data):
        max_group_text_width = 0
        for x in task_data:
            group_text = x.get("group")
            self.__painter.set_font("Arial", 12, x.get("colour"))
            group_text_width, group_text_height = self.__painter.get_text_dimension(group_text)
            if group_text_width > max_group_text_width:
                max_group_text_width = group_text_width + 20

        # 40px is for right margin
        timeline_width = self.__width - max_group_text_width - (self.__HSPACER * self.timeline_item) - 40
      
        timeline_y_pos = 40
        timeline_height = 20
        
        timeline_item_width = timeline_width / self.timeline_item

        timeline_positions = []
        for x in range(self.timeline_item):
            timeline_x_pos = (x * timeline_item_width) + max_group_text_width + (self.__HSPACER * x) + 30

            # Draw timeline box
            self.__painter.set_colour(self.timeline_fill_colour)
            self.__painter.draw_box(timeline_x_pos, timeline_y_pos, timeline_item_width, timeline_height)
            

            # Draw timeline text
            timeline_text = ""
            if self.timeline_mode == self.WEEKLY:
                this_week = self.__today + relativedelta(weeks=+x)
                timeline_text = f"W{this_week.strftime('%W')} {this_week.year}"
                timeline_text_with_year = f"{this_week.year}{this_week.strftime('%W')}"
                
            if self.timeline_mode == self.MONTHLY:
                this_month = self.__today + relativedelta(months=+x)
                timeline_text = f"{this_month.strftime('%b')} {this_month.year}"
                timeline_text_with_year = f"{this_month.year}{this_month.strftime('%m')}"
                
            if self.timeline_mode == self.QUARTERLY:
                this_month = self.__today + relativedelta(months=+(x*3))
                this_quarter = (this_month.month-1)//3 + 1
                timeline_text = f"Q{this_quarter} {this_month.year}"
                timeline_text_with_year = f"{this_month.year}{this_quarter}"
                
            if self.timeline_mode == self.HALF_YEARLY:
                this_month = self.__today + relativedelta(months=+(x*6))
                this_halfyear = (this_month.month-1)//6 + 1
                timeline_text = f"H{this_halfyear} {this_month.year}"
                timeline_text_with_year = f"{this_month.year}{this_halfyear}"
                print (f"{this_month.year}{this_halfyear}")
                
            if self.timeline_mode == self.YEARLY:
                this_month = self.__today + relativedelta(months=+(x*12))
                timeline_text = f"{this_month.year}"
                timeline_text_with_year = f"{this_month.year}"
                
            timeline_positions.append([timeline_x_pos, timeline_y_pos, timeline_item_width, timeline_height, timeline_text_with_year,timeline_text_with_year])
            
            self.__painter.set_font(self.text_font, 12, self.timeline_text_colour)
            x_pos, y_pos = self.__painter.get_display_text_position(timeline_x_pos, timeline_y_pos, timeline_item_width, timeline_height, timeline_text, "centre")
            self.__painter.draw_text(x_pos, y_pos, timeline_text)
        return max_group_text_width,timeline_positions
        
    def __draw_footer(self):
        self.__painter.set_font(self.footer_font, self.footer_font_size, self.footer_colour)
        footer_width, footer_height = self.__painter.get_text_dimension(self.footer_text)
        self.__painter.draw_text((self.__width/2) - footer_width/2, self.__height - 10, self.footer_text)
        
    def __draw_group(self, x, y, max_width, group):
        group_text = group.get("group")
        last_y_pos = 0        
        
        # Calc group height
        task_count = len(group.get("tasks"))
        group_total_height = (20 * task_count) + (2 * (task_count-1))
        group_total_width = max_width + 20
            
        self.__painter.set_colour(group.get("colour"))
        self.__painter.draw_box(x, y, group_total_width, group_total_height)
        
        self.__painter.set_colour("White")
        x_pos, y_pos = self.__painter.get_display_text_position(x, y, group_total_width, group_total_height, group_text, "left")
        self.__painter.draw_text(x_pos, y_pos, group_text)
        return last_y_pos
    
    def __draw_groups(self, task_data, max_group_text_width, timeline_positions):
        group_y_start_pos = 70
        group_height = 0

        next_group_y_pos = 0
        group_x_pos = 10
        group_y_pos = 0
        for x in task_data:
            group_text = x.get("group")
                
            self.__painter.set_font("Arial", 12, self.timeline_text_colour)
            group_task_width, group_text_height = self.__painter.get_text_dimension(group_text)
            if (next_group_y_pos == 0):
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
                        task_start_date = datetime(task.get("start").year, task.get("start").month, task.get("start").day)
                        task_end_date = datetime(task.get("end").year, task.get("end").month, task.get("end").day)
                        task_start_period = f"{task_start_date.year}{task_start_date.strftime('%W')}"
                        task_end_period = f"{task_end_date.year}{task_end_date.strftime('%W')}"
                    
                        this_period = timeline_positions[z][4]
                                              
                    if self.timeline_mode == self.MONTHLY:
                        task_start_period = datetime(task.get("start").year, task.get("start").month, 1)
                        task_end_period = datetime(task.get("end").year, task.get("end").month, 1)
                        
                        this_month = (self.__today + relativedelta(months=+z)).month
                        this_year = (self.__today + relativedelta(months=+z)).year
                        this_period = datetime(this_year, this_month, 1)
                            
                    if self.timeline_mode == self.QUARTERLY:
                        task_start_date = datetime(task.get("start").year, task.get("start").month, task.get("start").day)
                        task_end_date = datetime(task.get("end").year, task.get("end").month, task.get("end").day)
                        task_start_period = f"{task_start_date.year}{task_start_date.month//3 + 1}"
                        task_end_period = f"{task_end_date.year}{task_end_date.month//3 + 1}"
                        
                        this_period = timeline_positions[z][4]
                    
                    if self.timeline_mode == self.HALF_YEARLY:
                        task_start_date = datetime(task.get("start").year, task.get("start").month, task.get("start").day)
                        task_end_date = datetime(task.get("end").year, task.get("end").month, task.get("end").day)
                        task_start_period = f"{task_start_date.year}{task_start_date.month//6 + 1}"
                        task_end_period = f"{task_end_date.year}{task_end_date.month//6 + 1}"
                        
                        this_period = timeline_positions[z][4]
                        
                    if self.timeline_mode == self.YEARLY:
                        task_start_date = datetime(task.get("start").year, task.get("start").month, task.get("start").day)
                        task_end_date = datetime(task.get("end").year, task.get("end").month, task.get("end").day)
                        task_start_period = f"{task_start_date.year}"
                        task_end_period = f"{task_end_date.year}"
                        
                        this_period = timeline_positions[z][4]

                    print (f"{task_text},{task_start_date}-{task_end_date} = this_period: {this_period}, task_start_period: {task_start_period}, task_end_period: {task_end_period}")
                    if (task_start_period <= this_period and task_end_period >= this_period):
                        task_box_x_pos = timeline_positions[z][0]
                        task_box_width = timeline_positions[z][2]
                        print ("Match")
                        if (bar_start_x_pos == 0):
                            bar_start_x_pos = task_box_x_pos
                        
                        row_match += 1

                if (row_match > 0):
                    task_box_y_pos = y_pos
                    task_box_height = text_height
                    total_bar_width = task_box_width * row_match + (self.__HSPACER * row_match - 1)
                    
                    self.__painter.set_colour(task.get("colour"))
                    self.__painter.draw_box(bar_start_x_pos,task_box_y_pos, total_bar_width, task_box_height)
                    
                    self.__painter.set_font(self.text_font, 12, self.timeline_text_colour)
                    x_pos, y_pos = self.__painter.get_display_text_position(bar_start_x_pos, task_box_y_pos, total_bar_width, text_height, task_text, "centre")
                    self.__painter.draw_text(x_pos, y_pos, f"{task_text}")
                
                j += 1
    
    def add_group(self, group_text, colour) -> str:
        tasks = []
        group = {"group": group_text, "colour": colour, "tasks": tasks}
        self.__tasks.append(group)
        return group_text
        
    def add_task(self, group_text, task_text, start_date, end_date, colour):
        # Expecting YYYY-MM-DD format. E.g 2022-08-29
        start_date_object = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_object = datetime.strptime(end_date, "%Y-%m-%d")

        task = {"task": task_text, "start": start_date_object, "end": end_date_object, "colour": colour}
        for group in self.__tasks:
            if group.get("group") == group_text:
                group.get("tasks").append(task)
    
    def render(self):
        # Default settings
        self.__set_default_settings()
        
        # Create a sample data structure if none is provided
        task_data = self.__generate_sample_data()

        # Set backgroud
        self.__set_background()

        # Set Title      
        self.__draw_title()
        
        # Draw Timeline
        # Determine max group text width
        max_group_text_width, timeline_positions = self.__draw_timeline(task_data)
        
        # Draw Group
        self.__draw_groups(task_data, max_group_text_width, timeline_positions)
        
        # Draw footer
        self.__draw_footer()
        
        # Save
        self.__painter.save_surface()
