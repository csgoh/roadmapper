# RoadMapGenerator
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


class RoadmapGenerator():
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

    def render(self):
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
            taskText = x.get("task")
            textXbearing, textYbearing, textWidth, textHeight, dx, dy = cr.text_extents(taskText)
            #print (">" + x + ":" + str(textWidth))
            if textWidth > taskWidth:
                taskWidth = textWidth + 100

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
                textXbearing, textYbearing, groupWidth, groupHeight, dx, dy = cr.text_extents(groupText)
                if (nextGroupY == 0):
                    groupY = groupYPos + (groupHeight * i) + (self.VSPACER * i) 
                else:
                    groupY = nextGroupY + 30

                cr.move_to(groupX, groupY)
                #print("Group: ", groupText, str(groupX), str(groupY), str(groupWidth))
                cr.show_text(groupText)
                
                ###(4) Set Task
                taskYPos = groupY + groupHeight + 10

                nextGroupY = taskYPos 

                j = 0
                taskX = groupWidth 
                for y in taskData:
                    # Draw task item
                    #print (">", groupText, y.get("group"))
                    if (groupText == y.get("group")):
                        
                        taskText = y.get("task")
                        #print (">>>>", taskText)
                        
                        cr.set_source_rgb(tltcR, tltcG, tltcB)
                        textXbearing, textYbearing, textWidth, textHeight, dx, dy = cr.text_extents(taskText)
                        yPos = taskYPos + textHeight * j + (self.VSPACER * j)
                       
                        cr.move_to(taskX, yPos)
                        
                        cr.show_text(taskText)
                        nextGroupY = yPos
                        #print (">nextGroupY", nextGroupY)

                        # Draw task bar
                        taskR, taskG, taskB = self.rgb_to_float(x.get("colour"))

                        #print(taskText, "Task date: " + str(taskData[i]["start"].month) + " - " + str(taskData[i]["end"].month))
                        row = 0
                        
                        taskStartMonth = y.get("start").month
                        taskEndMonth = y.get("end").month
                        taskStartDate = datetime.datetime(y.get("start").year, taskStartMonth, 1)
                        taskEndDate = datetime.datetime(y.get("end").year, taskEndMonth, 1)
                        #print ("task : ", j, taskText, taskStartDate, taskEndDate)

                        for z in range(self.TimelineItem):
                            thisMonth = (self.Today + relativedelta(months=+z)).month
                            thisYear = (self.Today + relativedelta(months=+z)).year
                            thisDate = datetime.datetime(thisYear, thisMonth, 1)

                            if (taskStartDate <= thisDate and taskEndDate >= thisDate):
                                #print("     Task Position: ", taskText, str(taskX), str(yPos))
                                cr.set_source_rgb(taskR, taskG, taskB)
                                if (row == (self.TimelineItem - 1)):
                                    #print (row, timelineItem)
                                    cr.rectangle(timelinePositions[z][0],yPos-15, timelinePositions[z][2], textHeight+5)
                                else:
                                    cr.rectangle(timelinePositions[z][0],yPos-15, timelinePositions[z][2]+self.HSPACER+1, textHeight+5)
                                cr.fill()    
                            row += 1
                        j += 1
                    
                i += 1

        """ To do
        (1) Display task text on top of bar
        (2) Display group text as a block
        (3) Show milestones
        (4) Proporsion task bar according to the start and end date
        """
        footerText = "Powered by RoadMapGenerator"
        cr.set_source_rgb(footerR, footerG, footerB)
        cr.set_font_size(10)
        footerXbearing, footerYbearing, footerWidth, footerHeight, dx, dy = cr.text_extents(footerText)
        cr.move_to((self.Width/2) - footerWidth/2, self.Height - 10)
        cr.show_text(footerText)

        surface.write_to_png("example.png")  # Output to PNG


if __name__ == "__main__":
    x = RoadmapGenerator()
    x.Title = "This is my roadmap"
    x.Tasks = [
                {"group": "Sample Group 1", "task": "Feature 1", "start": datetime.datetime(2022, 10, 24), "end": datetime.datetime(2022, 11, 24), "colour": "lightgreen"},
                {"group": "Sample Group 1", "task": "Feature 2", "start": datetime.datetime(2022, 12, 24), "end": datetime.datetime(2023, 4, 24), "colour": "lightgreen"},
                {"group": "Sample Group 2", "task": "Feature 3", "start": datetime.datetime(2022, 4, 24), "end": datetime.datetime(2022, 12, 24), "colour": "lightblue"},
                {"group": "Sample Group 2", "task": "Feature 4", "start": datetime.datetime(2023, 1, 24), "end": datetime.datetime(2024, 12, 24), "colour": "lightblue"},
                {"group": "Sample Group 3", "task": "Feature 5", "start": datetime.datetime(2022, 10, 24), "end": datetime.datetime(2023, 3, 24), "colour": "yellow"},
                {"group": "Sample Group 3", "task": "Feature 6", "start": datetime.datetime(2023, 4, 24), "end": datetime.datetime(2023, 7, 24), "colour": "yellow"},
              
            ]
    x.render()
    #print(x.rgb_to_float("Pink"))

