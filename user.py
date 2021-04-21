from extension import db
import pdb

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(80), unique=True)
    # password = db.Column(db.String(80))
    preferences = db.Column(db.PickleType)

    def __init__(self, username, password):
        self.userName = username
        self.password = password

        self.preferences = Preferences()


class Preferences():
    def __init__(self):

        self.cuisines = []
        self.allergies = []
        self.vegetarian = False

        self.level_of_activity = None

        # self.health_goals = []


    def update(self, data):
        for key in list(data.keys()):
            if key in ['csrf_token', 'submit']:
                continue

            if not hasattr(self, key):
                print("Key [%s] did not exist for class prior" % key)

            setattr(self, key, data[key])
