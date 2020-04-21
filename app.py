from flask import Flask, render_template, Response, request, session, jsonify, redirect, url_for, send_file
from jinja2 import Template
from forms import Patient_mva, Patient_psemas, Patient_other, getTreatmentForm
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
    form_other = Patient_other()
    if form_mva.validate_on_submit():
        session["PATIENT"] = request.values
       # print(request.values)
        jsonData = jsonify(data={"medical": str(form_mva.medical.data), 'name': str(form_mva.name.data),'case': str(form_mva.case.data), 'po':str(form_mva.po.data), 'date': str(form_mva.date.data) })
        return jsonData
    if form_psemas.validate_on_submit():
        session["PATIENT"] = request.values
       # print(request.values)
        jsonData = jsonify(data={"medical": str(form_psemas.medical.data), 'name': str(form_psemas.name.data),'main': str(form_psemas.main.data), 'dob':str(form_psemas.dob.data), 'date': str(form_psemas.date.data), 'number': str(form_psemas.number.data)})
        return jsonData
    if form_other.validate_on_submit():
        session["PATIENT"] = request.values
       # print(request.values)
        jsonData = jsonify(data={"medical": str(form_other.medical.data), 'name': str(form_other.name.data),'main': str(form_other.main.data), 'dob':str(form_other.dob.data), 'date': str(form_other.date.data), 'number': str(form_other.number.data)})
        return jsonData
   # print(form_psemas.errors)
   # return jsonify(data=form_mva.errors)


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
    if form.treatments.data:
        getTreatmentByItem(treatments, tariff, price, dates, patient, modifier)
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
    print(name)
    path = "/Users/justusvoigt/Documents/" + str(name) + ".odt"
    print(path)
    print("this is running")
    return send_file(path, as_attachment=True)

@app.route('/session')
def sessionValues():
    return str(session.get('PATIENT'))


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port =4003, debug=True, threaded=True)
