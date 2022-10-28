from kaihanga import Mahere

my_roadmap = Mahere(800, 420, "my_roadmap.png")

my_roadmap.title_text = "This is my roadmap!!!!!"
    
my_roadmap.timeline_mode = Mahere.HALF_YEARLY
my_roadmap.timeline_item = 6

group1 = my_roadmap.add_group("Stream 1: Develop base", "green")
my_roadmap.add_task(group1, "Feature 1", "2022-10-24", "2022-11-24", "lightgreen")
my_roadmap.add_task(group1, "Feature 2", "2022-12-24", "2023-04-24", "lightgreen")
    
group2 = my_roadmap.add_group("Stream 2: Enable monitoring", "blue")
my_roadmap.add_task(group2, "Feature 3", "2022-04-24", "2022-12-24", "lightblue")
my_roadmap.add_task(group2, "Feature 4", "2023-01-24", "2024-12-24", "lightblue")

group3 = my_roadmap.add_group("Stream 3: Support reporting", "grey")
my_roadmap.add_task(group3, "Feature 5", "2022-10-24", "2023-03-24", "lightgrey")
my_roadmap.add_task(group3, "Feature 6", "2023-04-24", "2023-07-24", "lightgrey")
my_roadmap.add_task(group3, "Feature 7", "2023-08-24", "2023-08-24", "lightgrey")
    
group4 = my_roadmap.add_group("Stream 4: Implement ML analytics", "Purple")
my_roadmap.add_task(group4, "Feature 8", "2022-05-24", "2023-11-24", "Orchid")
my_roadmap.add_task(group4, "Feature 9", "2022-06-24", "2023-07-24", "Orchid")
my_roadmap.add_task(group4, "Feature 10", "2022-08-24", "2023-08-24", "Orchid")

group5 = my_roadmap.add_group("Stream 5: Build Mobile App", "OrangeRed")
my_roadmap.add_task(group5, "Feature 11", "2023-12-24", "2024-03-24", "Coral")
my_roadmap.add_task(group5, "Feature 12", "2024-04-24", "2024-06-24", "Coral")
my_roadmap.add_task(group5, "Feature 13", "2024-07-24", "2024-08-24", "Coral")

my_roadmap.render()