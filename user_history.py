from datetime import datetime
from extension import db
import pdb

class UserHistory(db.Model):

    historyId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    recipeId = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    mood = db.Column(db.String(80))
    weather = db.Column(db.String(80))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, username, recipeId, rating, mood, weather):
        self.username = username
        self.recipeId = recipeId
        self.rating = rating
        self.mood = mood
        self.weather = weather

