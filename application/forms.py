from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextField, SubmitField, validators, FieldList, FormField, FloatField, DateField, DecimalField
from wtforms.fields.html5 import DecimalField
from wtforms_components.fields import SelectField
from wtforms.validators import DataRequired, Length, Email, Required, NumberRange
from wtforms.widgets.html5 import NumberInput
from wtforms import Form as NoCsrfForm
from application.database_io import getTreatments

def getTreatmentForm(tariff = None):
    class Treatment(FlaskForm):
        treatments = SelectField(u'Treatments',coerce=int, validators=[DataRequired()] )
        date = TextField('Date', validators=[DataRequired()])
        price = DecimalField(u'Value')
        modifier = SelectField(u'Modifier', choices= [(0, 'None'), (14,'Rendered hospital'),(13, 'Travelling cost')], default=0)
        submit = SubmitField('Submit')
        def initialise_SelectOption(self,list_ordered_by_category = None, featured_ordered_by_category = None,  *args, **kwargs):
            super(Treatment, self).__init__(*args, **kwargs)
            self.treatments.choices = featured_ordered_by_category + list_ordered_by_category

        def nestedObjects(something, filtered_result, featured_result):
            list_of_categories = []
            list_ordered_by_category = []
            featured_ordered_by_category = []
            for i in filtered_result:
                list_of_categories.append(i['category'])
            seen = {}
            dupes = []
            for x in list_of_categories:
                if x not in seen:
                    seen[x] = 1
            else:
                if seen[x] == 1:
                    dupes.append(x)
                seen[x] += 1
            for keys, values in seen.items():
                a = (keys, )
                b = []
                for x in filtered_result:
                    if x['category'] == keys:
                        b.append((x['item'],x['description']))
                c = a + (tuple(b,),)
                list_ordered_by_category.append(c)
            for i in featured_result:
                featured_ordered_by_category.append((i['item'],i['description']))
            featured_ordered_by_category  = [('Featured',) + (tuple(featured_ordered_by_category,),)]
            return list_ordered_by_category, featured_ordered_by_category

        def __init__(self, *args, **kwargs):
            if(tariff is not None):
                featured = [501, 303, 314, 703, 702, 401, 405, 317, 503, 107, 901]
                filtered_result = getTreatments(tariff)
                featured_result = getTreatments(tariff, featured)
                list_ordered_by_category, featured_ordered_by_category = self.nestedObjects(filtered_result, featured_result)
                self.initialise_SelectOption(list_ordered_by_category = list_ordered_by_category, featured_ordered_by_category = featured_ordered_by_category)
    return Treatment()


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(),
                                             Email(message='Enter a valid email.')])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    def validate_username(self, username):
        #user = User.query.filter_by(username=username.data).first()
        user = None
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        #user = User.query.filter_by(email=email.data).first()
        user = None
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    """User Login Form."""
    email = StringField('Email', validators=[DataRequired(),
                                             Email(message='Enter a valid email.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class Patient_mva(FlaskForm):
    medical = StringField('Medical Aid')
    name = StringField(u'Full Name', validators=[DataRequired()])
    case = StringField(u'Case Number', validators=[DataRequired()])
    po = IntegerField(u'PO', widget=NumberInput(min=111111,max=999999))
    tariff = SelectField(u'Tariff', choices = [("namaf_physio_2014","Namaf Physio 2014"),("namaf_physio_2019", "Namaf Physio 2019"),("namaf_physio_2020", "Namaf Physio 2020")])
    date =  StringField(u'Invoice Date', validators=[DataRequired()])
    submit = SubmitField('Continue')


class Patient_psemas(FlaskForm):
    medical = StringField('Medical Aid')
    name = StringField(u'Full Name', validators=[DataRequired()])
    main = StringField(u'Main Member', validators=[DataRequired()])
    number = IntegerField(u'Medical Aid No:', validators=[DataRequired()])
    dob = StringField(u'Date of Birth', validators=[DataRequired()])
    tariff = SelectField(u'Tariff', choices = [("namaf_physio_2014","Namaf Physio 2014"),("namaf_physio_2019", "Namaf Physio 2019"),("namaf_physio_2020", "Namaf Physio 2020")])
    date =  StringField(u'Invoice Date', validators=[DataRequired()])
    submit = SubmitField('Continue')

class Patient_other(FlaskForm):
    medical = StringField('Medical Aid', validators=[DataRequired()])
    name = StringField(u'Full Name', validators=[DataRequired()])
    main = StringField(u'Main Member', validators=[DataRequired()])
    number = IntegerField(u'Medical Aid No:', validators=[DataRequired()])
    dob = StringField(u'Date of Birth', validators=[DataRequired()])
    tariff = SelectField(u'Tariff', choices = [("namaf_physio_2014","Namaf Physio 2014"),("namaf_physio_2019", "Namaf Physio 2019"),("namaf_physio_2020", "Namaf Physio 2020")])
    date =  StringField(u'Invoice Date', validators=[DataRequired()])
    submit = SubmitField('Continue')
