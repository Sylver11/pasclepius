from flask import Flask, render_template, Response, request, session, jsonify, redirect, url_for
from jinja2 import Template
from forms import Patient, Treatment
import json
from database_io import getTreatmentByItem
app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def contact():
    form = Patient()
    return render_template('index.html', form=form)


@app.route('/patient', methods=('GET', 'POST'))
def findPatient():
    form = Patient()
    return render_template('patient.html', form=form)


@app.route('/patient/select', methods=('GET', 'POST'))
def selectPatient():
    form = Patient()
    if form.validate_on_submit():
        session["PATIENT"] = request.values
        jsonData = jsonify(data={"medical": str(form.medical.data), 'name': str(form.name.data),'case': str(form.case.data), 'po': str(form.po.data), 'date': str(form.date.data) })
        return jsonData
    return jsonify(data=form.errors)


@app.route('/patient/<patient>/new-invoice')
def newInvoice(patient):
    form = Treatment() 
    set_choices = [(105, 'Muscle and nerve stimulating currents'),(301,'Percussion'),(314, 'Lymph drainage')]
    return render_template('index.html', form=form, set_choices=set_choices, patient = patient, po = session.get('PATIENT')["po"], case = session.get('PATIENT')["case"], date = session.get('PATIENT')["date"], medical = session.get('PATIENT')['medical'])


@app.route('/session')
def sessionValues():
      return str(session.get('PATIENT')["po"])


@app.route('/generate-invoice', methods=['POST'])
def generateInvoice():
    form = Treatment()
    dates = request.form.getlist('date')
    treatments = request.form.getlist('treatments')
    patient = session.get('PATIENT')
    if form.treatments.data:
        getTreatmentByItem(treatments, dates, patient)
        return jsonify(result='success')
    return jsonify(result='error')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port =4003, debug=True, threaded=True)
