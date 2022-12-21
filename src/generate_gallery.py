from datetime import datetime
from roadmapper.roadmap import Roadmap
from roadmapper.timelinemode import TimelineMode

# import unittest


def sample_roadmap(
    width: int = 1200,
    mode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2022-12-01",
    number_of_items: int = 12,
    show_generic_dates: bool = False,
    file_name: str = "demo01.png",
    colour_theme: str = "DEFAULT",
) -> None:
    roadmap = Roadmap(
        width, 1000, auto_height=True, colour_theme=colour_theme, show_marker=False
    )
    roadmap.set_title("STRATEGY ROADMAP 2023")
    roadmap.set_subtitle("Matariki Technologies Inc.")
    roadmap.set_timeline(
        mode,
        start_date,
        number_of_items,
        show_generic_dates=show_generic_dates,
        fill_colour="#404040",
        font_colour="white",
    )

    group = roadmap.add_group("Planning", fill_colour="#FFC000", font_colour="black")
    task = group.add_task(
        "Vision", "2023-01-01", "2023-03-31", fill_colour="#FFC000", font_colour="black"
    )
    task = group.add_task(
        "Goals", "2023-02-15", "2023-03-31", fill_colour="#FFC000", font_colour="black"
    )
    task.add_parallel_task(
        "Strategic Intent",
        "2023-04-01",
        "2023-05-31",
        fill_colour="#FFC000",
        font_colour="black",
    )
    task.add_parallel_task(
        "Sales Budget",
        "2023-06-01",
        "2023-07-15",
        fill_colour="#FFC000",
        font_colour="black",
    )
    task.add_parallel_task(
        "Release Plans",
        "2023-07-16",
        "2023-09-30",
        fill_colour="#FFC000",
        font_colour="black",
    )

    group = roadmap.add_group("Strategy", fill_colour="#ED7D31", font_colour="black")
    task = group.add_task(
        "Market Analysis",
        "2023-02-01",
        "2023-03-30",
        fill_colour="#ED7D31",
        font_colour="black",
    )
    task.add_milestone(
        "Competitor Review", "2023-03-30", fill_colour="#843C0C", font_colour="black"
    )
    task.add_parallel_task(
        "SWOT", "2023-04-01", "2023-04-30", fill_colour="#ED7D31", font_colour="black"
    )
    task = group.add_task(
        "Business Model",
        "2023-04-01",
        "2023-05-31",
        fill_colour="#ED7D31",
        font_colour="black",
    )
    task.add_milestone(
        "Price List (Draft)", "2023-06-01", fill_colour="#843C0C", font_colour="black"
    )
    parallel_task = task.add_parallel_task(
        "Price Reseach",
        "2023-06-01",
        "2023-08-05",
        fill_colour="#ED7D31",
        font_colour="black",
    )
    parallel_task.add_milestone(
        "Price List (Final)", "2023-07-28", fill_colour="#843C0C", font_colour="black"
    )
    group.add_task(
        "Objectives",
        "2023-06-20",
        "2023-09-10",
        fill_colour="#ED7D31",
        font_colour="black",
    )

    group.add_task(
        "Sales Trends Analysis",
        "2023-08-15",
        "2023-10-10",
        fill_colour="#ED7D31",
        font_colour="black",
    )

    group = roadmap.add_group(
        "Service Development", fill_colour="#70AD47", font_colour="black"
    )
    task = group.add_task(
        "Product Roadmap",
        "2023-02-15",
        "2023-03-31",
        fill_colour="#70AD47",
        font_colour="black",
    )
    parallel_task = task.add_parallel_task(
        "Development",
        "2023-04-01",
        "2023-08-30",
        fill_colour="#70AD47",
        font_colour="black",
    )
    parallel_task.add_milestone(
        "Alpha May 20", "2023-05-20", fill_colour="#385723", font_colour="black"
    )
    parallel_task.add_milestone(
        "Private Beta Jul 02", "2023-07-02", fill_colour="#385723", font_colour="black"
    )
    parallel_task.add_milestone(
        "Public Beta Aug 15", "2023-08-15", fill_colour="#385723", font_colour="black"
    )

    parallel_task = task.add_parallel_task(
        "Release Candidate",
        "2023-09-01",
        "2023-10-15",
        fill_colour="#70AD47",
        font_colour="black",
    )

    parallel_task = task.add_parallel_task(
        "Release To Public",
        "2023-10-16",
        "2023-12-31",
        fill_colour="#70AD47",
        font_colour="black",
    )

    parallel_task.add_milestone(
        "Go Live Dec 20", "2023-12-20", fill_colour="#385723", font_colour="black"
    )

    group = roadmap.add_group(
        "Business Intelligence",
        fill_colour="#4472C4",
        font_colour="black",
    )
    task = group.add_task(
        "BI Development",
        "2023-04-15",
        "2023-12-31",
        fill_colour="#4472C4",
        font_colour="black",
    )

    task.add_milestone(
        "Service Dashboard", "2023-05-15", fill_colour="#162641", font_colour="black"
    )

    task.add_milestone(
        "Real-Time Analytics", "2023-08-01", fill_colour="#162641", font_colour="black"
    )

    task.add_milestone(
        "Sales Dashboard", "2023-12-15", fill_colour="#162641", font_colour="black"
    )

    roadmap.set_footer("Generated by Roadmapper")
    roadmap.draw()

    roadmap.save(file_name)


