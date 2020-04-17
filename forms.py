from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields.html5 import DateField
from wtforms import StringField, IntegerField, TextField, SubmitField, validators, FieldList, SelectField, FormField, FloatField
from wtforms.validators import DataRequired, Length, Email, Required
from wtforms import Form as NoCsrfForm
import datetime
import wtforms_json
from database_io import getTreatments2019

wtforms_json.init()

class Treatment(FlaskForm):
    filtered_result = getTreatments2019()
    treatments = SelectField(u'Treatments',  coerce=int)
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.datetime.today().date())
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(Treatment, self).__init__(*args, **kwargs)
        self.treatments.choices =[(0, "Select treatment")] + [(i['item'], i['description']) for i in self.filtered_result] 

class Patient(FlaskForm): 
    medicalAid = [("psemas","PSEMAS"),("mva", "MVA"),("other", "OTHER")]
    medical = SelectField('Medical Aid', choices = medicalAid, validators = [Required()])
    name = StringField(u'Full Name', validators=[DataRequired()])
    case = StringField(u'Case Number', validators=[DataRequired()])
    po = IntegerField(u'PO', validators=[DataRequired()])
    date =  DateField(u'Invoice Date', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.datetime.today().date())
    submit = SubmitField('Continue')
