from datetime import datetime
from extension import db
import pdb

class UserHistory(db.Model):

    historyId = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(80))
    recipeId = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    mood = db.Column(db.String(80))
    weather = db.Column(db.String(80))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, username, user_id, recipe_id, rating, mood, weather):
        self.username = username
        self.user_id = user_id
        self.recipeId = recipe_id
        self.rating = rating
        self.mood = mood
        self.weather = weather

