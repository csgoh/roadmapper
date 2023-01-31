from datetime import datetime
from roadmapper.roadmap import Roadmap
from roadmapper.timelinemode import TimelineMode
from roadmapper.group import Group
from roadmapper.task import Task
import inspect


def colour_theme_demo(
    mode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2022-12-01",
    number_of_items: int = 12,
    show_generic_dates: bool = False,
    file_name: str = "demo01.png",
    colour_theme: str = "DEFAULT",
    locale_name: str = "en_US",
) -> None:
    file_name = "T_" + file_name
    roadmap = Roadmap(
        1200, 1000, auto_height=True, colour_theme=colour_theme, show_marker=True
    )
    roadmap.set_title("SAMPLE ROADMAP 2022/2023")
    roadmap.set_subtitle("ABC Corporation")
    roadmap.set_timeline(
        mode,
        start_date,
        number_of_items,
        show_generic_dates=show_generic_dates,
        timeline_locale=locale_name,
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


def chinese_theme_demo(
    mode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2022-12-01",
    number_of_items: int = 12,
    show_generic_dates: bool = False,
    show_first_day_of_week=False,
    file_name: str = "demo01.png",
    colour_theme: str = "DEFAULT",
    locale_name: str = "en_US",
) -> None:
    file_name = "T_" + file_name
    roadmap = Roadmap(
        1200, 1000, auto_height=True, colour_theme=colour_theme, show_marker=True
    )
    roadmap.set_title("示例路線圖 2022/2023")
    roadmap.set_subtitle("甲乙丙有限公司")
    roadmap.set_timeline(
        mode,
        start_date,
        number_of_items,
        show_generic_dates=show_generic_dates,
        timeline_locale=locale_name,
        show_first_day_of_week=show_first_day_of_week,
    )

    group = roadmap.add_group("核心產品工作流程", text_alignment="left")
    task = group.add_task("基本功能", "2022-11-01", "2023-10-31")
    task.add_milestone("版本 1.0", "2023-02-15")
    task.add_milestone("版本 1.1", "2023-08-01")
    parellel_task = task.add_parallel_task("增強功能", "2023-11-15", "2024-03-31")
    parellel_task.add_milestone("版本 2.0", "2024-01-30")

    task = group.add_task("陳列 #1", "2023-03-01", "2023-05-07")
    task.add_parallel_task("陳列 #2", "2023-06-01", "2023-08-07")

    group = roadmap.add_group("移動工作流程", text_alignment="left")
    group.add_task("移動應用程序開發", "2023-02-01", "2024-12-07")

    roadmap.set_footer("更新於 " + datetime.now().strftime("%Y-%m-%d"))
    roadmap.draw()

    roadmap.save(file_name)


def japanese_theme_demo(
    mode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2022-12-01",
    number_of_items: int = 12,
    show_generic_dates: bool = False,
    show_first_day_of_week=False,
    file_name: str = "demo01.png",
    colour_theme: str = "DEFAULT",
    locale_name: str = "en_US",
) -> None:
    file_name = "T_" + file_name
    roadmap = Roadmap(
        1200, 1000, auto_height=True, colour_theme=colour_theme, show_marker=True
    )
    roadmap.set_title("ロードマップの例 2022/2023")
    roadmap.set_subtitle("株式会社エー・ビー・シー")
    roadmap.set_timeline(
        mode,
        start_date,
        number_of_items,
        show_generic_dates=show_generic_dates,
        timeline_locale=locale_name,
        show_first_day_of_week=show_first_day_of_week,
    )

    group = roadmap.add_group("コア製品のワークフロー", text_alignment="left")
    task = group.add_task("基本的なスキル", "2022-11-01", "2023-10-31")
    task.add_milestone("バージョン 1.0", "2023-02-15")
    task.add_milestone("バージョン 1.1", "2023-08-01")
    parellel_task = task.add_parallel_task("強化", "2023-11-15", "2024-03-31")
    parellel_task.add_milestone("バージョン 2.0", "2024-01-30")

    task = group.add_task("ショーケース #1", "2023-03-01", "2023-05-07")
    task.add_parallel_task("ショーケース #2", "2023-06-01", "2023-08-07")

    group = roadmap.add_group("モバイル ワークフロー", text_alignment="left")
    group.add_task("モバイルアプリ開発", "2023-02-01", "2024-12-07")

    roadmap.set_footer("更新日 " + datetime.now().strftime("%Y-%m-%d"))
    roadmap.draw()

    roadmap.save(file_name)


def generic_date_test(
    mode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2022-11-01",
    number_of_items: int = 24,
    show_generic_dates: bool = False,
    show_first_day_of_week: bool = False,
    file_name: str = "demo01.png",
    colour_theme: str = "DEFAULT",
) -> None:
    file_name = "T_" + file_name
    roadmap = Roadmap(4400, 2000, colour_theme=colour_theme, show_marker=True)
    roadmap.set_title("My Demo Roadmap!!!")
    roadmap.set_timeline(
        mode,
        start_date,
        number_of_items,
        show_generic_dates=show_generic_dates,
        show_first_day_of_week=show_first_day_of_week,
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


def parallel_task_demo(
    mode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2022-12-01",
    number_of_items: int = 14,
    file_name: str = "demo01.png",
    colour_theme: str = "DEFAULT",
) -> None:
    file_name = "T_" + file_name
    roadmap = Roadmap(
        1200,
        612,
        auto_height=False,
        colour_theme=colour_theme,
        show_marker=True,
    )
    roadmap.set_title("ROADMAP EXAMPLE 2022/2023")
    roadmap.set_subtitle("This is a subtitle")
    roadmap.set_timeline(
        mode,
        start_date,
        number_of_items,
        show_generic_dates=False,
    )

    group = roadmap.add_group("Core Product Work Stream")

    task = group.add_task("Base Functionality", "2022-11-01", "2023-01-31")
    parellel_task = task.add_parallel_task("Enhancements", "2023-02-15", "2024-03-31")
    parellel_task.add_milestone("v.2.0", "2023-04-30")

    task = group.add_task("Showcase #1", "2023-01-01", "2023-01-31")
    parellel_task = task.add_parallel_task("Showcase #2", "2023-02-02", "2023-03-15")
    parellel_task.add_milestone("v.2.0", "2023-04-15")

    # group = roadmap.add_group("Core Product Work Stream 2")
    # task = group.add_task("Base Functionality", "2022-11-01", "2023-01-31")

    roadmap.set_footer("Author: CS Goh " + datetime.now().strftime("%Y-%m-%d"))
    roadmap.draw()
    roadmap.save(file_name)


def singleton_demo(
    mode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2023-01-01",
    number_of_items: int = 2,
    file_name: str = "demo01.png",
    colour_theme: str = "BLUEMOUNTAIN",
) -> None:
    file_name = "T_" + file_name
    roadmap = Roadmap(
        600,
        612,
        auto_height=True,
        colour_theme=colour_theme,
        show_marker=False,
    )
    roadmap.set_title("ROADMAP EXAMPLE")
    # roadmap.set_subtitle("This is a subtitle")
    roadmap.set_timeline(
        mode,
        start_date,
        number_of_items,
        show_generic_dates=False,
    )

    group = roadmap.add_group("Showcase Task Styles")

    task = group.add_task("Rectangle Style", "2023-01-15", "2023-02-15")
    task = group.add_task("Rounded Style", "2023-01-15", "2023-02-15", style="rounded")
    task = group.add_task(
        "Arrowhead Style", "2023-01-15", "2023-02-15", style="arrowhead"
    )

    # roadmap.set_footer("Author: CS Goh " + datetime.now().strftime("%Y-%m-%d"))
    roadmap.draw()
    roadmap.save(file_name)


def logo_demo(
    mode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2023-01-01",
    number_of_items: int = 2,
    file_name: str = "demo01.png",
    colour_theme: str = "BLUEMOUNTAIN",
    auto_height: bool = True,
    logo_position: str = "top-left",
) -> None:
    file_name = "T_" + file_name
    roadmap = Roadmap(
        800,
        612,
        auto_height=auto_height,
        colour_theme=colour_theme,
        show_marker=False,
    )
    frameinfo = inspect.getframeinfo(inspect.currentframe())
    title = f"{frameinfo.function}(), theme={colour_theme}, mode={mode}"

    roadmap.add_logo("images/logo/matariki-tech-logo.png", logo_position, 50, 50)
    roadmap.set_title(title)
    roadmap.set_subtitle("This is a subtitle")
    roadmap.set_timeline(
        mode,
        start_date,
        number_of_items,
        show_generic_dates=False,
    )

    group = roadmap.add_group("Showcase Task Styles")

    text = "I love Python"
    # emojized_text = emojize(text)
    task = group.add_task(text, "2023-01-15", "2023-02-15")

    roadmap.set_footer("Author: CS Goh " + datetime.now().strftime("%Y-%m-%d"))
    roadmap.draw()
    roadmap.save(file_name)


# # demo01(file_name="demo01.png")
# # demo01(TimelineMode.WEEKLY, "2023-02-01", 16, "demo02.png")
# # demo01(TimelineMode.QUARTERLY, "2023-02-01", 4, "demo03.png")
# # demo01(TimelineMode.HALF_YEARLY, "2023-02-01", 3, "demo04.png")
# # demo01(TimelineMode.YEARLY, "2023-02-01", 2, "demo05.png")

# # demo02_barestyle(file_name="demo01.png")
# # demo02_barestyle(TimelineMode.WEEKLY, "2023-02-01", 16, "demo02.png")
# # demo02_barestyle(TimelineMode.QUARTERLY, "2023-02-01", 4, "demo03.png")
# # demo02_barestyle(TimelineMode.HALF_YEARLY, "2023-02-01", 3, "demo04.png")
# # demo02_barestyle(TimelineMode.YEARLY, "2023-02-01", 2, "demo05.png")

# colour_theme_demo(file_name="demo-colour-default.png", colour_theme="DEFAULT")
# colour_theme_demo(file_name="demo-colour-GREYWOOF.png", colour_theme="GREYWOOF")
# colour_theme_demo(file_name="demo-colour-BLUEMOUNTAIN.png", colour_theme="BLUEMOUNTAIN")
# colour_theme_demo(file_name="demo-colour-ORANGEPEEL.png", colour_theme="ORANGEPEEL")
# colour_theme_demo(file_name="demo-colour-GREENTURTLE.png", colour_theme="GREENTURTLE")

show_generic_dates = False

### Problematic test case - To check
# colour_theme_demo(
#     file_name="demo-colour-GREENTURTLE-weekly.png",
#     colour_theme="GREENTURTLE",
#     mode=TimelineMode.WEEKLY,
#     number_of_items=53,
#     show_generic_dates=show_generic_dates,
# )

# colour_theme_demo(
#     file_name="demo-colour-GREENTURTLE-monthly-gen.png",
#     colour_theme="GREENTURTLE",
#     mode=TimelineMode.MONTHLY,
#     number_of_items=14,
#     show_generic_dates=show_generic_dates,
# )

# colour_theme_demo(
#     file_name="demo-colour-GREYWOOF-monthly-gen.png",
#     colour_theme="GREYWOOF",
#     mode=TimelineMode.MONTHLY,
#     number_of_items=14,
#     show_generic_dates=show_generic_dates,
# )

# colour_theme_demo(
#     file_name="demo-colour-ORANGEPEEL-monthly-gen.png",
#     colour_theme="ORANGEPEEL",
#     mode=TimelineMode.MONTHLY,
#     number_of_items=14,
#     show_generic_dates=show_generic_dates,
# )

# colour_theme_demo(
#     file_name="demo-colour-BLUEMOUNTAIN-monthly-gen.png",
#     colour_theme="BLUEMOUNTAIN",
#     mode=TimelineMode.MONTHLY,
#     number_of_items=14,
#     show_generic_dates=show_generic_dates,
# )

# show_generic_dates = False
# colour_theme_demo(
#     file_name="demo-colour-GREENTURTLE-monthly.png",
#     colour_theme="GREENTURTLE",
#     mode=TimelineMode.MONTHLY,
#     number_of_items=14,
#     show_generic_dates=show_generic_dates,
# )
# show_generic_dates = True
# colour_theme_demo(
#     file_name="demo-colour-GREENTURTLE-quarter.png",
#     colour_theme="GREENTURTLE",
#     mode=TimelineMode.QUARTERLY,
#     number_of_items=6,
#     show_generic_dates=show_generic_dates,
# )

# colour_theme_demo(
#     file_name="demo-colour-GREENTURTLE-halfyearly.png",
#     colour_theme="GREENTURTLE",
#     mode=TimelineMode.HALF_YEARLY,
#     number_of_items=6,
#     show_generic_dates=show_generic_dates,
# )

# colour_theme_demo(
#     file_name="demo-colour-GREENTURTLE-yearly.png",
#     colour_theme="GREENTURTLE",
#     mode=TimelineMode.YEARLY,
#     number_of_items=4,
#     show_generic_dates=show_generic_dates,
# )


# generic_date_test(
#     file_name="demo-weekly-1.png",
#     mode=TimelineMode.WEEKLY,
#     start_date="2022-11-01",
#     number_of_items=56,
#     show_generic_dates=True,
#     show_first_day_of_week=True,
# )

# generic_date_test(
#     file_name="demo-weekly-2.png",
#     mode=TimelineMode.WEEKLY,
#     start_date="2022-11-01",
#     number_of_items=70,
#     show_generic_dates=False,
#     show_first_day_of_week=True,
# )


# generic_date_test(
#     file_name="demo-weekly-3.png",
#     mode=TimelineMode.WEEKLY,
#     number_of_items=52,
#     start_date="2023-01-01",
#     show_generic_dates=False,
#     show_first_day_of_week=True,
# )


# generic_date_test(
#     file_name="demo-weekly-4.png",
#     mode=TimelineMode.WEEKLY,
#     number_of_items=56,
#     start_date="2023-01-01",
#     show_generic_dates=False,
#     show_first_day_of_week=True,
# )

# generic_date_test(
#     file_name="demo-weekly-5.png",
#     mode=TimelineMode.WEEKLY,
#     start_date="2022-11-01",
#     number_of_items=63,
#     show_generic_dates=False,
# )

# generic_date_test(
#     file_name="demo-weekly-6.png",
#     mode=TimelineMode.WEEKLY,
#     number_of_items=12,
#     start_date="2023-01-01",
#     show_generic_dates=False,
# )


# generic_date_test(
#     file_name="demo-monthly.png",
#     mode=TimelineMode.MONTHLY,
#     start_date="2022-11-01",
#     number_of_items=55,
#     show_generic_dates=show_generic_dates,
# )

# generic_date_test(
#     file_name="demo-quarterly.png",
#     mode=TimelineMode.QUARTERLY,
#     start_date="2022-11-01",
#     number_of_items=55,
#     show_generic_dates=show_generic_dates,
# )

# generic_date_test(
#     file_name="demo-half-yearly.png",
#     mode=TimelineMode.HALF_YEARLY,
#     start_date="2022-11-01",
#     number_of_items=12,
#     show_generic_dates=show_generic_dates,
# )

# generic_date_test(
#     file_name="demo-yearly.png",
#     mode=TimelineMode.YEARLY,
#     start_date="2022-11-01",
#     number_of_items=12,
#     show_generic_dates=show_generic_dates,
# )


# parallel_task_demo(file_name="parallel-demo01.png")
# singleton_demo(file_name="singleton-demo01.png")
# logo_demo(file_name="logo_demo_top-left.png", logo_position="top-left")
# logo_demo(file_name="logo_demo_top-centre.png", logo_position="top-centre")
# logo_demo(file_name="logo_demo_top_right.png", logo_position="top-right")
# logo_demo(file_name="logo_demo_bottom_left.png", logo_position="bottom-left")
# logo_demo(
#     file_name="logo_demo_bottom_centre.png",
#     logo_position="bottom-centre",
# )
# logo_demo(file_name="logo_demo_bottom_right.png", logo_position="bottom-right")

# logo_demo(
#     file_name="Flogo_demo_top-left.png", logo_position="top-left", auto_height=False
# )
# logo_demo(
#     file_name="Flogo_demo_top-centre.png", logo_position="top-centre", auto_height=False
# )
# logo_demo(
#     file_name="Flogo_demo_top_right.png", logo_position="top-right", auto_height=False
# )
# logo_demo(
#     file_name="Flogo_demo_bottom_left.png",
#     logo_position="bottom-left",
#     auto_height=False,
# )
# logo_demo(
#     file_name="Flogo_demo_bottom_centre.png",
#     logo_position="bottom-centre",
#     auto_height=False,
# )
# logo_demo(
#     file_name="Flogo_demo_bottom_right.png",
#     logo_position="bottom-right",
#     auto_height=False,
# ),


colour_theme_demo(
    file_name="demo-my-colour-rainbow.png",
    colour_theme="rainbow.json",
    mode=TimelineMode.MONTHLY,
    number_of_items=14,
)

# colour_theme_demo(
#     file_name="demo-my-colour-chocolate.png",
#     colour_theme="chocolate.json",
#     mode=TimelineMode.MONTHLY,
#     number_of_items=14,
# )

# colour_theme_demo(
#     file_name="demo-my-colour-orangepeel.png",
#     colour_theme="ORANGEPEEL",
#     mode=TimelineMode.MONTHLY,
#     number_of_items=14,
# )

# colour_theme_demo(
#     file_name="demo-my-colour-orangepeel-generic.png",
#     colour_theme="ORANGEPEEL",
#     mode=TimelineMode.MONTHLY,
#     number_of_items=14,
#     show_generic_dates=True,
# )

# chinese_theme_demo(
#     file_name="demo-my-colour-chinese.png",
#     colour_theme="chinese.json",
#     mode=TimelineMode.WEEKLY,
#     start_date="2023-01-01",
#     number_of_items=14,
#     locale_name="zh_TW_timeline_settings.json",
#     show_generic_dates=False,
#     show_first_day_of_week=True,
# )

# japanese_theme_demo(
#     file_name="demo-my-colour-japanese.png",
#     colour_theme="chinese.json",
#     mode=TimelineMode.MONTHLY,
#     start_date="2023-01-01",
#     number_of_items=14,
#     locale_name="ja_JP_timeline_settings.json",
#     show_generic_dates=False,
#     show_first_day_of_week=True,
# )
