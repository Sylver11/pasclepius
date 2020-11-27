from flask_login import UserMixin
from datetime import datetime
from application import db
from dataclasses import dataclass


@dataclass
class Calendar(db.Model):
    id:int
    practice_uuid:str
    patient_uuid:str
    title:str
    description:str
    start:datetime
    end:datetime
    color:str
    text_color:str
    created_on:datetime
    updated_on:datetime
    __tablename__ = 'pa_calendar'
    id = db.Column(db.Integer(), primary_key=True)
    practice_uuid = db.Column(db.String(36), nullable=False)
    patient_uuid = db.Column(db.String(36), nullable=True)
    title = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    color = db.Column(db.String(255), nullable=True)
    text_color = db.Column(db.String(255), nullable=True)
    created_on = db.Column(db.DateTime(),default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(),default=datetime.utcnow,onupdate=datetime.utcnow)



class User(UserMixin):
    def __init__(self, id, first_name='', uuid='', practice_uuid='',
            practice_name='', practice_id='', practice_admin='', invoice_layout = '', namaf_profession = '', practice_role='', practice_folder_id='', active=True):
        self.uuid = uuid
        self.first_name = first_name
        self.practice_uuid = practice_uuid
        self.practice_name = practice_name
        self.practice_id = practice_id
        self.practice_admin = practice_admin
        self.invoice_layout = invoice_layout
        self.namaf_profession = namaf_profession
        self.practice_role = practice_role
        self.id = id
        self.practice_folder_id = practice_folder_id
        self.active = active
    pass

