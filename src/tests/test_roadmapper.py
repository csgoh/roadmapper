import os
from datetime import datetime

from src.roadmapper.roadmap import Roadmap
from src.roadmapper.timelinemode import TimelineMode
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


def colour_theme_demo_without_locale(
    timelinemode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2022-12-01",
    number_of_items: int = 12,
    show_generic_dates: bool = False,
    file_name: str = "demo01.png",
    colour_theme: str = "DEFAULT",
) -> None:
    roadmap = Roadmap(
        1200, 1000, auto_height=True, colour_theme=colour_theme, show_marker=True
    )
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


def chinese_theme_demo(
    timelinemode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2022-12-01",
    number_of_items: int = 12,
    show_generic_dates: bool = False,
    show_first_day_of_week=False,
    file_name: str = "demo01.png",
    colour_theme: str = "DEFAULT",
    locale_name: str = "en_US",
) -> None:
    roadmap = Roadmap(
        1200, 1000, auto_height=True, colour_theme=colour_theme, show_marker=True
    )
    roadmap.set_title("示例路線圖 2022/2023")
    roadmap.set_subtitle("甲乙丙有限公司")
    roadmap.set_timeline(
        timelinemode,
        start=start_date,
        number_of_items=number_of_items,
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
    timelinemode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2022-12-01",
    number_of_items: int = 12,
    show_generic_dates: bool = False,
    show_first_day_of_week=False,
    file_name: str = "demo01.png",
    colour_theme: str = "DEFAULT",
    locale_name: str = "en_US",
) -> None:
    roadmap = Roadmap(
        1200, 1000, auto_height=True, colour_theme=colour_theme, show_marker=True
    )
    roadmap.set_title("ロードマップの例 2022/2023")
    roadmap.set_subtitle("株式会社エー・ビー・シー")
    roadmap.set_timeline(
        timelinemode,
        start=start_date,
        number_of_items=number_of_items,
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
    timelinemode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2022-11-01",
    number_of_items: int = 24,
    show_generic_dates: bool = False,
    show_first_day_of_week: bool = False,
    file_name: str = "demo01.png",
    colour_theme: str = "DEFAULT",
) -> None:
    roadmap = Roadmap(4400, 2000, colour_theme=colour_theme, show_marker=True)
    roadmap.set_title("My Demo Roadmap!!!")
    roadmap.set_timeline(
        timelinemode,
        start=start_date,
        number_of_items=number_of_items,
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
    timelinemode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2022-12-01",
    number_of_items: int = 14,
    file_name: str = "demo01.png",
    colour_theme: str = "DEFAULT",
) -> None:
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
        timelinemode,
        start=start_date,
        number_of_items=number_of_items,
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
    timelinemode: TimelineMode = TimelineMode.MONTHLY,
    start_date: str = "2023-01-01",
    number_of_items: int = 2,
    file_name: str = "demo01.png",
    colour_theme: str = "BLUEMOUNTAIN",
) -> None:

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
        timelinemode,
        start=start_date,
        number_of_items=number_of_items,
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
    timelinemode: TimelineMode = TimelineMode.MONTHLY,
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
    title = f"{frameinfo.function}(), theme={colour_theme}, mode={timelinemode}"

    roadmap.add_logo("../../images/logo/matariki-tech-logo.png", logo_position, 50, 50)
    roadmap.set_title(title)
    roadmap.set_subtitle("This is a subtitle")
    roadmap.set_timeline(
        timelinemode,
        start=start_date,
        number_of_items=number_of_items,
        show_generic_dates=False,
    )

    group = roadmap.add_group("Showcase Task Styles")

    text = "I love Python"
    # emojized_text = emojize(text)
    task = group.add_task(text, "2023-01-15", "2023-02-15")

    roadmap.set_footer("Author: CS Goh " + datetime.now().strftime("%Y-%m-%d"))
    roadmap.draw()
    roadmap.save(file_name)


def test_dev():
    if not os.path.exists("images"):
        os.mkdir("images")

    if not os.path.exists("../../images/test"):
        os.mkdir("../../images/test")

    output_file = "../../images/test/colour_theme_demo_without_locale.png"
    # if file exist, then delete it first
    if os.path.exists(output_file):
        os.remove(output_file)

    colour_theme_demo_without_locale(
        file_name=output_file,
        timelinemode=TimelineMode.MONTHLY,
        number_of_items=14,
    )

    assert os.path.exists(output_file)

    output_file = "../../images/test/demo-my-colour-chinese.png"
    chinese_theme_demo(
        file_name=output_file,
        colour_theme="../json/chinese.json",
        timelinemode=TimelineMode.WEEKLY,
        start_date="2023-01-01",
        number_of_items=14,
        locale_name="../json/zh_TW_timeline_settings.json",
        show_generic_dates=False,
        show_first_day_of_week=True,
    )
    assert os.path.exists(output_file)

    output_file = "../../images/test/demo-my-colour-japanese.png"
    japanese_theme_demo(
        file_name=output_file,
        colour_theme="../json/chinese.json",
        timelinemode=TimelineMode.MONTHLY,
        start_date="2023-01-01",
        number_of_items=14,
        locale_name="../json/ja_JP_timeline_settings.json",
        show_generic_dates=False,
        show_first_day_of_week=True,
    )

    assert os.path.exists(output_file)



# check if calling from main
if __name__ == "__main__":
    output_file = "../../images/test/colour_theme_demo_without_locale.png"
    colour_theme_demo_without_locale(
        file_name=output_file,
        timelinemode=TimelineMode.MONTHLY,
        number_of_items=14,
    )