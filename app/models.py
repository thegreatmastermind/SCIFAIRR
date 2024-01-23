from .extensions import db
from flask_login import UserMixin

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    tags = db.Column(db.String(255))
    note = db.Column(db.String(10000))
    mood = db.Column(db.Integer)
    moodTags = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    entries = db.relationship('Entry')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    event_icon = db.Column(db.String(255))
    event_notes = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))