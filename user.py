from extension import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(80), unique=True)
    # password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.userName = username
        self.password = password

        # self.set_default_values()


    def set_default_values(self):
        self.spiceness = 5

        self.cuisines = ["indian", "italian"]

        self.allergies = ["dairy"]

        self.level_of_activity = 5

        self.health_goals = ["eat_less_fat"]

        self.max_number_of_ingredients = 10
