from flask_sqlalchemy import SQLAlchemy
from datetime import time

db = SQLAlchemy()

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    date = db.Column(db.String(10))  # Format: YYYY-MM-DD
    time_slot = db.Column(db.String(5))  # Format: HH:MM