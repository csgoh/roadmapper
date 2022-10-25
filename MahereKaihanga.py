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

import cairo
import datetime
from webcolors import name_to_rgb
from dateutil.relativedelta import relativedelta


class MahereKaihanga():
    # Default settings
    Width, Height = 1024, 512 
    VSPACER, HSPACER = 12, 2
    BackgroundColour = "White"
    Title = "This is a sample title"
    
    TitleColour = "Black"
    FooterColour = TitleColour
    TimelineMode = "Month"
    TimelineItem = 12
    TimelineFillColour = "Salmon"
    TimelineTextColour = "Black"

    Today = datetime.datetime.today()

    Tasks = []

    def __init__(self) -> None:
        pass

    def rgb_to_float(self, colour):
        # Convert RGBS to floats
        fRGBS = name_to_rgb(colour)
        return [x / 255 for x in fRGBS]
        #return fRGBS[0] / 255, fRGBS[1] / 255, fRGBS[2] / 255

    def render(self, fileName):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.Width, self.Height)
        cr = cairo.Context(surface)
        
        ### Setup
        titleR, titleG, titleB = self.rgb_to_float(self.TitleColour)
        tlfcR, tlfcG, tlfcB = self.rgb_to_float(self.TimelineFillColour)
        tltcR, tltcG, tltcB = self.rgb_to_float(self.TimelineTextColour)
        footerR, footerG, footerB = self.rgb_to_float(self.FooterColour)

        # create a default data structure contains task name, start date, end date, and color
        if (len(self.Tasks) == 0):
            taskData = [
                {"group": "Sample Group 1", "task": "Feature 1", "start": datetime.datetime(2022, 10, 24), "end": datetime.datetime(2022, 11, 24), "colour": "lightgreen"},
                {"group": "Sample Group 1", "task": "Feature 2", "start": datetime.datetime(2023, 3, 24), "end": datetime.datetime(2023, 12, 24), "colour": "lightgreen"},
                {"group": "Sample Group 1", "task": "Feature 3", "start": datetime.datetime(2022, 12, 24), "end": datetime.datetime(2023, 6, 24), "colour": "lightgreen"},
                {"group": "Sample Group 1", "task": "Feature 4", "start": datetime.datetime(2023, 1, 24), "end": datetime.datetime(2023, 2, 24), "colour": "lightgreen"},
                {"group": "Sample Group 2", "task": "Feature 5", "start": datetime.datetime(2022, 4, 24), "end": datetime.datetime(2022, 12, 24), "colour": "lightblue"},
                {"group": "Sample Group 2", "task": "Feature 6", "start": datetime.datetime(2023, 10, 24), "end": datetime.datetime(2024, 12, 24), "colour": "lightblue"},
                {"group": "Sample Group 2", "task": "Feature 7", "start": datetime.datetime(2023, 1, 24), "end": datetime.datetime(2023, 6, 24), "colour": "lightblue"},
                {"group": "Sample Group 2", "task": "Feature 8", "start": datetime.datetime(2022, 1, 24), "end": datetime.datetime(2022, 10, 24), "colour": "lightblue"},
                {"group": "Sample Group 3", "task": "Feature 9", "start": datetime.datetime(2022, 10, 24), "end": datetime.datetime(2022, 11, 24), "colour": "yellow"},
                {"group": "Sample Group 3", "task": "Feature 10", "start": datetime.datetime(2023, 8, 24), "end": datetime.datetime(2023, 12, 24), "colour": "yellow"},
                {"group": "Sample Group 3", "task": "Feature 11", "start": datetime.datetime(2022, 12, 24), "end": datetime.datetime(2023, 6, 24), "colour": "yellow"},
                {"group": "Sample Group 3", "task": "Feature 12", "start": datetime.datetime(2023, 1, 24), "end": datetime.datetime(2023, 2, 24), "colour": "yellow"},
            ]
        else:
            taskData = self.Tasks


        ###(0) Set backgroud
        cr.set_source_rgb(*self.rgb_to_float("White"))
        cr.paint()

        ###(1) Set Title
        cr.set_source_rgb(titleR, titleG, titleB)
        cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(18)
        textXbearing, textYbearing, textWidth, textHeight, dx, dy = cr.text_extents(self.Title)
        cr.move_to((self.Width/2) - textWidth/2, 30)
        cr.show_text(self.Title)
        
        ###(2) Set Timeline
        # Determine max task text width
        taskWidth = 0
        for x in taskData:
            groupText = x.get("group")
            groupTextXbearing, groupTextYbearing, groupTextWidth, groupTextHeight, dx, dy = cr.text_extents(groupText)
            if groupTextWidth > taskWidth:
                taskWidth = groupTextWidth 

        #print (taskWidth)
        timelineWidth = self.Width - taskWidth - (self.HSPACER * self.TimelineItem) - 10
        
        timelineYPos = 40
        timelineHeight = 20
        
        timelineItemWidth = timelineWidth / self.TimelineItem

        timelinePositions = []
        for x in range(self.TimelineItem):
            timelineX = (x * timelineItemWidth) + taskWidth + (self.HSPACER * x)

            # Draw timeline item
            cr.set_source_rgb(tlfcR, tlfcG, tlfcB)
            cr.rectangle(timelineX,timelineYPos, timelineItemWidth, timelineHeight)
            timelinePositions.append([timelineX, timelineYPos, timelineItemWidth, timelineHeight])
            cr.fill()

            # Draw timeline text
            cr.set_source_rgb(tltcR, tltcG, tltcB)
            cr.set_font_size(12)

            thisMonth = self.Today + relativedelta(months=+x)
            timelineText = str(thisMonth.strftime("%b")) + " " + str(thisMonth.year)
            textXbearing, textYbearing, textWidth, textHeight, dx, dy = cr.text_extents(timelineText)
            cr.move_to(timelineX + timelineItemWidth/2 - (textWidth / 2), timelineYPos + 10 + (textHeight / 2))
            cr.show_text(timelineText)
                      
        ###(3) Set Group

        groupYPos = 80
        groupHeight = 20

        i = 0
        lastGroupText = ""
        nextGroupY = 0
        groupX = 10
        groupY = 0
        for x in taskData:
            groupText = x.get("group")

            if (lastGroupText != groupText):
                lastGroupText = groupText
                
                cr.set_source_rgb(tltcR, tltcG, tltcB)
                groupTextXbearing, groupTextYbearing, groupTextWidth, groupTextHeight, dx, dy = cr.text_extents(groupText)
                if (nextGroupY == 0):
                    groupY = groupYPos + (groupTextHeight * i) + (self.VSPACER * i) 
                else:
                    groupY = nextGroupY + 30

                cr.move_to(groupX, groupY)
                #print("Group: ", groupText, str(groupX), str(groupY), str(groupWidth))
                cr.show_text(groupText)
                
                ###(4) Set Task
                taskYPos = groupY + groupHeight + 10

                nextGroupY = taskYPos 

                j = 0
                taskX = groupTextWidth 
                for y in taskData:
                    # Draw task item
                    if (groupText == y.get("group")):
                        
                        tasks = y.get("tasks")
                        for task in tasks:
                            taskText = task.get("task")
                            #print (">>>>", taskText)
                            
                            cr.set_source_rgb(tltcR, tltcG, tltcB)
                            textXbearing, textYbearing, textWidth, textHeight, dx, dy = cr.text_extents(taskText)
                            yPos = taskYPos + textHeight * j + (self.VSPACER * j)
                            nextGroupY = yPos

                            # Draw task bar
                            taskR, taskG, taskB = self.rgb_to_float(task.get("colour"))
                            row = 0
                            
                            taskStartMonth = task.get("start").month
                            taskEndMonth = task.get("end").month
                            taskStartDate = datetime.datetime(task.get("start").year, taskStartMonth, 1)
                            taskEndDate = datetime.datetime(task.get("end").year, taskEndMonth, 1)
                            
                            totalBarWidth = 0
                            startPos = 0
                            rowMatch = 0
                            for z in range(self.TimelineItem):
                                thisMonth = (self.Today + relativedelta(months=+z)).month
                                thisYear = (self.Today + relativedelta(months=+z)).year
                                thisDate = datetime.datetime(thisYear, thisMonth, 1)

                                if (taskStartDate <= thisDate and taskEndDate >= thisDate):
                                    cr.set_source_rgb(taskR, taskG, taskB)
                                    if (row == (self.TimelineItem - 1)):
                                        cr.rectangle(timelinePositions[z][0],yPos-15, timelinePositions[z][2], textHeight+5)
                                    else:
                                        cr.rectangle(timelinePositions[z][0],yPos-15, timelinePositions[z][2]+self.HSPACER+1, textHeight+5)
                                    cr.fill()   
                                    if (rowMatch == 0):
                                        startPos = timelinePositions[z][0]
                                    rowMatch += 1
                                row += 1
                            totalBarWidth = timelineItemWidth * rowMatch
                            cr.set_source_rgb(0,0,1)
                            barTextX = startPos + (totalBarWidth / 2) - (textWidth / 2)
                            barTextY = yPos-3
                            cr.move_to(barTextX,barTextY)
                            cr.set_source_rgb(0,0,1)
                            cr.show_text(taskText)
                            j += 1
                    
                i += 1

        """ To do
        Done (1) Display task text on top of bar
        (2) Display group text as a block
        (3) Show milestones
        (4) Proporsion task bar according to the start and end date
        """
        footerText = "Powered by Mahere Kaihanga v0.1"
        cr.set_source_rgb(footerR, footerG, footerB)
        cr.set_font_size(10)
        footerXbearing, footerYbearing, footerWidth, footerHeight, dx, dy = cr.text_extents(footerText)
        cr.move_to((self.Width/2) - footerWidth/2, self.Height - 10)
        cr.show_text(footerText)

        if (len(fileName) == 0):
            fileName = "roadmap.png"
        surface.write_to_png(fileName)  # Output to PNG


