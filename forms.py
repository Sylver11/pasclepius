from flask_wtf import FlaskForm, RecaptchaField
#from wtforms.fields.html5 import DateField
from wtforms import StringField, TextField, SubmitField, validators, FieldList, SelectField, FormField, FloatField, DateField 
from wtforms.validators import DataRequired, Length, Email, Required
from wtforms import Form as NoCsrfForm
import datetime
import wtforms_json



wtforms_json.init()



class MyForm(FlaskForm):
    standard = StringField('Expense_Item', validators=[DataRequired()])
    wps = StringField('Number')
 
#record = {'field1': 'label1', 'field2': 'label2'}

#for key, value in record.items():
#    setattr(MyForm, key, SelectField("Treatment", choices = value, validators=[Required()]))

class NewOrderForm(FlaskForm):
    #product = FieldList(StringField())
    set = SelectField('Set', coerce=int)
    qty = StringField('Quantity', validators=[DataRequired()])

    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(NewOrderForm, self).__init__(*args, **kwargs)
        self.set.choices = [(set.id, set.friendly_name) for set in Set.query.order_by(Set.friendly_name).all()]



class ExpenseItem(NoCsrfForm):
    expense_name = StringField('Expense_Item', validators=[DataRequired()])
    cost = FloatField('Cost', validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.datetime.today().date())
    type = SelectField('Role', choices=[('mutual', 'Mutual'),('personal#1', 'Personal #1'),('personal#2', 'Personal #2'),])


class ExpensesForm(FlaskForm):
    """A collection of expense items."""
    items = FieldList(FormField(ExpenseItem), min_entries=1)
    #for item in items:
     #   print(item.data['expense_name'], item.data['cost'])
    #print(items)

class Sample(FlaskForm):
    name = StringField()
    date = DateField('Plan Start', validators=[Required()])
    flist = FieldList(TextField())
    submit = SubmitField('Submit')
    myChoices = [(1,"hello"),(2, "hello again"),(3, "goodbye")]
    myField = SelectField('Treatment', choices = myChoices, validators = [Required()])



def addTreatment(response):
    a, b, c = [response[k] for k in ("a", "b", "c")]
    #mylist = {}
    #mylist[a] = b
    #print(mylist)
    myChoices = Sample()
    print(response)
    for key, value in response.items():
        setattr(Sample, key, StringField(value))


   # setattr(Sample, str(ke, SelectField("Treatment", choices = myChoices, validators=[Required()]))
