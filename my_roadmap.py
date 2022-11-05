from generator import Roadmap

my_roadmap = Roadmap(1400, 612, "my_roadmap.png")

my_roadmap.title_text = "This is my roadmap!!!"
# my_roadmap.timeline_fill_colour = "#527a7a"
# my_roadmap.timeline_text_colour = "White"
my_roadmap.timeline_mode = Roadmap.YEARLY
my_roadmap.timeline_item = 6
# my_roadmap.group_text_colour = "Black"
# my_roadmap.task_text_colour = "Black"
my_roadmap.show_footer = True

group1 = my_roadmap.add_group("Stream 1: Develop base")
task1 = my_roadmap.add_task(group1, "Feature 1", "2022-10-24", "2022-11-24")
task2 = my_roadmap.add_task(group1, "Feature 2", "2022-12-24", "2023-04-24")
my_roadmap.add_milestone(group1, task1, "v1.0 MVP", "2022-11-01")
my_roadmap.add_milestone(group1, task2, "v1.1", "2023-04-24")
my_roadmap.add_milestone(group1, task2, "v1.2", "2023-12-15")

group2 = my_roadmap.add_group("Stream 2: Enable monitoring")
task3 = my_roadmap.add_task(group2, "Feature 3", "2022-04-24", "2023-01-24")
my_roadmap.add_milestone(group2, task3, "Monitoring Portal 1", "2022-12-30")

task4 = my_roadmap.add_task(group2, "Feature 4", "2023-01-24", "2024-12-24")
my_roadmap.add_milestone(group2, task4, "Monitoring Portal 2", "2023-06-30")

group3 = my_roadmap.add_group("Stream 3: Support reporting")
task5 = my_roadmap.add_task(group3, "Feature 5", "2022-10-24", "2023-03-24")
my_roadmap.add_milestone(group3, task5, "Reporting Framework", "2023-03-24")
task6 = my_roadmap.add_task(group3, "Feature 6", "2023-04-24", "2023-07-24")
my_roadmap.add_milestone(group3, task6, "Reporting server", "2023-06-30")

task7 = my_roadmap.add_task(group3, "Feature 7", "2023-08-24", "2023-08-24")
my_roadmap.add_milestone(group3, task7, "Reporting Portal", "2023-08-30")

group4 = my_roadmap.add_group("Stream 4: Implement ML analytics")
my_roadmap.add_task(group4, "Feature 8", "2022-05-24", "2023-11-24")
my_roadmap.add_task(group4, "Feature 9", "2022-06-24", "2023-07-24")
my_roadmap.add_task(group4, "Feature 10", "2022-08-24", "2023-08-24")

group5 = my_roadmap.add_group("Stream 5: Build Mobile App")
my_roadmap.add_task(group5, "Feature 11", "2023-12-24", "2024-03-24")
my_roadmap.add_task(group5, "Feature 12", "2024-04-24", "2024-06-24")
my_roadmap.add_task(group5, "Feature 13", "2024-07-24", "2024-08-24")


my_roadmap.render()
# print(f"{my_roadmap.__repr__()}")

## Idea
# with my_roadmap.add_group("Stream 2: Develop base") as group2:
#     with my_roadmap.add_task(group2, "Feature 3", "2022-10-24", "2022-11-24") as task3:
#         my_roadmap.add_milestone(group2, task3, "v1.0 MVP", "2022-11-01")
#         my_roadmap.add_milestone(group2, task3, "v1.1", "2023-06-28")
#         my_roadmap.add_milestone(group2, task3, "v1.2", "2023-12-15")
#     with my_roadmap.add_task(group2, "Feature 4", "2022-12-24", "2023-04-24") as task4:
#         my_roadmap.add_milestone(group2, task4, "v1.0 MVP", "2022-11-01")
#         my_roadmap.add_milestone(group2, task4, "v1.1", "2023-06-28")
#         my_roadmap.add_milestone(group2, task4, "v1.2", "2023-12-15")
