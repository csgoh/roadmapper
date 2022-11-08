# roadmap_generator

Purpose: This application is used to generate graphical roadmap using code.

## SDK Example

```python
my_roadmap = Roadmap(1000, 512)
my_roadmap.set_title("My Three Year Roadmap 2023~2025", font_size=18)
my_roadmap.set_timeline()

with Task("Task1", "2023-01-01", "2023-10-31") as task1:
    task1.add_milestone("Milestone 1", "2023-01-01", "Red")
    task1.add_milestone("Milestone 2", "2023-02-01", "Green")
    task1.add_milestone("Milestone 3", "2023-03-01", "Blue")

with Task("Task2", "2023-01-01", "2023-10-31") as task2:
    task2.add_milestone("Milestone 4", "2023-01-01", "Red")
    task2.add_milestone("Milestone 5", "2023-02-01", "Green")
    task2.add_milestone("Milestone 6", "2023-03-01", "Blue")

with Group("Group 1", "Arial", 18, "Black", "White") as group1:
    group1.add_task(task1)
    group1.add_task(task2)

my_roadmap.add_group(group1)

my_roadmap.set_footer("this is footer", font_size=10)
my_roadmap.draw()
my_roadmap.save()
```

## Output

![name](my_roadmap.png)

## Plain english example

```txt
Title This is my title
Footer This is my footer
Timescale is Monthly
Roadmap starts 2022-11-13
Timescale has 12 items
task font colour is black

(group 1) is coloured in green
	[task 1] starts 2022-12-01 ends 2023-06-30 coloured in lightgreen
		<v1.0 Go Live> happens 2022-06-30 coloured in red
	[task 2] starts 2023-03-01 ends 2023-08-30 coloured in lightgreen
		<v1.1 release> happens 2022-06-30 coloured in red

(group 2) is coloured in blue
	[task 1] starts 2022-12-01 ends 2023-06-30 coloured in lightgreen
	[task 2] starts 2023-03-01 ends 2023-08-30 coloured in lightgreen
	[task 3] starts 2023-03-01 ends 2023-08-30 coloured in lightgreen
		<v1.0 Go Live> happens 2022-06-30 coloured in red

```
