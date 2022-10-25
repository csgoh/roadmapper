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
        
        
        # create a default data structure if none is provided
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
        self.painter.setBackgroundColour(self.BackgroundColour)

        ###(1) Set Title      
        self.painter.setFont("Arial", 18, self.TitleColour)
        self.painter.drawTitle(self.Title, self.TitleColour)
        
        ###(2) Set Timeline
        # Determine max task text width
        groupTaskWidth = 0
        for x in taskData:
            groupText = x.get("group")
            self.painter.setFont("Arial", 12, x.get("colour"))
            groupTextWidth, groupTextHeight = self.painter.getTextDimension(groupText)
            if groupTextWidth > groupTaskWidth:
                groupTaskWidth = groupTextWidth + 20

        timelineWidth = self.Width - groupTaskWidth - (self.__HSPACER * self.TimelineItem) - 10
      
        timelineYPos = 40
        timelineHeight = 20
        
        timelineItemWidth = timelineWidth / self.TimelineItem

        timelinePositions = []
        for x in range(self.TimelineItem):
            timelineX = (x * timelineItemWidth) + groupTaskWidth + (self.__HSPACER * x)

            # Draw timeline item
            self.painter.setColour(self.TimelineFillColour)
            self.painter.drawBox(timelineX, timelineYPos, timelineItemWidth, timelineHeight)
            timelinePositions.append([timelineX, timelineYPos, timelineItemWidth, timelineHeight])

            # Draw timeline text
            thisMonth = self.__TODAY + relativedelta(months=+x)
            timelineText = str(thisMonth.strftime("%b")) + " " + str(thisMonth.year)

            #self.painter.setColour(self.TimelineTextColour)
            self.painter.setFont(self.TextFont, 12, self.TimelineTextColour)

            textWidth, textHeight = self.painter.getTextDimension(timelineText)
            posX, posY = self.painter.getDisplayTextPosision(timelineX, timelineYPos, timelineItemWidth, timelineHeight, timelineText, "centre")
            #print ("timeline : ", posX, posY, "-", timelineX, timelineYPos, timelineItemWidth, timelineHeight)
            self.painter.drawText(posX, posY, timelineText)
        
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
                
                self.painter.setFont("Arial", 12, self.TimelineTextColour)
                groupTaskWidth, groupTextHeight = self.painter.getTextDimension(groupText)
                if (nextGroupY == 0):
                    groupY = groupYPos + (groupTextHeight * i) + (self.__VSPACER * i) 
                else:
                    groupY = nextGroupY + 30
                
                self.painter.drawText(groupX, groupY, groupText)  
                i += 1
                nextGroupY = groupY
                
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
                            
                            textWidth, textHeight = self.painter.getTextDimension(taskText)
                            yPos = taskYPos + textHeight * j + (self.__VSPACER * j)
                            nextGroupY = yPos

                            # Draw task bar
                            row = 0
                            
                            taskStartMonth = task.get("start").month
                            taskEndMonth = task.get("end").month
                            taskStartDate = datetime.datetime(task.get("start").year, taskStartMonth, 1)
                            taskEndDate = datetime.datetime(task.get("end").year, taskEndMonth, 1)
                            
                            totalBarWidth = 0
                            startPos = 0
                            rowMatch = 0
                            for z in range(self.TimelineItem):
                                thisMonth = (self.__TODAY + relativedelta(months=+z)).month
                                thisYear = (self.__TODAY + relativedelta(months=+z)).year
                                thisDate = datetime.datetime(thisYear, thisMonth, 1)

                                if (taskStartDate <= thisDate and taskEndDate >= thisDate):
                                    self.painter.setColour(task.get("colour"))
                                    if (row == (self.TimelineItem - 1)):
                                        self.painter.drawBox(timelinePositions[z][0],yPos-15, timelinePositions[z][2], textHeight+5)
                                    else:
                                        self.painter.drawBox(timelinePositions[z][0],yPos-15, timelinePositions[z][2]+self.__HSPACER+1, textHeight+5)
                                    if (rowMatch == 0):
                                        startPos = timelinePositions[z][0]
                                    rowMatch += 1
                                row += 1
                            totalBarWidth = timelineItemWidth * rowMatch
                            
                            barTextX = startPos + (totalBarWidth / 2) - (textWidth / 2)
                            barTextY = yPos-3
                            self.painter.setColour(self.TimelineTextColour)
                            self.painter.drawText(barTextX, barTextY, taskText)
                            j += 1
                    
                i += 1

        """ To do
        Done (1) Display task text on top of bar
        (2) Display group text as a block
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




