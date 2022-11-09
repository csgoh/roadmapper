import uuid
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class Umbrella:
    groups = []

    def __init__(self) -> None:
        pass

    def __enter__(self):
        print("Umbrella", "1 - Entering")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Umbrella", "2 - Exiting")

    @contextmanager
    def add_group(self, group_text: str):
        try:
            print("Umbrella", "3 - Adding group")
            found = False
            group = Group(group_text)
            for g in self.groups:
                if g == group:
                    found = True
                    break
            if not found:
                self.groups.append(group)
            print(group.__dict__)
            yield group
        finally:
            pass


@dataclass
class Group:
    tasks = []

    def __init__(self, group_text) -> None:
        self.uid = uuid.uuid4()
        self.text = group_text

    def __enter__(self):
        print(self.text, "1 - Entering")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.text, "2 - Exiting")

    def do_something(self):
        try:
            print(type(self).__name__, self.uid, "I'm doing something")
            yield Task()
        finally:
            print(type(self).__name__, self.uid, "I'm done!")

    @contextmanager
    def add_task(self, task_text: str):
        try:
            print(self.text, "3 - Adding task")
            found = False
            task = Task(task_text)
            for t in self.tasks:
                if t == task:
                    found = True
                    break
            if not found:
                self.tasks.append(task)

            yield task
        finally:
            pass


@dataclass
class Task:
    milestones = []

    def __init__(self, text) -> None:
        self.uid = uuid.uuid4()
        self.text = text

    def __enter__(self):
        print(self.text, "1 - Entering")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.text, "2 - Exiting")

    def do_something(self):
        try:
            print("     ", type(self).__name__, self.uid, "I'm doing something")
            yield Milestone()
        finally:
            print("     ", type(self).__name__, self.uid, "I'm done!")

    def add_milestone(self, milestone_text: str):
        try:
            print(self.text, "3 - Adding milestone")
            found = False
            milestone = Milestone(milestone_text)
            for m in self.milestones:
                if m == milestone:
                    found = True
                    break
            if not found:
                self.milestones.append(milestone)

            yield milestone
        finally:
            pass


@dataclass
class Milestone:
    def __init__(self, text) -> None:
        self.uid = uuid.uuid4()
        self.text = text


my_umbrella = Umbrella()

with my_umbrella.add_group("Group 1") as group:
    with group.add_task("Task 1") as task:
        task.add_milestone("M1-1")
        task.add_milestone("M2-2")
    with group.add_task("Task 2") as task:
        task.add_milestone("M2-1")
        task.add_milestone("M2-2")

print(group.__dict__)
