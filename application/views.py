from flask import current_app as app
import subprocess 
import os
from flask import render_template, Response, request, session, jsonify, redirect, url_for, send_file
from jinja2 import Template
from application.forms import Patient_mva, Patient_psemas, Patient_other, getTreatmentForm
import simplejson as json
from decimal import *
from application.database_io import getTreatmentByItem, getValueTreatments

@app.route('/', methods=('GET', 'POST'))
def home():
    return render_template('index.html')


@app.route('/patient', methods=('GET', 'POST'))
def findPatient():
    form_mva = Patient_mva()
    form_psemas = Patient_psemas()
    form_other = Patient_other()
    return render_template('patient.html', form_mva=form_mva, form_psemas = form_psemas, form_other = form_other)


@app.route('/patient/select', methods=('GET', 'POST'))
def selectPatient():
    form_mva = Patient_mva()
    form_psemas = Patient_psemas()
    form_other = Patient_other()
    if form_mva.validate_on_submit() or form_psemas.validate_on_submit() or form_other.validate_on_submit():
        session["PATIENT"] = request.values
        jsonData = jsonify(data={'name': str(form_mva.name.data)})
        return jsonData


@app.route('/patient/<patient>/new-invoice')
def newInvoice(patient):
    medical = (session.get('PATIENT')["medical"])
    tariff = (session.get('PATIENT')["tariff"])
    date = session.get('PATIENT')['date']
    form = getTreatmentForm(tariff) 
    if (medical == 'mva'):
        po = session.get('PATIENT')['po']
        case = session.get('PATIENT')["case"]
        return render_template('invoice.html', form=form, patient = patient, tariff = tariff, po = po, case = case, date = date, medical = medical)
    elif(medical == 'psemas'):
        number = session.get('PATIENT')['number']
        main = session.get('PATIENT')['main']
        dob = session.get('PATIENT')['dob']
        return render_template('invoice.html', form=form, patient = patient, tariff = tariff, main = main, dob = dob, date = date, medical = medical, number = number)
    else:
        number = session.get('PATIENT')['number']
        main = session.get('PATIENT')['main']
        dob = session.get('PATIENT')['dob']
        return render_template('invoice.html', form=form, patient = patient, tariff = tariff, main = main, dob = dob, date = date, medical = medical, number = number)


@app.route('/generate-invoice', methods=['POST'])
def generateInvoice():
    dates = request.form.getlist('date')
    treatments = request.form.getlist('treatments')
    modifier = request.form.getlist('modifier')
    price = request.form.getlist('price')
    tariff = session.get('PATIENT')["tariff"]
    patient = session.get('PATIENT')
    form = getTreatmentForm(tariff) 
    print(price)
    print(treatments)
    if form.treatments.data:
        treatment_list = getTreatmentByItem(treatments, tariff)
        subprocess.call([os.getenv("LIBPYTHON"), os.getenv("APP_URL") + '/application/swriter.py', json.dumps(treatments), json.dumps(treatment_list), json.dumps(price), json.dumps(dates), json.dumps(patient), json.dumps(modifier)])
        return jsonify(result='success')
    return jsonify(result='error')


@app.route('/get-value',methods=['GET','POST'])
def getValue():
    tariff = session.get('PATIENT')["tariff"]
    item = request.args.get('item', 0, type=int)
    value = getValueTreatments(item, tariff)
    value_json = json.dumps({'value' : Decimal(value['value'])}, use_decimal=True)
    return value_json


@app.route('/download-invoice')
def downloadInvoice():
    name = session.get('PATIENT')["name"]
    path = "Users/justusvoigt/Documents/" + str(name) + ".odt"
    return send_file(path, as_attachment=True)

@app.route('/session')
def sessionValues():
    return str(session.get('PATIENT'))

