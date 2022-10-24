import math
import cairo
import datetime
from webcolors import name_to_rgb
from dateutil.relativedelta import relativedelta


class RoadmapGenerator():
    def __init__(self) -> None:
        pass

    def paint(self):
        WIDTH, HEIGHT = 1748 , 1240 
 
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        cr = cairo.Context(surface)
        
        ### Setup
        backgroundColour = "White"
        title = "This is a very looooooong roadmap title!!!!!"
        
        titleColour = "Black"
        timelineMode = "Month"
        timelineItem = 9
        timelineStartDate = datetime.datetime(2022,10, 24)
        timelineFillColour = "Salmon"
        timelineTextColour = "DarkRed"

        titleR, titleG, titleB = name_to_rgb(titleColour)
        tlfcR, tlfcG,tlfcB = name_to_rgb(timelineFillColour)
        tltcR, tltcG,tltcB = name_to_rgb(timelineTextColour)

        today = datetime.datetime.today()

        # create a list of tasks
        tasks = ["Task 1", "Task 2", "Task 3", "Task 4"]


        #(0) Set backgroud
        cr.set_source_rgb(255, 255, 255)
        cr.rectangle(0,0,WIDTH,HEIGHT)
        cr.fill()

        #(1) Set Title
        cr.set_source_rgb(titleR/255, titleG/255, titleB/255)
        cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(18)
        textXbearing, textYbearing, textWidth, textHeight, dx, dy = cr.text_extents(title)
        cr.move_to((WIDTH/2) - textWidth/2, 30)
        cr.show_text(title)
        
        #(2) Set Timeline
        taskWidth = 300
        spacer = 2 
        timelineWidth = WIDTH - taskWidth - (spacer * timelineItem)
        
        timelineYPos = 40
        timelineHeight = 20
        
        timelineItemWidth = timelineWidth / timelineItem

        if timelineMode == "Month":
            timelineItemText = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"]

        for x in range(timelineItem):
            timelineX = (x * timelineItemWidth) + taskWidth + (spacer * x)

            # Draw timeline item
            cr.set_source_rgb(tlfcR/256, tlfcG/256, tlfcB/256)
            cr.rectangle(timelineX,timelineYPos, timelineItemWidth, timelineHeight)
            cr.fill()

            # Draw timeline text
            cr.set_source_rgb(tltcR/256, tltcG/256, tltcB/256)
            cr.set_font_size(12)
            #timelineText = timelineItemText[x]
            thisMonth = today + relativedelta(months=+x)
            timelineText = str(thisMonth.strftime("%b")) + " " + str(thisMonth.year)
            textXbearing, textYbearing, textWidth, textHeight, dx, dy = cr.text_extents(timelineText)
            cr.move_to(timelineX + timelineItemWidth/2 - (textWidth / 2), timelineYPos + 10 + (textHeight / 2))
            cr.show_text(timelineText)
                      
       
        #(4) Set Task

        taskYPos = 100
        taskHeight = 20

        i = 0
        for x in tasks:
            taskX = 10
            taskY = 0
            taskWidth = 300
            taskHeight = 20

            taskText = x
            print (taskText)
            cr.set_source_rgb(tltcR/256, tltcG/256, tltcB/256)
            textXbearing, textYbearing, textWidth, textHeight, dx, dy = cr.text_extents(taskText)
            cr.move_to(taskX, taskYPos + (taskHeight * i))
            cr.show_text(taskText)


            cr.set_source_rgb(0, 0, 0)
            cr.rectangle(taskX, taskY, taskWidth, taskHeight)
            cr.fill()
            i += 1

        """ Elements of roadmap
        Done (1) Title
        Done (2) Timeline       
        (3) Grouping of item (4)
        (4) Tasks/Functions/Activities/Steps
        (4) Milestone
        """
        


        surface.write_to_png("example.png")  # Output to PNG



x = RoadmapGenerator()
x.paint()

