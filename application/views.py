import os
from flask import current_app as app
from flask import render_template, Response, request, session, jsonify, redirect, url_for, send_file
from werkzeug.urls import url_parse
from application.forms import Patient_mva, Patient_psemas, Patient_other, getTreatmentForm, RegistrationForm, LoginForm
from application.database_io import getTreatmentByItem, getValueTreatments, getTreatmentByGroup
from application.database_invoice import get_index, add_invoice, getInvoiceURL, queryInvoice, getSingleInvoice, updateInvoice, liveSearch, getPatient
from application.url_generator import InvoicePath
from application.name_generator import InvoiceName
from application.models import User
from flask_login import current_user, login_user, UserMixin
from . import login_manager
from datetime import datetime
from jinja2 import Template
from decimal import *
import subprocess 
import simplejson as json


#class User(UserMixin):
#    pass


@login_manager.user_loader
def load_user(email):
    user = User()
    user.id = email
    return user

#    return User.get(user_id)
#    return User.query.get(user_id)

@app.route('/', methods=('GET', 'POST'))
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(user = form.username.data, email = form.email.data)
        #            form.password.data)
        #user = User(username=form.username.data, email=form.email.data)
        #user.id = form.email.data
        user.set_password(form.password.data)
        login_user(user)
        print(user)
       # db_session.add(user)
        #flash('Thanks for registering')
        return redirect(url_for('login'))
    print(form.errors.items())
    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
       # user = User.query.filter_by(username=form.username.data).first()
       # if user is None or not user.check_password(form.password.data):
           # flash('Invalid username or password')
       #     return redirect(url_for('login'))
        user = User()
        user.id = form.email.data
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', form=form)




@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/patient', methods=('GET', 'POST'))
def findPatient():
    form_mva = Patient_mva()
    form_psemas = Patient_psemas()
    form_other = Patient_other()
    return render_template('create.html',form_mva=form_mva, form_psemas = form_psemas, form_other = form_other)

@app.route('/patient/<patient>')
def invoiceOption(patient):
    form_mva = Patient_mva()
    form_psemas = Patient_psemas()
    form_other = Patient_other()
    data = queryInvoice(patient)
    patient_data = getPatient(patient)
    return  render_template('patient.html', patient_data=patient_data, data=data, patient=patient, form_mva=form_mva, form_psemas = form_psemas, form_other = form_other)


@app.route('/patient/<patient>/new-invoice')
def newInvoice(patient):
    medical = (session.get('PATIENT')["medical"])
    tariff = (session.get('PATIENT')["tariff"])
    date = session.get('PATIENT')['date']
    form = getTreatmentForm(tariff) 
    if (medical == 'mva'):
        po = session.get('PATIENT')['po']
        case = session.get('PATIENT')["case"]
        return render_template('invoice.html', dates=None, treatments=None, form=form, patient = patient, tariff = tariff, po = po, case = case, date = date, medical = medical)
    elif(medical == 'psemas'):
        number = session.get('PATIENT')['number']
        main = session.get('PATIENT')['main']
        dob = session.get('PATIENT')['dob']
        return render_template('invoice.html', dates=None, treatments=None,form=form, patient = patient, tariff = tariff, main = main, dob = dob, date = date, medical = medical, number = number)
    else:
        number = session.get('PATIENT')['number']
        main = session.get('PATIENT')['main']
        dob = session.get('PATIENT')['dob']
        return render_template('invoice.html', dates=None, treatments=None,form=form, patient = patient, tariff = tariff, main = main, dob = dob, date = date, medical = medical, number = number)



@app.route('/patient/<patient>/continue-invoice')
def continueInvoice(patient):
    medical = (session.get('PATIENT')["medical"])
    tariff = (session.get('PATIENT')["tariff"])
    date = session.get('PATIENT')['date']
    treatments = session.get('PATIENT')['treatments']
    dates = session.get('PATIENT')['dates']
    form = getTreatmentForm(tariff) 
    if (medical == 'mva'):
        po = session.get('PATIENT')['po']
        case = session.get('PATIENT')["case"]
        return render_template('invoice.html', dates=dates,treatments=treatments,form=form, patient = patient, tariff = tariff, po = po, case = case, date = date, medical = medical)
    elif(medical == 'psemas'):
        number = session.get('PATIENT')['number']
        main = session.get('PATIENT')['main']
        dob = session.get('PATIENT')['dob']
        return render_template('invoice.html',dates=dates,treatments=treatments,form=form, patient = patient, tariff = tariff, main = main, dob = dob, date = date, medical = medical, number = number)
    else:
        number = session.get('PATIENT')['number']
        main = session.get('PATIENT')['main']
        dob = session.get('PATIENT')['dob']
        return render_template('invoice.html', dates=dates,treatments=treatments,form=form, patient = patient, tariff = tariff, main = main, dob = dob, date = date, medical = medical, number = number)

