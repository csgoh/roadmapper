from typing import List


class Milestone:
    text: str
    date: str
    colour: str
    x: int
    y: int
    width: int
    height: int


class Task:
    text: str
    start_date: str
    end_date: str
    colour: str
    x: int
    y: int
    width: int
    height: int
    milestones: List[Milestone]


class Group:
    text: str
    colour: str
    x: int
    y: int
    width: int
    height: int
    tasks: List[Task]


class Title:
    text: str
    colour: str
    x: int
    y: int
    width: int
    height: int


class Timeline:
    text: str
    value: str
    colour: str
    x: int
    y: int
    width: int
    height: int


class Timelines:
    timeline_items: List[Timeline]


class Footer:
    text: str
    colour: str
    x: int
    y: int
    width: int
    height: int


class Roadmap:
    title: Title
    timelines: Timelines
    groups: List[Group]
    footer: Footer


my_roadmap = Roadmap()

foot = Footer()
foot.text = "My Footer"
foot.colour = "red"
my_roadmap.footer = foot

print(my_roadmap.footer.text)
