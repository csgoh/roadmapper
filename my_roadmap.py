from kaihanga import Mahere

my_roadmap = Mahere(1024, 417, "my_roadmap.png")

my_roadmap.title_text = "This is my roadmap!!!"
# my_roadmap.timeline_fill_colour = "#527a7a"
# my_roadmap.timeline_text_colour = "White"
my_roadmap.timeline_mode = Mahere.QUARTERLY
my_roadmap.timeline_item = 9
# my_roadmap.group_text_colour = "Black"
# my_roadmap.task_text_colour = "Black"
my_roadmap.show_footer = True

group1 = my_roadmap.add_group("Stream 1: Develop base")
my_roadmap.add_task(group1, "Feature 1", "2022-10-24", "2022-11-24")
my_roadmap.add_task(group1, "Feature 2", "2022-12-24", "2023-04-24")

group2 = my_roadmap.add_group("Stream 2: Enable monitoring")
my_roadmap.add_task(group2, "Feature 3", "2022-04-24", "2022-12-24")
my_roadmap.add_task(group2, "Feature 4", "2023-01-24", "2024-12-24")

group3 = my_roadmap.add_group("Stream 3: Support reporting")
my_roadmap.add_task(group3, "Feature 5", "2022-10-24", "2023-03-24")
my_roadmap.add_task(group3, "Feature 6", "2023-04-24", "2023-07-24")
my_roadmap.add_task(group3, "Feature 7", "2023-08-24", "2023-08-24")

group4 = my_roadmap.add_group("Stream 4: Implement ML analytics")
my_roadmap.add_task(group4, "Feature 8", "2022-05-24", "2023-11-24")
my_roadmap.add_task(group4, "Feature 9", "2022-06-24", "2023-07-24")
my_roadmap.add_task(group4, "Feature 10", "2022-08-24", "2023-08-24")

group5 = my_roadmap.add_group("Stream 5: Build Mobile App")
my_roadmap.add_task(group5, "Feature 11", "2023-12-24", "2024-03-24")
my_roadmap.add_task(group5, "Feature 12", "2024-04-24", "2024-06-24")
my_roadmap.add_task(group5, "Feature 13", "2024-07-24", "2024-08-24")


# group1 = my_roadmap.add_group("Stream 1: Develop base", "#80ffff")
# group1 = my_roadmap.add_group("Stream 1: Develop base")
# my_roadmap.add_task(group1, "Feature 1", "2022-10-24", "2022-11-24", "#ccffff")
# my_roadmap.add_task(group1, "Feature 2", "2022-12-24", "2023-04-24", "#ccffff")

# group2 = my_roadmap.add_group("Stream 2: Enable monitoring", "#80ff80")
# my_roadmap.add_task(group2, "Feature 3", "2022-04-24", "2022-12-24", "#ccffcc")
# my_roadmap.add_task(group2, "Feature 4", "2023-01-24", "2024-12-24", "#ccffcc")

# group3 = my_roadmap.add_group("Stream 3: Support reporting", "#ffff80")
# my_roadmap.add_task(group3, "Feature 5", "2022-10-24", "2023-03-24", "#ffffcc")
# my_roadmap.add_task(group3, "Feature 6", "2023-04-24", "2023-07-24", "#ffffcc")
# my_roadmap.add_task(group3, "Feature 7", "2023-08-24", "2023-08-24", "#ffffcc")

# group4 = my_roadmap.add_group("Stream 4: Implement ML analytics", "#ff80ff")
# my_roadmap.add_task(group4, "Feature 8", "2022-05-24", "2023-11-24", "#ffccff")
# my_roadmap.add_task(group4, "Feature 9", "2022-06-24", "2023-07-24", "#ffccff")
# my_roadmap.add_task(group4, "Feature 10", "2022-08-24", "2023-08-24", "#ffccff")

# group5 = my_roadmap.add_group("Stream 5: Build Mobile App", "#ff8080")
# my_roadmap.add_task(group5, "Feature 11", "2023-12-24", "2024-03-24", "#ffcccc")
# my_roadmap.add_task(group5, "Feature 12", "2024-04-24", "2024-06-24", "#ffcccc")
# my_roadmap.add_task(group5, "Feature 13", "2024-07-24", "2024-08-24", "#ffcccc")

my_roadmap.render()
print(f"{my_roadmap.__repr__()}")
