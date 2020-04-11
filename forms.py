from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField, FieldList, SelectField
from wtforms.validators import DataRequired, Length, Email, Required



class Sample(FlaskForm):
    name = StringField()
    flist = FieldList(TextField())
    submit = SubmitField('Submit')
    myChoices = [(1,"hello"),(2, "hello again"),(3, "goodbye")]
    myField = SelectField('Treatment', choices = myChoices, validators = [Required()])
