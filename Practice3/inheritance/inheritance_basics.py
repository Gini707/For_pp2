class Person:
    def greet(self):
        print("Hello, I am a person")

class Student(Person):
    pass

p = Person()
s = Student()

p.greet()  
s.greet()   
