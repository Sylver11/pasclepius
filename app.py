from flask import Flask, render_template, Response, request, session, jsonify, redirect, url_for
from jinja2 import Template
from forms import Patient_mva, Patient_psemas, Patient_other, getFormByYear
import simplejson as json
from decimal import *
from database_io import getTreatmentByItem, getValueTreatments
app = Flask(__name__)


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
    if form_mva.validate_on_submit():
        session["PATIENT"] = request.values
        print(request.values)
        jsonData = jsonify(data={"medical": str(form_mva.medical.data), 'name': str(form_mva.name.data),'case': str(form_mva.case.data), 'po':str(form_mva.po.data), 'date': str(form_mva.date.data) })
        return jsonData
    if form_psemas.validate_on_submit():
        session["PATIENT"] = request.values
        print(request.values)
        jsonData = jsonify(data={"medical": str(form_mva.medical.data), 'name': str(form_mva.name.data),'case': str(form_mva.case.data), 'po':str(form_mva.po.data), 'date': str(form_mva.date.data) })
        return jsonData
    print(form_psemas.errors)
    return jsonify(data=form_mva.errors)


@app.route('/patient/<patient>/new-invoice')
def newInvoice(patient):
    tariff = session.get('PATIENT')["tariff"]
    form = getFormByYear(tariff) 
    set_choices = [(105, 'Muscle and nerve stimulating currents'),(301,'Percussion'),(314, 'Lymph drainage')]
    return render_template('invoice.html', form=form, set_choices=set_choices, patient = patient, tariff = session.get('PATIENT')["tariff"], po = session.get('PATIENT')["po"], case = session.get('PATIENT')["case"], date = session.get('PATIENT')["date"], medical = session.get('PATIENT')['medical'])


@app.route('/session')
def sessionValues():
      return str(session.get('PATIENT')["po"])


@app.route('/generate-invoice', methods=['POST'])
def generateInvoice():
    form = Treatment()
    dates = request.form.getlist('date')
    treatments = request.form.getlist('treatments')
    price = request.form.getlist('price')
    tariff = session.get('PATIENT')["tariff"]
    patient = session.get('PATIENT')
    if form.treatments.data:
        getTreatmentByItem(treatments, tariff, price, dates, patient)
        return jsonify(result='success')
    return jsonify(result='error')


@app.route('/get-value',methods=['GET','POST'])
def getValue():
    tariff = session.get('PATIENT')["tariff"]
    item = request.args.get('item', 0, type=int)
    value = getValueTreatments(item, tariff)
    value_json = json.dumps({'value' : Decimal(value['value'])}, use_decimal=True)
    return value_json
 

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port =4003, debug=True, threaded=True)