def colour_theme_roadmap(
    width: int = 1200,
    mode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2022-12-01",
    number_of_items: int = 12,
    show_generic_dates: bool = False,
    file_name: str = "demo01.png",
    colour_theme: str = "DEFAULT",
) -> None:
    roadmap = Roadmap(
        width, 1000, auto_height=True, colour_theme=colour_theme, show_marker=True
    )
    roadmap.set_title("SAMPLE ROADMAP 2022/2023")
    roadmap.set_subtitle("GodZone Corporation")
    roadmap.set_timeline(
        mode, start_date, number_of_items, show_generic_dates=show_generic_dates
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

    roadmap.set_footer("Generated by Roadmapper")
    roadmap.draw()

    roadmap.save(file_name)


def custom_colour_roadmap(
    width: int = 1200,
    height: int = 1000,
    mode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2022-11-01",
    number_of_items: int = 24,
    show_marker: bool = False,
    show_generic_dates: bool = False,
    file_name: str = "demo01.png",
    colour_theme: str = "DEFAULT",
) -> None:
    roadmap = Roadmap(
        width,
        height,
        auto_height=True,
        colour_theme=colour_theme,
        show_marker=show_marker,
    )
    roadmap.set_title("My Demo Roadmap!!!")
    roadmap.set_timeline(
        mode, start_date, number_of_items, show_generic_dates=show_generic_dates
    )

    group = roadmap.add_group("Core Product Work Stream")
    task = group.add_task("Base Functionality", "2022-11-01", "2023-10-31")
    task.add_milestone("v.1.0", "2023-02-15")
    task.add_milestone("v.1.1", "2023-08-01")
    parellel_task = task.add_parallel_task("Enhancements", "2023-11-15", "2024-03-31")
    parellel_task.add_milestone("v.2.0", "2024-03-30")

    task = group.add_task("Showcase #1", "2023-03-01", "2023-05-07")
    task.add_parallel_task("Showcase #2", "2023-06-01", "2023-08-07")

    group = roadmap.add_group("Mobility Work Stream")
    group.add_task("Mobile App Development", "2023-02-01", "2024-12-07")

    roadmap.set_footer("Generated by Roadmapper")
    roadmap.draw()
    roadmap.save(file_name)


### Sample Roadmap ###
sample_roadmap(
    width=1400,
    file_name="images/gallery/gallery-sample-01.png",
    mode=TimelineMode.MONTHLY,
    number_of_items=12,
    start_date="2023-01-01",
)

### Colour Theme Roadmap ###

colour_theme_roadmap(
    file_name="images/gallery/gallery-DEFAULT-monthly.png",
    # colour_theme="ORANGEPEEL",
    mode=TimelineMode.MONTHLY,
    number_of_items=12,
    start_date="2023-01-01",
)

colour_theme_roadmap(
    file_name="images/gallery/gallery-ORANGEPEEL-monthly.png",
    colour_theme="ORANGEPEEL",
    mode=TimelineMode.MONTHLY,
    number_of_items=12,
    start_date="2023-01-01",
)

colour_theme_roadmap(
    file_name="images/gallery/gallery-BLUEMOUNTAIN-monthly.png",
    colour_theme="BLUEMOUNTAIN",
    mode=TimelineMode.MONTHLY,
    number_of_items=12,
    start_date="2023-01-01",
)

colour_theme_roadmap(
    file_name="images/gallery/gallery-GREENTURTLE-monthly.png",
    colour_theme="GREENTURTLE",
    mode=TimelineMode.MONTHLY,
    number_of_items=12,
    start_date="2023-01-01",
)

colour_theme_roadmap(
    file_name="images/gallery/gallery-GREYWOOF-monthly.png",
    colour_theme="GREYWOOF",
    mode=TimelineMode.MONTHLY,
    number_of_items=12,
    start_date="2023-01-01",
)

### Marker Roadmap ###
custom_colour_roadmap(
    width=1200,
    file_name="images/gallery/gallery-marker-monthly.png",
    mode=TimelineMode.MONTHLY,
    number_of_items=12,
    start_date="2022-11-01",
    show_marker=True,
    show_generic_dates=False,
)

### WEEKLY Timeline Roadmap ###
colour_theme_roadmap(
    width=2400,
    file_name="images/gallery/gallery-DEFAULT-weekly.png",
    colour_theme="DEFAULT",
    mode=TimelineMode.WEEKLY,
    number_of_items=52,
    start_date="2023-01-01",
    show_generic_dates=False,
)

### QUARTERLY Timeline Roadmap ###
colour_theme_roadmap(
    width=1400,
    file_name="images/gallery/gallery-DEFAULT-quarterly.png",
    colour_theme="DEFAULT",
    mode=TimelineMode.QUARTERLY,
    number_of_items=6,
    start_date="2023-01-01",
    show_generic_dates=False,
)

### HALF-YEARLY Timeline Roadmap ###
colour_theme_roadmap(
    width=1400,
    file_name="images/gallery/gallery-DEFAULT-halfyearly.png",
    colour_theme="DEFAULT",
    mode=TimelineMode.HALF_YEARLY,
    number_of_items=4,
    start_date="2023-01-01",
    show_generic_dates=False,
)

### YEARLY Timeline Roadmap ###
colour_theme_roadmap(
    width=1400,
    file_name="images/gallery/gallery-DEFAULT-yearly.png",
    colour_theme="DEFAULT",
    mode=TimelineMode.YEARLY,
    number_of_items=2,
    start_date="2023-01-01",
    show_generic_dates=False,
)

### Generic Dates Roadmap ###
colour_theme_roadmap(
    width=1400,
    file_name="images/gallery/gallery-DEFAULT-generic-monthly.png",
    colour_theme="DEFAULT",
    mode=TimelineMode.MONTHLY,
    number_of_items=12,
    start_date="2023-01-01",
    show_generic_dates=True,
)
