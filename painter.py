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
import datetime
from webcolors import name_to_rgb
from dateutil.relativedelta import relativedelta
class Painter():    
    # initialise code
    def __init__(self, width, height):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.cr = cairo.Context(self.surface)
        self.Width = width
        self.Height = height

    def rgb_to_float(self, colour):
        # Convert RGBS to floats
        fRGBS = name_to_rgb(colour)
        return [x / 255 for x in fRGBS]
        
    def setColour(self, colour):
        self.cr.set_source_rgb(*self.rgb_to_float(colour))
        
    def setFont(self, font, fontSize, fontColour):
        self.cr.select_font_face(font)
        self.cr.set_font_size(fontSize)
        self.setColour(fontColour)
        
    def drawTitle(self, title, titleColour):
        textWidth, textHeight = self.getTextDimension(title)
        self.drawText((self.Width/2) - textWidth/2, 30, title)
        
    def drawFooter(self, footer, footerColour):
        footerWidth, footerHeight = self.getTextDimension(footer)
        self.drawText((self.Width/2) - footerWidth/2, self.Height - 10, footer)
        
    def drawBox(self, x, y, width, height):
        self.cr.rectangle(x, y, width, height)
        self.cr.fill()
        
    def drawText(self, x, y, text):
        self.cr.move_to(x, y)
        self.cr.show_text(text)
        
    def getTextDimension(self, text):
        textXbearing, textYbearing, textWidth, textHeight, dx, dy = self.cr.text_extents(text)
        return textWidth, textHeight
        
    def setBackgroundColour(self, colour):
        self.setColour(colour)
        self.cr.paint()
        
    def getDisplayTextPosision(self, x, y, width, height, text, alignment):
        textWidth, textHeight = self.getTextDimension(text)
        if alignment == "centre":
            textPosX = (width / 2) - (textWidth / 2)
        elif alignment == "right":
            textPosX = width - textWidth
        
        textPosY = (height / 2) + (textHeight / 2)
            
        return x+textPosX, y+textPosY
    
    def saveSurfaceToPNG(self, fileName):
        if (len(fileName) == 0):
            fileName = "roadmap.png"
        self.surface.write_to_png(fileName)  # Output to PNG

