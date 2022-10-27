# Painter class - Wrapper for PyCairo library
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
import cairo
from webcolors import name_to_rgb

class Painter():    
    __VSPACER, __HSPACER = 12, 2
    
    # initialise code
    def __init__(self, width, height):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.cr = cairo.Context(self.surface)
        self.Width = width
        self.Height = height

    def rgb_to_float(self, colour):
        # Convert RGBS to floats
        f_rgbs = name_to_rgb(colour)
        return [x / 255 for x in f_rgbs]
        
    def set_colour(self, colour):
        self.cr.set_source_rgb(*self.rgb_to_float(colour))
        
    def set_font(self, font, font_size, font_colour):
        self.cr.select_font_face(font)
        self.cr.set_font_size(font_size)
        self.set_colour(font_colour)
        
    def draw_title(self, title):
        text_width, text_height = self.get_text_dimension(title)
        self.draw_text((self.Width/2) - text_width/2, 30, title)
        
    def draw_footer(self, footer):
        footer_width, footer_height = self.get_text_dimension(footer)
        self.draw_text((self.Width/2) - footer_width/2, self.Height - 10, footer)
        
    def draw_box(self, x, y, width, height):
        self.cr.rectangle(x, y, width, height)
        self.cr.fill()
        
    def draw_text(self, x, y, text):
        self.cr.move_to(x, y)
        self.cr.show_text(text)
        
        
    def draw_group(self, x, y, max_width, group):
        group_text = group.get("group")
        last_y_pos = 0        
        group_task_width, group_text_height = self.get_text_dimension(group_text)
        
        # Calc group height
        task_count = len(group.get("tasks"))
        group_total_height = (20 * task_count) + (2 * (task_count-1))
        group_total_width = max_width + 20
            
        self.set_colour(group.get("colour"))
        self.draw_box(x, y, group_total_width, group_total_height)
        print (f"Drawing group {group_text} y:{y}, h:{group_total_height}, total={y+group_total_height}")
        self.set_colour("White")
        x_pos, y_pos = self.get_display_text_position(x, y, group_total_width, group_total_height, group_text, "left")
        self.draw_text(x_pos, y_pos, group_text)
        return last_y_pos
        
    def get_text_dimension(self, text):
        text_x_bearing, text_y_bearing, text_width, text_height, dx, dy = self.cr.text_extents(text)
        return text_width, text_height
        
    def set_background_colour(self, colour):
        self.set_colour(colour)
        self.cr.paint()
        
    def get_display_text_position(self, x, y, width, height, text, alignment):
        text_width, text_height = self.get_text_dimension(text)
        if alignment == "centre":
            text_x_pos = (width / 2) - (text_width / 2)
        elif alignment == "right":
            text_x_pos = width - text_width
        elif alignment == "left":
            text_x_pos = x + 10
        
        text_y_pos = (height / 2) + (text_height / 2)
            
        return x+text_x_pos, y+text_y_pos
    
    def save_surface_to_png(self, file_name):
        if (len(file_name) == 0):
            file_name = "roadmap.png"
        self.surface.write_to_png(file_name)  # Output to PNG


