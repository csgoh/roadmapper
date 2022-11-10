import uuid
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class Umbrella:

    def __init__(self) -> None:
        self.groups = []
        pass

    @contextmanager
    def add_group(self, group_text: str):
        try:
            group = Group(group_text)
            self.groups.append(group)
            #yield self.groups[len(self.groups) - 1]
            yield group
        finally:
            group = None


@dataclass
class Group:

    def __init__(self, group_text) -> None:
        self.uid = uuid.uuid4()
        self.text = group_text
        self.tasks = []

    @contextmanager
    def add_task(self, task_text: str):
        try:
            task = Task(task_text)
            self.tasks.append(task)

            #yield self.tasks[len(self.tasks) - 1]
            yield task
        finally:
            task = None


@dataclass
class Task:

    def __init__(self, text) -> None:
        self.uid = uuid.uuid4()
        self.text = text
        self.milestones = []

    def add_milestone(self, milestone_text: str):
        milestone = Milestone(milestone_text)
        self.milestones.append(milestone)



@dataclass
class Milestone:
    def __init__(self, text) -> None:
        self.uid = uuid.uuid4()
        self.text = text


my_umbrella = Umbrella()

with my_umbrella.add_group("Group 1") as group:
    with group.add_task("Task 1") as task1:
        task1.add_milestone("M1-1")
        task1.add_milestone("M2-2")
    with group.add_task("Task 2") as task2:
        task2.add_milestone("M2-1")
        task2.add_milestone("M2-2")
        
with my_umbrella.add_group("Group 2") as group2:
    with group2.add_task("Task 3") as task3:
        task3.add_milestone("M4-1")
        task3.add_milestone("M4-2")
        task3.add_milestone("M4-3")
        task3.add_milestone("M4-4")
        task3.add_milestone("M4-5")
        task3.add_milestone("M4-6")
        task3.add_milestone("M4-7")

#print(my_umbrella.groups[0].tasks[0].milestones[0].text)

def print_umbrella(umbrella: Umbrella):
    for group in umbrella.groups:
        print(group.text)
        for task in group.tasks:
            print(f"  {task.text}")
            for milestone in task.milestones:
                print(f"    {milestone.text}")            
# for group in my_umbrella.groups:
#     print (f"Group: {group.text}")
#     for task in group.tasks:
#         print (f"     Task: {task.text}")
#         for milestone in task.milestones:
#             print (f"          Milestone: {milestone.text}")

print_umbrella(my_umbrella)
            
