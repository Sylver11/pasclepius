import os
from flask import current_app as app
from flask import render_template, Response, request, session, jsonify, redirect, url_for, send_file, flash
from werkzeug.urls import url_parse
from application.forms import updateBankingForm, updatePracticeForm,Patient_mva, Patient_psemas, Patient_other,getTreatmentForm, RegistrationForm, LoginForm, updatePasswordForm, updatePersonalForm
from application.database_io import getTreatmentByItem, getValueTreatments, getMultipleValues, getTreatmentByGroup, liveSearchTreatments
from application.database_invoice import get_index, add_invoice, getInvoiceURL, queryInvoice, getSingleInvoice, updateInvoice, liveSearch, getPatient
from application.database_users import addUser, checkUser, updateUserPassword, updateUserPersonal, updateUserPractice, updateUserBanking
from application.url_generator import InvoicePath
from application.name_generator import InvoiceName
from application.models import User, Password
from flask_login import current_user, login_user, logout_user, UserMixin, login_required, fresh_login_required
from . import login_manager
from datetime import datetime
from jinja2 import Template
from decimal import *
import subprocess 
import simplejson as json


@login_manager.user_loader
def load_user(id):
    data = checkUser(id)
    if data:
        return User(id, data["first_name"], data["uuid_text"])


