#from application import db
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#db = SQLAlchemy()

class Calendar(db.Model):
    __tablename__ = 'pa_calendar'
    id = db.Column(db.Integer(), primary_key=True)
    practice_uuid = db.Column(db.String(36), nullable=False)
    title = db.Column(db.Text(), nullable=False)
    start_event = db.Column(db.String(255), nullable=False)
    end_event = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255), nullable=True)
    text_color = db.Column(db.String(255), nullable=True)
    created_on = db.Column(db.DateTime(),default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(),default=datetime.utcnow,onupdate=datetime.utcnow)


