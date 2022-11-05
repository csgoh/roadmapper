# roadmap_generator

Purpose: This application is used to generate graphical roadmap using code. 



## Example  
```python
from generator import Roadmap

my_roadmap = Mahere(1024, 420, "my_roadmap.png")

my_roadmap.title_text = "This is my roadmap!!"
my_roadmap.timeline_mode = Mahere.QUARTERLY
my_roadmap.timeline_item = 9

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
```
## Output

![name](my_roadmap.png)
