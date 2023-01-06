from datetime import datetime
from roadmapper.roadmap import Roadmap
from roadmapper.timelinemode import TimelineMode

import unittest


def colour_theme_demo(
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
    roadmap.set_subtitle("Mars Software Inc.")
    roadmap.set_timeline(
        mode,
        start_date,
        number_of_items,
        show_generic_dates=show_generic_dates,
        year_fill_colour="#404040",
        item_fill_colour="#404040",
        year_font_colour="white",
        item_font_colour="white",
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
        "Private Beta Jun 30", "2023-06-30", fill_colour="#385723", font_colour="black"
    )
    parallel_task.add_milestone(
        "Public Beta Jun 30", "2023-08-10", fill_colour="#385723", font_colour="black"
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

    roadmap.set_footer(
        "Generated by Roadmapper on " + datetime.now().strftime("%Y-%m-%d")
    )
    roadmap.draw()

    roadmap.save(file_name)


def unicode_demo(
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
    roadmap.set_title("2023 年戰略路線圖")
    roadmap.set_subtitle("火星科技公司")
    roadmap.set_timeline(
        mode,
        start_date,
        number_of_items,
        show_generic_dates=show_generic_dates,
        year_fill_colour="#404040",
        item_fill_colour="#404040",
        year_font_colour="white",
        item_font_colour="white",
    )

    group = roadmap.add_group("規劃", fill_colour="#FFC000", font_colour="black")
    task = group.add_task(
        "願景", "2023-01-01", "2023-03-31", fill_colour="#FFC000", font_colour="black"
    )
    task = group.add_task(
        "目標", "2023-02-15", "2023-03-31", fill_colour="#FFC000", font_colour="black"
    )
    task.add_parallel_task(
        "戰略意圖",
        "2023-04-01",
        "2023-05-31",
        fill_colour="#FFC000",
        font_colour="black",
    )
    task.add_parallel_task(
        "銷售預算",
        "2023-06-01",
        "2023-07-15",
        fill_colour="#FFC000",
        font_colour="black",
    )
    task.add_parallel_task(
        "發布計劃",
        "2023-07-16",
        "2023-09-30",
        fill_colour="#FFC000",
        font_colour="black",
    )

    group = roadmap.add_group("戰略", fill_colour="#ED7D31", font_colour="black")
    task = group.add_task(
        "市場分析",
        "2023-02-01",
        "2023-03-30",
        fill_colour="#ED7D31",
        font_colour="black",
    )
    task.add_milestone(
        "競爭對手審查", "2023-03-30", fill_colour="#843C0C", font_colour="black"
    )
    task.add_parallel_task(
        "SWOT", "2023-04-01", "2023-04-30", fill_colour="#ED7D31", font_colour="black"
    )
    task = group.add_task(
        "商業模式",
        "2023-04-01",
        "2023-05-31",
        fill_colour="#ED7D31",
        font_colour="black",
    )
    task.add_milestone(
        "價目表（草稿）", "2023-06-01", fill_colour="#843C0C", font_colour="black"
    )
    parallel_task = task.add_parallel_task(
        "價格研究",
        "2023-06-01",
        "2023-08-05",
        fill_colour="#ED7D31",
        font_colour="black",
    )
    parallel_task.add_milestone(
        "價目表（最終）", "2023-07-28", fill_colour="#843C0C", font_colour="black"
    )
    group.add_task(
        "目標",
        "2023-06-20",
        "2023-09-10",
        fill_colour="#ED7D31",
        font_colour="black",
    )

    group.add_task(
        "銷售趨勢分析",
        "2023-08-15",
        "2023-10-10",
        fill_colour="#ED7D31",
        font_colour="black",
    )

    group = roadmap.add_group("服務發展", fill_colour="#70AD47", font_colour="black")
    task = group.add_task(
        "產品路線圖",
        "2023-02-15",
        "2023-03-31",
        fill_colour="#70AD47",
        font_colour="black",
    )
    parallel_task = task.add_parallel_task(
        "軟件開發",
        "2023-04-01",
        "2023-08-30",
        fill_colour="#70AD47",
        font_colour="black",
    )
    parallel_task.add_milestone(
        "阿尔法 5月20", "2023-05-20", fill_colour="#385723", font_colour="black"
    )
    parallel_task.add_milestone(
        "私人測試 6月30", "2023-06-30", fill_colour="#385723", font_colour="black"
    )
    parallel_task.add_milestone(
        "公開測試 8月30", "2023-08-10", fill_colour="#385723", font_colour="black"
    )

    parallel_task = task.add_parallel_task(
        "候选版本",
        "2023-09-01",
        "2023-10-15",
        fill_colour="#70AD47",
        font_colour="black",
    )

    parallel_task = task.add_parallel_task(
        "公開發布",
        "2023-10-16",
        "2023-12-31",
        fill_colour="#70AD47",
        font_colour="black",
    )

    parallel_task.add_milestone(
        "上綫 12月20", "2023-12-20", fill_colour="#385723", font_colour="black"
    )

    group = roadmap.add_group(
        "商業智能",
        fill_colour="#4472C4",
        font_colour="black",
    )
    task = group.add_task(
        "商業智能開發",
        "2023-04-15",
        "2023-12-31",
        fill_colour="#4472C4",
        font_colour="black",
    )

    task.add_milestone(
        "服務儀表板", "2023-05-15", fill_colour="#162641", font_colour="black"
    )

    task.add_milestone("實時分析", "2023-08-01", fill_colour="#162641", font_colour="black")

    task.add_milestone(
        "Sales Dashboard", "2023-12-15", fill_colour="#162641", font_colour="black"
    )

    roadmap.set_footer("由 Roadmapper 生成於 " + datetime.now().strftime("%Y-%m-%d"))
    roadmap.draw()

    roadmap.save(file_name)


def test_sample_case1():
    colour_theme_demo(
        width=2500,
        file_name="images/test/test-ORANGEPEEL-weekly.png",
        colour_theme="ORANGEPEEL",
        mode=TimelineMode.WEEKLY,
        number_of_items=52,
        start_date="2023-01-01",
    )
    assert True


def test_sample_case2():
    colour_theme_demo(
        file_name="images/test/test-ORANGEPEEL-monthly.png",
        colour_theme="ORANGEPEEL",
        mode=TimelineMode.MONTHLY,
        number_of_items=12,
        start_date="2023-01-01",
    )
    assert True


def test_sample_case3():
    colour_theme_demo(
        file_name="images/test/test-ORANGEPEEL-quarter.png",
        colour_theme="ORANGEPEEL",
        mode=TimelineMode.QUARTERLY,
        number_of_items=4,
        start_date="2023-01-01",
    )
    assert True


def test_sample_unicase1():
    unicode_demo(
        file_name="images/test/test-unicode-monthly.png",
        # colour_theme="ORANGEPEEL",
        mode=TimelineMode.MONTHLY,
        number_of_items=12,
        start_date="2023-01-01",
    )
    assert True