@app.route('/patient/select', methods=('GET', 'POST'))
def selectPatient():
    form_mva = Patient_mva()
    form_psemas = Patient_psemas()
    form_other = Patient_other()
    if form_mva.validate_on_submit() or form_psemas.validate_on_submit() or form_other.validate_on_submit():
        session["PATIENT"] = request.values
        jsonData = jsonify(data={'name': str(form_mva.name.data)})
        return jsonData



@app.route('/generate-invoice', methods=['POST'])
def generateInvoice():
    dates = request.form.getlist('date')
    treatments = request.form.getlist('treatments')
    modifier = request.form.getlist('modifier')
    price = request.form.getlist('price')
    tariff = session.get('PATIENT')["tariff"]
    patient = session.get('PATIENT')
    medical = session.get('PATIENT')['medical']
    status = False
    url = ''
    invoice_name = ''
    form = getTreatmentForm(tariff)
    if form.treatments.data:
        treatment_list = getTreatmentByItem(treatments, tariff)
        if 'url' in session['PATIENT']:
            url = session.get('PATIENT')['url']
            invoice_name = session.get('PATIENT')['invoice']
            status = updateInvoice(treatments, dates, patient)
        else:
            date = session.get('PATIENT')['date']
            index = get_index(medical, date)
            url = InvoicePath(patient, index)
            url = url.generate()
            invoice_name = InvoiceName(patient, index, modifier)
            invoice_name = invoice_name.generate()
            status = add_invoice(patient, invoice_name, url, treatments, dates)
        if status:
            subprocess.call([os.getenv("LIBPYTHON"), os.getenv("APP_URL") +
                            '/application/swriter.py', json.dumps(treatments),
                            json.dumps(treatment_list), json.dumps(price),
                            json.dumps(dates), json.dumps(patient),
                            json.dumps(modifier), json.dumps(url),
                            json.dumps(invoice_name)])
            return jsonify(result='success')
        else:
            return jsonify(result='Error: Entry already exists')
    return jsonify(result='error')

@app.route('/live-search',methods=['GET','POST'])
def liveSearchPatient():
    name = request.args.get('username')
    data = liveSearch(name)
    value_json = json.dumps(data)
    return value_json

@app.route('/set-known-invoice',methods=['GET','POST'])
def knownInvoice():
    patient = request.args.get('patient')
    date = request.args.get('date')
    data =  getSingleInvoice(patient, date)
    d = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    date_deutsch = d.strftime('%d.%m.%Y')
    session["PATIENT"] = data
    session["PATIENT"]["date"]= date_deutsch
    return data


@app.route('/get-value',methods=['GET','POST'])
def getValue():
    tariff = session.get('PATIENT')["tariff"]
    item = request.args.get('item', 0, type=int)
    value = getValueTreatments(item, tariff)
    value_json = json.dumps({'value' : Decimal(value['value'])}, use_decimal=True)
    return value_json

@app.route('/get-treatment-name',methods=['GET','POST'])
def getTreatmentName():
    items = request.args.get('items')
    tariff = request.args.get('tariff')
    treatment_list = getTreatmentByGroup(items, tariff)
    value_json = json.dumps({'treatments':treatment_list})
    return value_json

@app.route('/download-invoice/<random>')
def downloadInvoice(random):
    name = session.get('PATIENT')['name']
    date = session.get('PATIENT')['date']
    url = getInvoiceURL(name, date)
    path = str(url['url']) + ".odt"
    return send_file(path, as_attachment=True)

@app.route('/session')
def sessionValues():
    return str(session.get('PATIENT'))
