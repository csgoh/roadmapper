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
    TextFont = "Arial"
    
    BackgroundColour = "White"
    Title = "This is a sample title"    
    TitleColour = "Black"
    FooterColour = TitleColour
    TimelineMode = "Month"
    TimelineItem = 12
    TimelineFillColour = "Salmon"
    TimelineTextColour = "Black"
    
    TaskTextColour = "Black"

    Tasks = []
    
    def __init__(self, width, height) -> None:
        self.painter = Painter(width, height)
        self.Width = width
        self.Height = height

    def render(self, fileName):
        
        
        # create a sample data structure if none is provided
        if (len(self.Tasks) == 0):
            taskData = [
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
            taskData = self.Tasks


        ###(0) Set backgroud
        self.painter.setBackgroundColour(self.BackgroundColour)

        ###(1) Set Title      
        self.painter.setFont("Arial", 18, self.TitleColour)
        self.painter.drawTitle(self.Title, self.TitleColour)
        
        ###(2) Set Timeline
        # Determine max group text width
        maxGroupTextWidth = 0
        for x in taskData:
            groupText = x.get("group")
            self.painter.setFont("Arial", 12, x.get("colour"))
            groupTextWidth, groupTextHeight = self.painter.getTextDimension(groupText)
            if groupTextWidth > maxGroupTextWidth:
                maxGroupTextWidth = groupTextWidth + 20

        # 20px is for right margin
        timelineWidth = self.Width - maxGroupTextWidth - (self.__HSPACER * self.TimelineItem) - 20 - 20
      
        timelineYPos = 40
        timelineHeight = 20
        
        timelineItemWidth = timelineWidth / self.TimelineItem

        timelinePositions = []
        for x in range(self.TimelineItem):
            timelineXPos = (x * timelineItemWidth) + maxGroupTextWidth + (self.__HSPACER * x) + 30

            # Draw timeline item
            self.painter.setColour(self.TimelineFillColour)
            self.painter.drawBox(timelineXPos, timelineYPos, timelineItemWidth, timelineHeight)
            timelinePositions.append([timelineXPos, timelineYPos, timelineItemWidth, timelineHeight])

            # Draw timeline text
            thisMonth = self.__TODAY + relativedelta(months=+x)
            timelineText = f"{thisMonth.strftime('%b')} {thisMonth.year}"
            self.painter.setFont(self.TextFont, 12, self.TimelineTextColour)
            xPos, yPos = self.painter.getDisplayTextPosision(timelineXPos, timelineYPos, timelineItemWidth, timelineHeight, timelineText, "centre")
            self.painter.drawText(xPos, yPos, timelineText)
        
        ###(3) Set Group
        groupYStartPos = 70
        groupHeight = 0

        i = 0
        lastGroupText = ""
        nextGroupYPos = 0
        groupXPos = 10
        groupYPos = 0
        for x in taskData:
            groupText = x.get("group")
                
            self.painter.setFont("Arial", 12, self.TimelineTextColour)
            groupTaskWidth, groupTextHeight = self.painter.getTextDimension(groupText)
            if (nextGroupYPos == 0):
                groupYPos = groupYStartPos + (groupTextHeight * i) + (self.__VSPACER * i) 
            else:
                groupYPos = nextGroupYPos + 30
            
            self.painter.drawGroup(groupXPos, groupYPos, maxGroupTextWidth, x)
            nextGroupYPos = groupYPos
            
            ###(4) Set Task
            taskYPos = groupYPos 
            nextGroupYPos = taskYPos 

            j = 0
            taskXPos = groupTextWidth 
            for task in x.get("tasks"):
                taskText = task.get("task")
                textWidth, textHeight = self.painter.getTextDimension(taskText)
                yPos = taskYPos + textHeight * j + (self.__VSPACER * j)
                nextGroupYPos = yPos
                textHeight = 20

                # Draw task bar
                row = 0
                
                taskStartDate = datetime.datetime(task.get("start").year, task.get("start").month, 1)
                taskEndDate = datetime.datetime(task.get("end").year, task.get("end").month, 1)
                
                barStartXPos = 0
                totalBarWidth = 0
                startXPos = 0
                rowMatch = 0
                for z in range(self.TimelineItem):
                    thisMonth = (self.__TODAY + relativedelta(months=+z)).month
                    thisYear = (self.__TODAY + relativedelta(months=+z)).year
                    thisDate = datetime.datetime(thisYear, thisMonth, 1)

                    if (taskStartDate <= thisDate and taskEndDate >= thisDate):
                        taskBoxXPos = timelinePositions[z][0]
                        taskBoxWidth = timelinePositions[z][2]
                        if (barStartXPos == 0):
                            barStartXPos = taskBoxXPos
                        
                        rowMatch += 1
                    row += 1

                taskBoxYPos = yPos
                taskBoxHeight = textHeight
                totalBarWidth = taskBoxWidth * rowMatch + (self.__HSPACER * rowMatch - 1)
                
                self.painter.setColour(task.get("colour"))
                self.painter.drawBox(barStartXPos,taskBoxYPos, totalBarWidth, taskBoxHeight)
                
                self.painter.setFont(self.TextFont, 12, self.TimelineTextColour)
                xPos, yPos = self.painter.getDisplayTextPosision(barStartXPos, taskBoxYPos, totalBarWidth, textHeight, taskText, "centre")
                self.painter.drawText(xPos, yPos, taskText)

                j += 1
                    
                i += 1

        """ To do
        Done (1) Display task text on top of bar
        Done (2) Display group text as a block
        (3) Show milestones
        (4) Proporsion task bar according to the start and end date
        """
        footerText = "Generated by Mahere Kaihanga v0.1"
        self.painter.drawFooter(footerText, self.FooterColour)

        self.painter.saveSurfaceToPNG(fileName)
        


if __name__ == "__main__":
    x = MahereKaihanga(1024, 512)
    x.Title = "This is my roadmap!!"

    x.Tasks = [
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




