from roadmapper.roadmap import Roadmap
from roadmapper.timelinemode import TimelineMode


def readme_roadmap():
    roadmap = Roadmap(1200, 400, colour_theme="BLUEMOUNTAIN")
    roadmap.set_title("My Demo Roadmap")
    roadmap.set_subtitle("Matariki Technologies Ltd")
    roadmap.set_timeline(TimelineMode.MONTHLY, "2023-01-01", 12)
    roadmap.add_logo(
        "images/logo/matariki-tech-logo.png", position="top-right", width=50, height=50
    )

    group = roadmap.add_group("Core Product Work Stream")

    task = group.add_task("Base Functionality", "2023-01-01", "2023-10-31")
    task.add_milestone("v.1.0", "2023-02-15")
    task.add_milestone("v.1.1", "2023-08-01")

    parellel_task = task.add_parallel_task("Enhancements", "2023-11-15", "2024-03-31")
    parellel_task.add_milestone("v.2.0", "2024-03-30")

    task = group.add_task("Showcase #1", "2023-03-01", "2023-05-07")
    task.add_parallel_task("Showcase #2", "2023-06-01", "2023-08-07")

    roadmap.set_footer("Generated by Roadmapper")
    roadmap.draw()
    roadmap.save("images/demo01.png")


### Wiki Images
def home_roadmap():
    my_roadmap = Roadmap(width=500, height=400)
    my_roadmap.set_title("My Roadmap")
    my_roadmap.set_timeline(
        mode=TimelineMode.MONTHLY, start="2022-11-14", number_of_items=6
    )

    group = my_roadmap.add_group("Development")
    group.add_task("Activity 1", "2022-12-01", "2023-02-10")
    group.add_task("Activity 2", "2023-01-11", "2023-03-20")
    group.add_task("Activity 3", "2023-01-21", "2023-06-30")

    my_roadmap.set_footer("Generated by Roadmapper")
    my_roadmap.draw()
    my_roadmap.save("images/my_roadmap.png")


def color01(filename: str, colour_theme: str):
    roadmap = Roadmap(600, 500, colour_theme=colour_theme, show_marker=True)
    roadmap.set_title("My Demo Roadmap")
    roadmap.set_timeline(TimelineMode.QUARTERLY, "2023-01-01", 4)
    roadmap.set_footer("Generated by Roadmapper")

    group = roadmap.add_group("Workstream 1")
    task = group.add_task("Task 1-A", "2023-01-01", "2023-04-30")
    task.add_parallel_task("Task 2-B", "2023-05-15", "2023-08-30")
    group.add_task("Task 3-C", "2023-04-01", "2023-06-30")

    group = roadmap.add_group("Workstream 2")
    group.add_task("Task 2-A", "2023-04-01", "2023-06-30")
    group.add_task("Task 2-B", "2023-05-01", "2023-07-30")
    group.add_task("Task 2-C", "2023-06-01", "2023-08-30")

    roadmap.draw()
    roadmap.save(filename)


def banner_roadmap():
    color01("images/color-theme01.png", "DEFAULT")
    color01("images/color-theme02.png", "GREYWOOF")
    color01("images/color-theme03.png", "ORANGEPEEL")
    color01("images/color-theme04.png", "BLUEMOUNTAIN")
    color01("images/color-theme05.png", "GREENTURTLE")


if __name__ == "__main__":
    readme_roadmap()
    home_roadmap()
    banner_roadmap()
