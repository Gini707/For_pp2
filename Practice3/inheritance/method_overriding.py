class Person:
    def greet(self):
        print("Hello from Person")


class Student(Person):
    def greet(self):
        print("Hello from Student")


p = Person()
s = Student()

p.greet()   
s.greet()   
