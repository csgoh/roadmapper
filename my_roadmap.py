from generator import roadmap

my_roadmap = roadmap(1400, 512, "my_roadmap.png")

my_roadmap.title_text = "Product Development Roadmap"
my_roadmap.timeline_mode = roadmap.QUARTERLY
my_roadmap.timeline_item = 3
my_roadmap.show_footer = True

group1 = my_roadmap.add_group("Stream 1: Core Functionality")
task1 = my_roadmap.add_task(group1, "Foundation", "2022-10-24", "2023-02-24")
task2 = my_roadmap.add_task(group1, "Core Function 1", "2022-12-24", "2023-04-24")
task3 = my_roadmap.add_task(group1, "Core Function 2", "2023-04-01", "2023-08-30")
my_roadmap.add_milestone(group1, task1, "v1.0 Release", "2023-02-24")
my_roadmap.add_milestone(group1, task2, "v1.1 Release", "2023-04-24")
my_roadmap.add_milestone(group1, task3, "v1.2 Release", "2023-08-30")

# group2 = my_roadmap.add_group("Stream 2: Analytics & Reporting")
# task4 = my_roadmap.add_task(group2, "Reporting Server", "2022-11-24", "2023-03-24")
# task5 = my_roadmap.add_task(group2, "Analytics Engine", "2023-01-24", "2023-06-24")
# task6 = my_roadmap.add_task(group2, "Reporting Portal", "2023-01-24", "2023-08-30")

# my_roadmap.add_milestone(group2, task6, "Go Live", "2023-03-30")
# my_roadmap.add_milestone(group2, task6, "Major Enhancement", "2023-08-30")

# group5 = my_roadmap.add_group("Stream 3: Mobile App")
# task7 = my_roadmap.add_task(group5, "iOS App", "2023-06-01", "2024-01-24")
# task8 = my_roadmap.add_task(group5, "Android App", "2023-08-01", "2024-02-24")
# my_roadmap.add_milestone(group5, task7, "iOS App v1.0 release", "2023-08-30")
# my_roadmap.add_milestone(group5, task7, "iOS App v1.1 release", "2024-01-24")
# my_roadmap.add_milestone(group5, task8, "Android App v1.0 release", "2023-09-30")
# my_roadmap.add_milestone(group5, task8, "Android App v1.1 release", "2024-02-24")


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
