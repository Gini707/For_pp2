class Father:
    def skill1(self):
        print("I can drive")


class Mother:
    def skill2(self):
        print("I can cook")


class Child(Father, Mother):
    pass


c = Child()
c.skill1()
c.skill2()
