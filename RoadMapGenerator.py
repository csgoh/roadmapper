import math
import cairo
import datetime
from webcolors import name_to_rgb
from dateutil.relativedelta import relativedelta


class RoadmapGenerator():
    def __init__(self) -> None:
        pass

    def rgb_to_float(self, colour):
        # Convert RGBS to floats
        fRGBS = name_to_rgb(colour)
        return [x / 255 for x in fRGBS]
        #return fRGBS[0] / 255, fRGBS[1] / 255, fRGBS[2] / 255

    def paint(self):
        WIDTH, HEIGHT = 1024 , 3000 
 
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        cr = cairo.Context(surface)
        
        ### Setup
        VSPACER, HSPACER = 12, 2
        backgroundColour = "White"
        title = "This is a very looooooong roadmap title!!!!!"
        
        titleColour = "Black"
        timelineMode = "Month"
        timelineItem = 12
        timelineStartDate = datetime.datetime(2022,10, 24)
        timelineFillColour = "Salmon"
        timelineTextColour = "DarkRed"

        titleR, titleG, titleB = self.rgb_to_float(titleColour)
        tlfcR, tlfcG, tlfcB = self.rgb_to_float(timelineFillColour)
        tltcR, tltcG, tltcB = self.rgb_to_float(timelineTextColour)

        today = datetime.datetime.today()

        # create a list of tasks
        tasks = ["Tranche 1 - Feature 1", "Tranche 1 - Feature 2", "Task 3sa sad", "Task 4"]

        # create a data structure contains task name, start date, end date, and color
        taskData = [
            {"group": "Tranche 1", "task": "Feature 1", "start": datetime.datetime(2022, 10, 24), "end": datetime.datetime(2022, 11, 24), "colour": "lightgreen"},
            {"group": "Tranche 1", "task": "Feature 2", "start": datetime.datetime(2023, 3, 24), "end": datetime.datetime(2023, 12, 24), "colour": "lightgreen"},
            {"group": "Tranche 1", "task": "Feature 3 blah", "start": datetime.datetime(2022, 12, 24), "end": datetime.datetime(2023, 6, 24), "colour": "lightgreen"},
            {"group": "Tranche 1", "task": "Task 4", "start": datetime.datetime(2023, 1, 24), "end": datetime.datetime(2023, 2, 24), "colour": "lightgreen"},
            {"group": "Tranche 2", "task": "Feature 5", "start": datetime.datetime(2022, 4, 24), "end": datetime.datetime(2022, 12, 24), "colour": "lightblue"},
            {"group": "Tranche 2", "task": "Feature 6", "start": datetime.datetime(2023, 10, 24), "end": datetime.datetime(2024, 12, 24), "colour": "lightblue"},
            {"group": "Tranche 2", "task": "Feature 7 blah", "start": datetime.datetime(2023, 1, 24), "end": datetime.datetime(2023, 6, 24), "colour": "lightblue"},
            {"group": "Tranche 2", "task": "Task 8", "start": datetime.datetime(2022, 1, 24), "end": datetime.datetime(2022, 10, 24), "colour": "lightblue"},
            {"group": "Tranche 3", "task": "Feature 9", "start": datetime.datetime(2022, 10, 24), "end": datetime.datetime(2022, 11, 24), "colour": "yellow"},
            {"group": "Tranche 3", "task": "Feature 10", "start": datetime.datetime(2023, 8, 24), "end": datetime.datetime(2023, 12, 24), "colour": "yellow"},
            {"group": "Tranche 3", "task": "Feature 11 blah", "start": datetime.datetime(2022, 12, 24), "end": datetime.datetime(2023, 6, 24), "colour": "yellow"},
            {"group": "Tranche 3", "task": "Task 12", "start": datetime.datetime(2023, 1, 24), "end": datetime.datetime(2023, 2, 24), "colour": "yellow"},
        ]


        ###(0) Set backgroud
        cr.set_source_rgb(*self.rgb_to_float("White"))
        cr.paint()

        ###(1) Set Title
        cr.set_source_rgb(titleR, titleG, titleB)
        cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(18)
        textXbearing, textYbearing, textWidth, textHeight, dx, dy = cr.text_extents(title)
        cr.move_to((WIDTH/2) - textWidth/2, 30)
        cr.show_text(title)
        
        ###(2) Set Timeline
        # Determine max task text width
        taskWidth = 0
        for x in tasks:
            taskText = x
            textXbearing, textYbearing, textWidth, textHeight, dx, dy = cr.text_extents(taskText)
            #print (">" + x + ":" + str(textWidth))
            if textWidth > taskWidth:
                taskWidth = textWidth

        #print (taskWidth)
        timelineWidth = WIDTH - taskWidth - (HSPACER * timelineItem)
        
        timelineYPos = 40
        timelineHeight = 20
        
        timelineItemWidth = timelineWidth / timelineItem

        timelinePositions = []
        for x in range(timelineItem):
            timelineX = (x * timelineItemWidth) + taskWidth + (HSPACER * x)

            # Draw timeline item
            cr.set_source_rgb(tlfcR, tlfcG, tlfcB)
            cr.rectangle(timelineX,timelineYPos, timelineItemWidth, timelineHeight)
            timelinePositions.append([timelineX, timelineYPos, timelineItemWidth, timelineHeight])
            cr.fill()

            # Draw timeline text
            cr.set_source_rgb(tltcR, tltcG, tltcB)
            cr.set_font_size(12)

            thisMonth = today + relativedelta(months=+x)
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
                    groupY = groupYPos + (groupHeight * i) + (VSPACER * i) 
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
                        yPos = taskYPos + textHeight * j + (VSPACER * j)
                       
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

                        for z in range(timelineItem):
                            thisMonth = (today + relativedelta(months=+z)).month
                            thisYear = (today + relativedelta(months=+z)).year
                            thisDate = datetime.datetime(thisYear, thisMonth, 1)

                            if (taskStartDate <= thisDate and taskEndDate >= thisDate):
                                #print("     Task Position: ", taskText, str(taskX), str(yPos))
                                cr.set_source_rgb(taskR, taskG, taskB)
                                if (row == (timelineItem - 1)):
                                    #print (row, timelineItem)
                                    cr.rectangle(timelinePositions[z][0],yPos-15, timelinePositions[z][2], textHeight+5)
                                else:
                                    cr.rectangle(timelinePositions[z][0],yPos-15, timelinePositions[z][2]+HSPACER+1, textHeight+5)
                                cr.fill()    
                            row += 1
                        j += 1
                    
                i += 1
                #if (i == 2): break

        """ Elements of roadmap
        Done (1) Title
        Done (2) Timeline       
        (3) Grouping of item (4)
        Done (4) Tasks/Functions/Activities/Steps
        (4) Milestone
        """

        surface.write_to_png("example.png")  # Output to PNG


if __name__ == "__main__":
    x = RoadmapGenerator()
    x.paint()
    #print(x.rgb_to_float("Pink"))

