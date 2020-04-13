from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields.html5 import DateField
from wtforms import StringField, IntegerField, TextField, SubmitField, validators, FieldList, SelectField, FormField, FloatField
from wtforms.validators import DataRequired, Length, Email, Required
from wtforms import Form as NoCsrfForm
import datetime
import wtforms_json

wtforms_json.init()

class Treatment(FlaskForm):
    set = SelectField('Set', choices=[(314, 'Lymph drainage'),(305, 'Re-education of movement/ Exercises (excluding ante- and post-natal exercises)'),(131, 'Ante and post natal exercises/counselling'),])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.datetime.today().date())

   # qty = StringField('Quantity', validators=[DataRequired()])
   # db = [(1, 'C++'), (2, 'Python'), (3, 'Plain Text')]
    submit = SubmitField('Submit')

   # def __init__(self, *args, **kwargs):
    #    super(NewOrderForm, self).__init__(*args, **kwargs)
     #   self.set.choices =  [(set.id, set.name) for set in self.db]


class Patient(FlaskForm): 
    medicalAid = [("psemas","PSEMAS"),("mva", "MVA"),("other", "OTHER")]
    medical = SelectField('Medical Aid', choices = medicalAid, validators = [Required()])
    name = StringField(u'Full Name', validators=[DataRequired()])
    case = StringField(u'Case Number', validators=[DataRequired()])
    po = IntegerField(u'PO', validators=[DataRequired()])
    date =  DateField(u'Invoice Date', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.datetime.today().date())
    submit = SubmitField('Continue')
