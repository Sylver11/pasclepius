from flask_login import UserMixin
from datetime import datetime
from application import db
from dataclasses import dataclass
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case
from sqlalchemy.ext.declarative import DeclarativeMeta
import simplejson as json

@dataclass
class Calendar(db.Model):
    id:int
    practice_uuid:str
    patient_id:str
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
    patient_id = db.Column(db.String(255), nullable=True)
    title = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    color = db.Column(db.String(255), nullable=True)
    text_color = db.Column(db.String(255), nullable=True)
    created_on = db.Column(db.DateTime(),default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(),default=datetime.utcnow,onupdate=datetime.utcnow)


@dataclass
class Patient(db.Model):
    practice_uuid:str
    patient_id:str
    patient_name:str
    medical_aid:str
    main_member:str
    patient_birth_date:datetime
    medical_number:str
    case_number:str
    patient_note:str
    created_on:datetime
    #updated_on:datetime
    __tablename__ = 'patients'
    id = db.Column(db.Integer(), primary_key=True)
    practice_uuid = db.Column(db.String(36), nullable=False)
    patient_name = db.Column(db.String(255), nullable=False)
    medical_aid = db.Column(db.String(255), nullable=False)
    main_member = db.Column(db.String(255), nullable=True)
    patient_birth_date = db.Column(db.Date(), nullable=True)
    medical_number = db.Column(db.String(255), nullable=True)
    case_number = db.Column(db.String(255), nullable=True)
    patient_note = db.Column(db.Text, nullable=True)
    created_on = db.Column(db.DateTime(),default=datetime.utcnow)
    #updated_on = db.Column(db.DateTime(),default=datetime.utcnow,onupdate=datetime.utcnow)

    @hybrid_property
    def patient_id(self):
        if self.medical_number is not None:
            return self.medical_number
        else:
            return self.case_number
    @patient_id.expression
    def patient_id(cls):
        return case([(cls.case_number != None,
            cls.case_number),], else_ = cls.medical_number)


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


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)
