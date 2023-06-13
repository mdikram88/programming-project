from main import db
from flask_security import UserMixin
from sqlalchemy.orm import relationship


# Configure Tables
# Users
class Users(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    backup = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.CHAR(1), nullable=False)
    trackers = relationship("Trackers", back_populates="tracker_user")

    def __init__(self, email, password, name, age, backup, gender):
        self.email = email
        self.password = password
        self.name = name
        self.age = int(age)
        self.backup = backup
        self.gender = gender


# Trackers
class Trackers(db.Model, UserMixin):
    __tablename__ = "trackers"
    tracker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tracker_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    tracker_type = db.Column(db.String, nullable=False)
    setting = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    last_time = db.Column(db.String(255), nullable=False)
    tracker_user = relationship("Users", back_populates="trackers")
    logs = relationship("Logs", back_populates="tracker")

    def __init__(self, tracker_name, description, tracker_type, setting, user_id, last_time):
        self.tracker_name = tracker_name
        self.description = description
        self.tracker_type = tracker_type
        self.setting = setting
        self.user_id = user_id
        self.last_time = last_time


# Logs
class Logs(db.Model, UserMixin):
    __tablename__ = "logs"
    log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    note = db.Column(db.String)
    tracker_id = db.Column(db.Integer, db.ForeignKey("trackers.tracker_id"), nullable=False)
    tracker = relationship("Trackers", back_populates="logs")

    def __init__(self, time, value, note, tracker_id):
        self.time = time
        self.value = value
        self.note = note
        self.tracker_id = tracker_id


# db.create_all()