if __name__ == "__main__":
    x = MahereKaihanga()
    x.Title = "This is my roadmap"

    x.Tasks = [
                {"group": "Group 1", "colour": "lightgreen", "tasks": [
                    {"task": "Feature 1", "start": datetime.datetime(2022, 10, 24), "end": datetime.datetime(2022, 11, 24), "colour": "lightgreen"},
                    {"task": "Feature 2", "start": datetime.datetime(2022, 12, 24), "end": datetime.datetime(2023, 4, 24), "colour": "lightgreen"}
                    ]},
                {"group": "Group 2", "colour": "lightgreen", "tasks": [
                    {"task": "Feature 3", "start": datetime.datetime(2022, 4, 24), "end": datetime.datetime(2022, 12, 24), "colour": "lightblue"},
                    {"task": "Feature 4", "start": datetime.datetime(2023, 1, 24), "end": datetime.datetime(2024, 12, 24), "colour": "lightblue"}
                    ]},
                {"group": "Group 3", "colour": "lightgreen", "tasks": [
                    {"task": "Feature 5", "start": datetime.datetime(2022, 10, 24), "end": datetime.datetime(2023, 3, 24), "colour": "yellow"},
                    {"task": "Feature 6", "start": datetime.datetime(2023, 4, 24), "end": datetime.datetime(2023, 7, 24), "colour": "yellow"},
                    {"task": "Feature 7", "start": datetime.datetime(2023, 8, 24), "end": datetime.datetime(2023, 8, 24), "colour": "yellow"}
                ]}              
            ]
    x.render("my_roadmap.png")


