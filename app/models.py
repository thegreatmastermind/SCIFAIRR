from .extensions import db
from flask_login import UserMixin
from datetime import datetime

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    tags = db.Column(db.String(255))
    note = db.Column(db.String(10000))
    mood = db.Column(db.Integer)
    moodTags = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    food_name = db.Column(db.String(255)) 
    food_description = db.Column(db.String(1000)) 
    sleep_start_time = db.Column(db.Time)  
    sleep_end_time = db.Column(db.Time)  

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    entries = db.relationship('Entry')
    last_login_date = db.Column(db.Date, default=datetime.now().date())
    login_streak = db.Column(db.Integer, default=0)
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    event_notes = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_icon = db.Column(db.String(255))

class SavedResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    link_or_thumbnail_url = db.Column(db.String(255))