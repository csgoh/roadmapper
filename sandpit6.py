
class A:
    
    def add_element(self, element):
        self.elements = []
        self.elements.append(element)
        print (f"memory address of self.elements is {id(self.elements)}")
        return self.elements
    
    def print_elements(self):
        print(self.elements)
        

a = A()
elements = a.add_element(1)
print (f"memory address of elements is {id(elements)}")
elements.append(2)

a.print_elements()