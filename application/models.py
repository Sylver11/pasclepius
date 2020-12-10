from flask_login import UserMixin
from datetime import datetime
import datetime as datetime2
from application import db
from dataclasses import dataclass
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy_utils import UUIDType
import uuid
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




@dataclass
class Invoice(db.Model):
    id:int
    practice_uuid:str
    patient_id:str
    medical_aid:str
    date_created:datetime
    date_invoice:datetime
    invoice_id:str
    invoice_file_url:str
    tariff:str
    po_number:int
    hospital_name:str
    admission_date:datetime
    discharge_date:datetime
    procedure:str
    procedure_date:str
    diagnosis:str
    diagnosis_date:datetime
    implants:str
    intra_op:str
    post_op:str
    submitted_on:datetime
    invoice_layout:int
    status:str
    credit_cent:int
    remind_me:datetime
    last_edited:datetime
    last_edited_by:str

    __tablename__ = 'invoices'
    id = db.Column(db.Integer(), primary_key=True)
    practice_uuid = db.Column(db.String(36), nullable=False)
    patient_id = db.Column(db.String(255), nullable=False)
    medical_aid = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(),default=datetime.utcnow)
    date_invoice = db.Column(db.Date(),nullable=False)
    invoice_id = db.Column(db.String(255),nullable=False)
    invoice_file_url = db.Column(db.String(255),nullable=False)
    tariff = db.Column(db.String(255),nullable=False)
    po_number = db.Column(db.Integer(), nullable=True)
    hospital_name = db.Column(db.String(255), nullable=True)
    admission_date = db.Column(db.Date(), nullable=True)
    discharge_date = db.Column(db.Date(), nullable=True)
    procedure = db.Column(db.Text(), nullable=True)
    procedure_date = db.Column(db.Date(), nullable=True)
    diagnosis = db.Column(db.Text(), nullable=True)
    diagnosis_date = db.Column(db.Date(), nullable=True)
    implants = db.Column(db.Text(), nullable=True)
    intra_op = db.Column(db.String(255), nullable=True)
    post_op = db.Column(db.String(255), nullable=True)
    submitted_on = db.Column(db.Date(),nullable=True)
    invoice_layout = db.Column(db.Integer(), nullable=True)
    status = db.Column(db.String(255), default="not-submitted")
    credit_cent = db.Column(db.Integer(), default=0)
    remind_me = db.Column(db.DateTime, nullable=True)
    last_edited = db.Column(db.DateTime(),default=datetime.utcnow,onupdate=datetime.utcnow)
    last_edited_by = db.Column(db.String(255), nullable=True)


@dataclass
class Practice(db.Model):
    id:int
#    practice_uuid:str
    practice_admin:str
    practice_name:str
    practice_number:str
    namaf_profession:str
    practice_email:str
    phone:str
    cell:str
    fax:str
    pob:str
    city:str
    country:str
    bank_holder:str
    bank_account:str
    bank:str
    bank_branch:str
    hpcna_number:str
    qualification:str
    specialisation:str
    practice_folder_id:str
    premium:bool
    invoice_layout:int
    created_on:datetime
    __tablename__ = 'practices'
    id = db.Column(db.Integer(), primary_key=True)
    uuid_bin = db.Column(UUIDType(binary=False))
    practice_admin = db.Column(db.String(255), nullable=False, unique=True)
    practice_name = db.Column(db.String(255), nullable=False)
    practice_number = db.Column(db.String(255), nullable=False)
    namaf_profession = db.Column(db.String(255), nullable=False)
    practice_email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=True)
    cell = db.Column(db.String(255), nullable=True)
    fax = db.Column(db.String(255), nullable=True)
    pob = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=True)
    bank_holder = db.Column(db.String(255), nullable=True)
    bank_account = db.Column(db.String(255), nullable=True)
    bank = db.Column(db.String(255), nullable=True)
    bank_branch = db.Column(db.String(255), nullable=True)
    hpcna_number = db.Column(db.String(255), nullable=True)
    qualification = db.Column(db.String(255), nullable=True)
    specialisation = db.Column(db.String(255), nullable=True)
    practice_folder_id = db.Column(db.Integer(), default=0)
    premium = db.Column(db.Boolean(), default=False)
    invoice_layout = db.Column(db.Integer(), default=1)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    @hybrid_property
    def practice_uuid(self):
        return self.bin_uuid

    @practice_uuid.expression
    def practice_uuid(cls):
        if not isinstance(cls.bin_uuid, uuid.UUID):
            return str(uuid.UUID(cls.bin_uuid))
        else:
            return str(cls.bin_uuid)

        #return case([(cls.case_number != None,
        #    cls.case_number),], else_ = cls.medical_number)


@dataclass
class Tariff(db.Model):
    id:int
    item:int
    description:str
    procedure:str
    units:int
    units_specification:str
    value_cent:int
    anaesthetic_units:int
    anaesthetic_value_cent:int
    category:str
    sub_category:str
    sub_sub_category:str
    sub_sub_sub_category:str
    note:str
    tariff:str
    __tablename__ = 'namaf_tariffs'
    id = db.Column(db.Integer(), primary_key=True)
    item = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    procedure = db.Column(db.String(), nullable=True)
    units = db.Column(db.Integer(), nullable=False)
    units_specification = db.Column(db.String(255), nullable=True)
    value_cent = db.Column(db.Integer(), nullable=True)
    anaesthetic_units = db.Column(db.Integer(), nullable=True)
    anaesthetic_value_cent = db.Column(db.Integer(), nullable=True)
    category = db.Column(db.String(255),nullable=True)
    sub_category = db.Column(db.String(255),nullable=True)
    sub_sub_category = db.Column(db.String(255),nullable=True)
    sub_sub_sub_category = db.Column(db.String(255),nullable=True)
    note = db.Column(db.Text(),nullable=True)
    tariff = db.Column(db.String(255),nullable=False)


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
                    if isinstance(data, datetime2.datetime):
                        d = datetime.strptime(data.__str__(), '%Y-%m-%d %H:%M:%S')
                        date = d.strftime('%d.%m.%Y')
                        data = date
                    elif isinstance(data, datetime2.date):
                        d = datetime.strptime(data.__str__(), '%Y-%m-%d')
                        date = d.strftime('%Y-%m-%d')
                        data = date
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)
