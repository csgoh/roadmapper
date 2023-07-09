import os
from datetime import datetime
from roadmapper.roadmap import Roadmap
from roadmapper.timelinemode import TimelineMode


def colour_theme_demo_without_locale(
    timelinemode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2022-12-01",
    number_of_items: int = 12,
    show_generic_dates: bool = False,
    file_name: str = "demo01.png",
    colour_theme: str = "DEFAULT",
) -> None:
    roadmap = Roadmap(
        1200,
        1000,
        auto_height=True,
        colour_theme=colour_theme,
        show_marker=True,
        painter_type="SVG",
    )
    roadmap.set_background_colour("lightblue")
    roadmap.add_logo("images/logo/matariki-tech-logo.png", "top-left", 50, 50)
    roadmap.set_title("SAMPLE ROADMAP 2022/2023")
    roadmap.set_subtitle("ABC Corporation")
    roadmap.set_timeline(
        timelinemode,
        start=start_date,
        number_of_items=number_of_items,
        show_generic_dates=show_generic_dates,
    )

    group = roadmap.add_group("Core Product Work Stream", text_alignment="left")
    task = group.add_task("Base Functionality", "2022-11-01", "2023-10-31")
    task.add_milestone("v.1.0", "2023-02-15")
    task.add_milestone("v.1.1", "2023-08-01")
    parellel_task = task.add_parallel_task("Enhancements", "2023-11-15", "2024-03-31")
    parellel_task.add_milestone("v.2.0", "2024-03-30")

    task = group.add_task("Showcase #1", "2023-03-01", "2023-05-07")
    task.add_parallel_task("Showcase #2", "2023-06-01", "2023-08-07")

    group = roadmap.add_group("Mobility Work Stream", text_alignment="left")
    group.add_task("Mobile App Development", "2023-02-01", "2024-12-07")

    roadmap.set_footer("Updated on " + datetime.now().strftime("%Y-%m-%d"))
    roadmap.draw()

    roadmap.save(file_name)


if __name__ == "__main__":
    output_file = "images/test/colour_theme_demo_without_locale.svg"
    colour_theme_demo_without_locale(
        file_name=output_file,
        timelinemode=TimelineMode.MONTHLY,
        number_of_items=14,
    )
