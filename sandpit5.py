from contextlib import contextmanager

class Parent:
   
    @contextmanager
    def do_something(self):
        try:
            print(type(self).__name__, id(self), "I'm doing something")
            yield Child()
        finally:
            print(type(self).__name__, id(self),"I'm done!")
            
class Child:
    @contextmanager
    def do_something(self):
        try:
            print(type(self).__name__, id(self), "    I'm doing something")
            yield GrandChild()
        finally:
            print(type(self).__name__, id(self), "    I'm done!")

    
class GrandChild:
    @contextmanager
    def do_something(self):
        print(type(self).__name__, id(self), "        I'm doing something")
        print(type(self).__name__, id(self), "        I'm done!")


my_parent = Parent()

with my_parent.do_something() as my_child:
    with my_child.do_something() as my_grandchild:
        my_grandchild.do_something()
        my_grandchild.do_something()
    with my_child.do_something() as my_grandchild:
        my_grandchild.do_something()
        my_grandchild.do_something()
        
print ("*********")
with my_parent.do_something() as my_child:
    with my_child.do_something() as my_grandchild:
        my_grandchild.do_something()
        my_grandchild.do_something()
    with my_child.do_something() as my_grandchild:
        my_grandchild.do_something()
        my_grandchild.do_something()