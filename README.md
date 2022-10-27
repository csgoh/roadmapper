# roadmap_generator

Purpose: This application is used to generate graphical roadmap using code. 

Mahere Kaihanga means roadmap generator in Maori language.

## Example  
```python
    x = MahereKaihanga(1024, 800, "PNG", "my_roadmap.png")
    x.title = "This is my roadmap!"
    x.timeline_mode = MahereKaihanga.QUARTERLY
    x.timeline_item = 6

    x.tasks = [
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
                    {"task": "Feature 8", "start": datetime.datetime(2022, 5, 24), "end": datetime.datetime(2023, 11, 24), "colour": "Orchid"},
                    {"task": "Feature 9", "start": datetime.datetime(2022, 6, 24), "end": datetime.datetime(2023, 7, 24), "colour": "Orchid"},
                    {"task": "Feature 10", "start": datetime.datetime(2022, 8, 24), "end": datetime.datetime(2023, 8, 24), "colour": "Orchid"}
                ]},
                {"group": "Stream 5: Build Mobile App", "colour": "OrangeRed", "tasks": [
                    {"task": "Feature 11", "start": datetime.datetime(2023, 12, 24), "end": datetime.datetime(2024, 3, 24), "colour": "Coral"},
                    {"task": "Feature 12", "start": datetime.datetime(2024, 4, 24), "end": datetime.datetime(2024, 6, 24), "colour": "Coral"},
                    {"task": "Feature 13", "start": datetime.datetime(2024, 7, 24), "end": datetime.datetime(2024, 8, 24), "colour": "Coral"}
                ]}              
            ]
    x.render()
```
![name](my_roadmap.png)
