from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields.html5 import DateField
from wtforms import StringField, TextField, SubmitField, FieldList, SelectField
from wtforms.validators import DataRequired, Length, Email, Required



class Sample(FlaskForm):
    name = StringField()
    date = DateField('Plan Start', validators=[Required()])
    flist = FieldList(TextField())
    submit = SubmitField('Submit')
    myChoices = [(1,"hello"),(2, "hello again"),(3, "goodbye")]
    myField = SelectField('Treatment', choices = myChoices, validators = [Required()])



def addTreatment(key):
    setattr(Sample, key, SelectField("Treatment", choices = myChoices, validators=[Required()]))
