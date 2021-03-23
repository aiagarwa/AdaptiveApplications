class User:
    def __init__(self, name='John', age=25):

        self.name = name
        self.age = age

        self.set_default_values()


    def set_default_values(self):
        self.spiceness = 5

        self.cuisines = ["indian", "italian"]

        self.allegies = ["dairy"]

        self.level_of_activity = 5