@app.route('/', methods=('GET', 'POST'))
def home():
    return render_template('index.html', title = 'PANAM - Medical Software')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.email.data, form.first_name.data)
        password = user.set_password(form.password.data)
        status = addUser(form.title.data, form.first_name.data,
                         form.second_name.data,
                         form.email.data, password,
                         form.phone.data, form.cell.data,
                         form.fax.data, form.pob.data,
                         form.city.data, form.country.data,
                         form.bank_holder.data, form.bank_account.data,
                         form.bank.data, form.bank_branch.data,
                         form.practice_number.data, form.practice_name.data,
                         form.hpcna_number.data, form.qualification.data,
                         form.specialisation.data)
        if status:
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        data = checkUser(form.email.data)
        user = User(form.email.data)
        if data is None or not user.check_password(data['password'], form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/fresh-login', methods=['GET', 'POST'])
def freshLogin():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        data = checkUser(form.email.data)
        user = User(form.email.data)
        if data is None or not user.check_password(data['password'], form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

####TODO: Reset data queries need to be fitted with MASTER_POS_WAIT######
@app.route('/profile/reset-password', methods=('GET', 'POST'))
@fresh_login_required
def resetPassword():
    form_password = updatePasswordForm()
    if request.method == 'POST' and form_password.validate():
        password = Password()
        hashed_password = password.set_password(form_password.password.data)
        status =  updateUserPassword(current_user.id, hashed_password)
        if status:
            flash('Password changed succesfully')
    return render_template('reset_password.html', form_password=form_password)

@app.route('/profile/reset-personal', methods=('GET', 'POST'))
def resetPersonal():
    data = checkUser(current_user.id)
    form_personal = updatePersonalForm()
    if request.method == 'POST' and form_personal.validate():
        status = updateUserPersonal(current_user.id, form_personal.first_name.data,
                form_personal.second_name.data, form_personal.cell.data,
                form_personal.pob.data, form_personal.city.data,
                form_personal.country.data, form_personal.qualification.data,
                form_personal.title.data, form_personal.phone.data,
                form_personal.fax.data, form_personal.specialisation.data)
        if status:
            flash('Personal data updated')
    return render_template('reset_personal.html',
            form_personal=form_personal,title=data['title'],
            first_name=data['first_name'],second_name=data['second_name'], phone=data['phone'],cell=data['cell'],fax=data['fax'],pob=data['pob'],city=data['city'],country=data['country'],
            qualification=data['qualification'],
            specialisation=data['specialisation'])

@app.route('/profile/reset-practice', methods=('GET', 'POST'))
def resetPractice():
    data = checkUser(current_user.id)
    form_practice = updatePracticeForm()
    if request.method == 'POST' and form_practice.validate():
        status = updateUserPractice(current_user.id,
                form_practice.practice_name.data,
                form_practice.practice_number.data,
                form_practice.hpcna_number.data)
        if status:
            flash('Practice data updated')
    return render_template('reset_practice.html', form_practice=form_practice,
            practice_name=data['practice_name'],practice_number=data['practice_number'],
            hpcna_number=data['hpcna_number'])

@app.route('/profile/reset-banking', methods=('GET', 'POST'))
def resetBanking():
    data = checkUser(current_user.id)
    form_banking = updateBankingForm()
    if request.method == 'POST' and form_banking.validate():
        status = updateUserBanking(current_user.id,
                form_banking.bank_holder.data,
                form_banking.bank_account.data,
                form_banking.bank_branch.data,
                form_banking.bank.data)
        if status:
            flash('Banking data  updated')
    return render_template('reset_banking.html', form_banking=form_banking,
            bank_holder=data['bank_holder'], bank_account =
            data['bank_account'], bank_branch = data['bank_branch'], bank =
            data['bank'])



@app.route('/new-patient', methods=('GET', 'POST'))
@login_required
def newPatient():
    form_mva = Patient_mva()
    form_psemas = Patient_psemas()
    form_other = Patient_other()
    if request.method == 'POST' and form_mva.validate_on_submit():
        session["PATIENT"] = form_mva.data
        return redirect('/patient/' + form_mva.name.data + '/new-invoice')
    elif request.method == 'POST' and form_psemas.validate_on_submit():
        session["PATIENT"] = form_psemas.data
        return redirect('/patient/' + form_psemas.name.data + '/new-invoice')
    elif request.method == 'POST' and form_other.validate_on_submit():
        session["PATIENT"] = form_other.data
        return redirect('/patient/' + form_other.name.data + '/new-invoice')
    return render_template('create.html',form_mva=form_mva, form_psemas = form_psemas, form_other = form_other)


@app.route('/patient/<patient>', methods=('GET','POST'))
@login_required
def invoiceOption(patient):
    form_mva = Patient_mva()
    form_psemas = Patient_psemas()
    form_other = Patient_other()
    if request.method == 'POST' and form_mva.validate_on_submit():
        session["PATIENT"] = form_mva.data
        return redirect('/patient/' + form_mva.name.data + '/new-invoice')
    elif request.method == 'POST' and form_psemas.validate_on_submit():
        session["PATIENT"] = form_psemas.data
        return redirect('/patient/' + form_psemas.name.data + '/new-invoice')
    elif request.method == 'POST' and form_other.validate_on_submit():
        session["PATIENT"] = form_other.data
        return redirect('/patient/' + form_other.name.data + '/new-invoice')
    data = queryInvoice(current_user.uuid, patient)
    patient_data = getPatient(current_user.uuid, patient)
    return  render_template('patient.html', patient_data=patient_data, data=data, patient=patient, form_mva=form_mva, form_psemas = form_psemas, form_other = form_other)


@app.route('/patient/<patient>/new-invoice')
@login_required
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
@login_required
def continueInvoice(patient):
    medical = (session.get('PATIENT')["medical"])
    tariff = (session.get('PATIENT')["tariff"])
    date = session.get('PATIENT')['date']
    modifiers = session.get('PATIENT')['modifiers']
    treatments = session.get('PATIENT')['treatments']
    prices = session.get('PATIENT')['values']
    dates = session.get('PATIENT')['dates']
    form = getTreatmentForm(tariff) 
    if (medical == 'mva'):
        po = session.get('PATIENT')['po']
        case = session.get('PATIENT')["case"]
        return render_template('invoice.html', modifiers=modifiers,
                prices=prices, dates=dates,treatments=treatments,form=form, patient = patient, tariff = tariff, po = po, case = case, date = date, medical = medical)
    elif(medical == 'psemas'):
        number = session.get('PATIENT')['number']
        main = session.get('PATIENT')['main']
        dob = session.get('PATIENT')['dob']
        return render_template('invoice.html',modifiers=modifiers,
                prices=prices, dates=dates,treatments=treatments,form=form, patient = patient, tariff = tariff, main = main, dob = dob, date = date, medical = medical, number = number)
    else:
        number = session.get('PATIENT')['number']
        main = session.get('PATIENT')['main']
        dob = session.get('PATIENT')['dob']
        return render_template('invoice.html', modifiers=modifiers,
                prices=prices, dates=dates,treatments=treatments,form=form, patient = patient, tariff = tariff, main = main, dob = dob, date = date, medical = medical, number = number)


@app.route('/generate-invoice', methods=['POST'])
@login_required
def generateInvoice():
    dates = request.form.getlist('date')
    treatments = request.form.getlist('treatments')
    modifiers = request.form.getlist('modifier')
    prices = request.form.getlist('price')
    date_invoice = request.form.getlist('date_invoice')
    tariff = session.get('PATIENT')["tariff"]
    patient = session.get('PATIENT')
    medical = session.get('PATIENT')['medical']
    status = False
    url = ''
    invoice_name = ''
    form = getTreatmentForm(tariff)
    if form.treatments.data:
        treatment_list = getTreatmentByItem(treatments, tariff)
        data = checkUser(current_user.id)
        if 'url' in session['PATIENT']:
            url = session.get('PATIENT')['url']
            invoice_name = session.get('PATIENT')['invoice']
            status = updateInvoice(current_user.uuid, modifiers, treatments,
                    prices, dates, patient, date_invoice)
        else:
            date = session.get('PATIENT')['date']
            index = get_index(current_user.uuid, medical, date)
            url = InvoicePath(patient, index, data)
            url = url.generate()
            invoice_name = InvoiceName(patient, index, modifiers)
            invoice_name = invoice_name.generate()
            status = add_invoice(patient, invoice_name, url, modifiers,
                    treatments, prices, dates, date_invoice, current_user.uuid)
        if status:
            res_dict = {"treatments" : treatments,
                    "treatment_list" : treatment_list,
                    "prices" : prices,
                    "dates" : dates,
                    "patient" : patient,
                    "modifiers" : modifiers,
                    "url" : url,
                    "invoice_name" : invoice_name,
                    "date_invoice" : date_invoice,
                    "data" : data}
            to_json = json.dumps(res_dict)
            subprocess.call([os.getenv("LIBPYTHON"), os.getenv("APP_URL") +
                            '/swriter/main.py', to_json])
                            # json.dumps(treatments),
                            #json.dumps(treatment_list), json.dumps(prices),
                            #json.dumps(dates), json.dumps(patient),
                            #json.dumps(modifiers), json.dumps(url),
                            #json.dumps(invoice_name), json.dumps(date_invoice),
                            # json.dumps(data), to_json])
            return jsonify(result='success')
        else:
            return jsonify(result='Error: Entry already exists')
    return jsonify(result='error')


@app.route('/live-search',methods=['GET','POST'])
@login_required
def liveSearchPatient():
    name = request.args.get('username')
    data = liveSearch(current_user.uuid, name)
    value_json = json.dumps(data)
    return value_json


@app.route('/live-search-treatment',methods=['GET','POST'])
@login_required
def liveSearchTreatment():
    treatment = request.args.get('treatment')
    tariff = session.get('PATIENT')['tariff']
    data, data2 = liveSearchTreatments(treatment, tariff)
    value_json = json.dumps({'treatments' : data, 'procedures': data2})
    return value_json


@app.route('/set-known-invoice',methods=['GET','POST'])
@login_required
def knownInvoice():
    patient = request.args.get('patient')
    date = request.args.get('date')
    data =  getSingleInvoice(current_user.uuid, patient, date)
    d = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    date_deutsch = d.strftime('%d.%m.%Y')
    session["PATIENT"] = data
    session["PATIENT"]["date"]= date_deutsch
    return data


@app.route('/get-value',methods=['GET','POST'])
@login_required
def getValue():
    tariff = session.get('PATIENT')["tariff"]
    item = request.args.get('item', 0, type=int)
    value = getValueTreatments(item, tariff)
    value_json = json.dumps({'value' : Decimal(value['value']), 'description' :
        value['description']}, use_decimal=True)
    return value_json

@app.route('/get-values',methods=['GET','POST'])
@login_required
def getValues():
    tariff = session.get('PATIENT')["tariff"]
    items = session.get('PATIENT')['treatments']
    value_list = getMultipleValues(items, tariff)
    value_list = json.dumps(value_list)
    return value_list


@app.route('/get-treatment-name',methods=['GET','POST'])
@login_required
def getTreatmentName():
    items = request.args.get('items')
    tariff = request.args.get('tariff')
    treatment_list = getTreatmentByGroup(items, tariff)
    value_json = json.dumps({'treatments':treatment_list})
    return value_json


@app.route('/download-invoice/<random>')
@login_required
def downloadInvoice(random):
    name = session.get('PATIENT')['name']
    date = session.get('PATIENT')['date']
    url = getInvoiceURL(current_user.uuid, name, date)
    path = str(url['url']) + ".odt"
    return send_file(path, as_attachment=True)


@app.route('/session')
def sessionValues():
    return str(session.get('PATIENT'))
