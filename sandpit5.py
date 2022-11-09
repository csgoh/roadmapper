from contextlib import contextmanager
import uuid

class Group:
    tasks = []
    def __init__(self) -> None:
        self.uid = uuid.uuid4()
        
    @contextmanager
    def do_something(self):
        try:
            print(type(self).__name__, self.uid, "I'm doing something")
            yield Group()
        finally:
            print(type(self).__name__, self.uid,"I'm done!")
    def add_task(self, task):
        self.tasks.append(task)
    
            
class Task:
    milestones = []
    def __init__(self) -> None:
        self.uid = uuid.uuid4()
    
    @contextmanager
    def do_something(self):
        try:

            print("     ", type(self).__name__, self.uid, "I'm doing something")
            yield Task()
        finally:
            print("     ", type(self).__name__, self.uid, "I'm done!")
    
    def add_milestone(self, milestone):
        self.milestones.append(milestone)
    
class Milestone:
    def __init__(self) -> None:
        self.uid = uuid.uuid4()
        
    @contextmanager
    def do_something(self):
        
        print("             ", type(self).__name__, self.uid, "I'm doing something")
        print("             ", type(self).__name__, self.uid, "I'm done!")

my_group1 = Group()

with my_group1.do_something() as group:
    with group.do_something() as task:
        pass
    with group.do_something() as task:
        task.do_something()
        group.do_something()
    with group.do_something() as task:
        task.do_something()
        task.do_something()
print ("*********")
my_group2 = Group()
with my_group2.do_something() as group:
    with group.do_something() as task:
        task.do_something()
        task.do_something()
    with group.do_something() as task:
        task.do_something()
        task.do_something()