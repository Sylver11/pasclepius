from flask_wtf import FlaskForm, RecaptchaField
#from wtforms.fields.html5 import DateField
from wtforms import StringField, IntegerField, TextField, SubmitField, validators, FieldList, SelectField, FormField, FloatField, DateField
from wtforms.validators import DataRequired, Length, Email, Required
from wtforms import Form as NoCsrfForm
import datetime
import wtforms_json
from database_io import getTreatments

wtforms_json.init()
def getFormByYear(tariff):
    class Treatment(FlaskForm):
        filtered_result = getTreatments(tariff)
        treatments = SelectField(u'Treatments',  coerce=int)
        date = TextField('Date', validators=[DataRequired()])
        price = TextField(u'Value')
        submit = SubmitField('Submit')
        def __init__(self, *args, **kwargs):
            super(Treatment, self).__init__(*args, **kwargs)
            self.treatments.choices =[(0, "Select treatment")] + [(i['item'], i['description']) for i in self.filtered_result] 
    return Treatment()



class Patient_mva(FlaskForm): 
    medical = StringField('Medical Aid')
    name = StringField(u'Full Name', validators=[DataRequired()])
    case = StringField(u'Case Number', validators=[DataRequired()])
    po = IntegerField(u'PO', validators=[DataRequired()])
    tariff = SelectField(u'Tariff', choices = [("namaf_pyhsio_2014","Namaf Physio 2014"),("namaf_physio_2019", "Namaf Physio 2019"),("namaf_physio_2020", "Namaf Physio 2020")])
    date =  StringField(u'Invoice Date', validators=[DataRequired()])# default=datetime.datetime.today().date())
    submit = SubmitField('Continue')


class Patient_psemas(FlaskForm): 
    medical = StringField('Medical Aid')
    name = StringField(u'Full Name', validators=[DataRequired()])
    main = StringField(u'Main Member', validators=[DataRequired()])
    number = IntegerField(u'Medical Aid No:', validators=[DataRequired()])
    dob = StringField(u'Date of Birth', validators=[DataRequired()])
    tariff = SelectField(u'Tariff', choices = [("namaf_pyhsio_2014","Namaf Physio 2014"),("namaf_physio_2019", "Namaf Physio 2019"),("namaf_physio_2020", "Namaf Physio 2020")])
    date =  StringField(u'Invoice Date', validators=[DataRequired()])# default=datetime.datetime.today().date())
    submit = SubmitField('Continue')

class Patient_other(FlaskForm): 
    medical = StringField('Medical Aid', validators=[DataRequired()])
    name = StringField(u'Full Name', validators=[DataRequired()])
    main = StringField(u'Main Member', validators=[DataRequired()])
    number = IntegerField(u'Medical Aid No:', validators=[DataRequired()])
    dob = StringField(u'Date of Birth', validators=[DataRequired()])
    tariff = SelectField(u'Tariff', choices = [("namaf_pyhsio_2014","Namaf Physio 2014"),("namaf_physio_2019", "Namaf Physio 2019"),("namaf_physio_2020", "Namaf Physio 2020")])
    date =  StringField(u'Invoice Date', validators=[DataRequired()])# default=datetime.datetime.today().date())
    submit = SubmitField('Continue')
