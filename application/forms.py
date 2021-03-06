from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, IntegerField, TextField, SubmitField, validators, FieldList, FormField, FloatField, DateField, DecimalField, TextAreaField
from wtforms.fields.html5 import DecimalField
from wtforms_components.fields import SelectField
from wtforms.validators import DataRequired, Length, Email, Required, NumberRange, ValidationError, Regexp
from wtforms.widgets.html5 import NumberInput
from wtforms.widgets import TextArea, CheckboxInput
from wtforms import Form as NoCsrfForm
from application.db_tariffs import getTreatments, getTariffs

def getTreatmentForm(tariff = None):
    class Treatment(FlaskForm):
        if ('namaf_physio' in tariff):
            treatments = SelectField(u'Treatments',coerce=int,
                    validators=[DataRequired()])
            date = TextField('Date', validators=[DataRequired()])
            description = TextField()
            units = DecimalField(u'Units')
            value = DecimalField(u'Value')
            post_value = DecimalField(u'Value')
            modifier = SelectField(u'Modifier', choices= 
                    [(0, 'None'),(6, '006 - Emergency treatment'),
                        (8, '008 - More than one procedure'), 
                        (9,'009 - Multpile conditions'),
                        (10, '010 - Treatment time overlap'),
                        (13, '013 - Travelling cost'),
                        (14,'014 - Rendered hospital')], default=0)
            date_invoice = TextField('Invoice date', validators=[DataRequired()])
            submit = SubmitField('Submit')
        else:
            treatments = TextField('Treatment')
            description = TextField('Description')
            units = DecimalField(u'Units')
            date = TextField('Date', validators=[DataRequired()])
            modifier = DecimalField(u'modifier')
            value = DecimalField(u'Value')
            post_value = DecimalField(u'Value')
            date_invoice =  TextField('Invoice date', validators=[DataRequired()])
            submit = SubmitField('Submit')

        def initialise_SelectOption(self,list_ordered_by_category = None, featured_ordered_by_category = None,  *args, **kwargs):
            super(Treatment, self).__init__(*args, **kwargs)
            if ('namaf_physio' in tariff):
                self.treatments.choices = featured_ordered_by_category + list_ordered_by_category

        def nestedObjects(self, filtered_result, featured_result):
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
            if('namaf_physio' in tariff):
                featured = [501, 303, 314, 703, 702, 401, 405, 317, 503, 107, 901]
                filtered_result = getTreatments(tariff)
                featured_result = getTreatments(tariff, featured)
                list_ordered_by_category, featured_ordered_by_category = self.nestedObjects(filtered_result, featured_result)
                self.initialise_SelectOption(list_ordered_by_category = list_ordered_by_category, featured_ordered_by_category = featured_ordered_by_category)
            else:
                self.initialise_SelectOption()
    return Treatment()


class UserForm(FlaskForm):
    first_name =  StringField('First name', validators=[DataRequired(Length(min=4,
                                                                     max=35))])
    second_name =  StringField('Second name', validators=[DataRequired(Length(min=4,
                                                                     max=35))])
    email = StringField('Email', validators=[DataRequired(),Email(message='Enter a valid email.')])
    submit = SubmitField('Update Personal Data')

class PracticeForm(FlaskForm):
    practice_email = StringField('Practice Email')
    phone = StringField('Landline number')
    cell =  StringField('Cell number', validators=[DataRequired()])
    fax = StringField('Fax number')
    pob = StringField('PO Box', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    bank = StringField('Bank', validators=[DataRequired()])
    bank_branch = StringField('Branch number',
                              validators=[DataRequired()])
    bank_account = StringField('Account number', validators=[DataRequired()])
    bank_holder =  StringField('Account holder', validators=[DataRequired()])
    practice_number = StringField('Practice number', validators=[DataRequired()])
    practice_name = StringField('Practice name', validators=[DataRequired()])
    hpcna_number = StringField('HPCNA number', validators=[DataRequired()])
    qualification = StringField('Qualification', validators=[DataRequired()])
    specialisation = StringField('Specialisation')

    submit = SubmitField('Update Practice Data')


class InvoiceForm(FlaskForm):
    phone =  BooleanField('Landline')
    fax = BooleanField('Fax')
    hospital = BooleanField('Hospital & Admission Information')
    diagnosis = BooleanField('Diagnosis & Procedure')
    submit = SubmitField('Update Invoice Layout')

def mva_patient_form(namaf_profession):

    class Patient_mva(FlaskForm):
        medical_aid = StringField('Medical Aid')
        tariffs = getTariffs(namaf_profession)
        choices = []
        for x in tariffs:
            _tariff = x['tariff']
            tariff_ = _tariff.replace('_', ' ')
            _tariff_ = tariff_.upper()
            choices.append((_tariff, _tariff_))
        choices.append(('', 'Choose Tariff'))
        patient_name = StringField(u'Full Name', validators=[DataRequired()])
        case_number = StringField(u'Case Number', validators=[DataRequired()])
        po_number = IntegerField(u'PO', validators=[DataRequired()]) #widget=NumberInput(min=111111,max=999999))
        tariff = SelectField(u'Tariff', choices = choices,
            validators=[DataRequired()], default='')
        date_created =  StringField(u'Invoice created', validators=[DataRequired()])
        hospital_name = StringField('Hospital')
        admission_date = StringField('Date of admission')
        discharge_date = StringField('Date of discharge')
        diagnosis = StringField('Diagnosis')
        diagnosis_date = StringField('Date of diagnosis')
        procedure = StringField('Procedure')
        procedure_date = StringField('Date of procedure')
        implants = StringField('Implants')
        intra_op = SelectField('Intra-OP imaging', choices = [('',
        'Select Intra-OP'),('yes','Yes'),('no','No')], default='')
        post_op =  StringField('Post-OP imaging')
        status = TextField('Status')
        submit = SubmitField('Create invoice')
    return Patient_mva()


def other_patient_form(namaf_profession):
    class Patient_other(FlaskForm):
        medical_aid = StringField('Medical Aid',validators = [DataRequired(),
            Regexp('^\w+$', message="Please delete all white spaces before & after the word")])
        patient_name = StringField(u'Full Name', validators=[DataRequired()])
        main_member = StringField(u'Main Member', validators=[DataRequired()])
        medical_number = IntegerField(u'Medical Aid No:', validators=[DataRequired()])
        patient_birth_date = StringField(u'Date of Birth', validators=[DataRequired()])
        date_created =  StringField(u'Invoice created', validators=[DataRequired()])
        tariffs = getTariffs(namaf_profession)
        choices = []
        for x in tariffs:
            _tariff = x['tariff']
            tariff_ = _tariff.replace('_', ' ')
            _tariff_ = tariff_.upper()
            choices.append((_tariff, _tariff_))
        choices.append(('', 'Choose Tariff'))
        tariff = SelectField(u'Tariff', choices = choices,
                         validators=[DataRequired()] , default='')
        hospital_name = StringField('Hospital')
        admission_date = StringField('Date of admission')
        discharge_date = StringField('Date of discharge')
        diagnosis = StringField('Diagnosis')
        diagnosis_date = StringField('Date of diagnosis')
        procedure = StringField('Procedure')
        procedure_date = StringField('Date of procedure')
        implants = StringField('Implants')
        intra_op = SelectField('Intra-OP imaging',
            choices = [('', 'Select Intra-op'),('yes','Yes'),
                ('no','No')], default='')
        post_op =  StringField('Post-OP imaging')
        status = TextField('Status')
        submit = SubmitField('Create invoice')
    return Patient_other()
