from generator.roadmap import Roadmap
from generator.timelinemode import TimelineMode

my_roadmap = Roadmap(width=1200, height=612)
my_roadmap.set_title("My Demo Roadmap 2023-2025", font_size=18)
# my_roadmap.set_timeline(TimelineMode.MONTHLY, "2022-12-01", 12, font_size=11)
my_roadmap.set_timeline(TimelineMode.QUARTERLY, "2022-12-15", 4, font_size=11)

with my_roadmap.add_group(
    "Group 1 something long", "Arial", 12, "Black", "White"
) as group1:
    with group1.add_task(
        "Task 1", "2023-01-01", "2023-06-01", "Arial", 10, "Black", "LightGreen"
    ) as task1:
        pass
#         task1.add_milestone("Milestone 1", "2023-01-15", "Arial", 10, "Red", "Red")
#         task1.add_milestone("Milestone 2", "2023-03-01", "Arial", 10, "Red", "Red")
#         task1.add_milestone("Milestone 3", "2023-05-31", "Arial", 10, "Red", "Red")
#         with task1.add_parellel_task(
#             "Task 1a",
#             "2023-07-15",
#             "2023-10-31",
#             "Arial",
#             10,
#             "Black",
#             "LightBlue",
#         ) as task1a:
#             task1a.add_milestone(
#                 "Milestone 1a", "2023-07-30", "Arial", 10, "Red", "Red"
#             )
#             task1a.add_milestone(
#                 "Milestone 2a", "2023-10-30", "Arial", 10, "Red", "Red"
#             )
#     with group1.add_task(
#         "Task 2", "2023-03-01", "2023-05-07", "Arial", 10, "Black", "LightGreen"
#     ) as task2:
#         task2.add_milestone("Milestone 4", "2023-03-15", "Arial", 10, "Red", "Red")
#         task2.add_milestone("Milestone 5", "2023-05-07", "Arial", 10, "Red", "Red")

# with my_roadmap.add_group("Stream 2", "Arial", 12, "Black", "White") as group2:
#     with group2.add_task(
#         "Task 3", "2023-04-01", "2023-08-30", "Arial", 10, "Black", "LightGreen"
#     ) as task3:
#         task3.add_milestone("Milestone 6", "2023-05-15", "Arial", 10, "Red", "Red")
#         task3.add_milestone("Milestone 7", "2023-08-01", "Arial", 10, "Red", "Red")

# with my_roadmap.add_group("Stream 3", "Arial", 12, "Black", "White") as group3:
#     with group3.add_task(
#         "Task 4", "2023-04-01", "2023-08-30", "Arial", 10, "Black", "LightGreen"
#     ) as task3:
#         pass
#     with group3.add_task(
#         "Task 5", "2023-04-01", "2023-08-30", "Arial", 10, "Black", "LightGreen"
#     ):
#         pass

my_roadmap.set_footer("this is footer!!", font_size=10)
my_roadmap.draw()
my_roadmap.save()
my_roadmap.print_roadmap("groups")
