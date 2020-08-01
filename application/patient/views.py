from application.url_generator import InvoicePath
from application.name_generator import InvoiceName
from werkzeug.datastructures import ImmutableMultiDict
from flask_login import current_user, login_required
from flask import render_template, Blueprint, request, session, redirect
from application.db_workbench import newWork, lastFive, removeWork
from application.db_users import checkUser
from application.forms import Patient_mva, Patient_psemas, Patient_other,getTreatmentForm
from application.db_invoice import insertInvoice, get_index, queryInvoice, getPatient, getSingleInvoice, getItems
from datetime import datetime
import datetime as datetime2
import simplejson as json
import re
import subprocess
import os

patient_bp = Blueprint('patient_bp',__name__,
        template_folder='templates', static_folder='static')


@patient_bp.route('')
@login_required
def invoiceTab():
    return render_template('patient/tab_bar.html')


@patient_bp.route('/<patient>', methods=('GET','POST'))
@login_required
def invoiceOption(patient):
    form_mva = Patient_mva()
    form_psemas = Patient_psemas()
    form_other = Patient_other()
    if request.method == 'POST' and form_mva.validate_on_submit():
        session["PATIENT"] = form_mva.data
        return redirect('/patient/' + form_mva.patient_name.data + '/new-invoice')
    elif request.method == 'POST' and form_psemas.validate_on_submit():
        session["PATIENT"] = form_psemas.data
        return redirect('/patient/' + form_psemas.patient_name.data + '/new-invoice')
    elif request.method == 'POST' and form_other.validate_on_submit():
        session["PATIENT"] = form_other.data
        return redirect('/patient/' + form_other.patient_name.data + '/new-invoice')
    data = queryInvoice(current_user.uuid, patient)
    patient_data = getPatient(current_user.uuid, patient)
    return render_template('patient/patient.html',
            patient_data = patient_data,
            data = data,
            patient = patient,
            form_mva = form_mva,
            form_psemas = form_psemas,
            form_other = form_other,
            page_title = 'Continue previous')


@patient_bp.route('/invoice/create', methods=('GET', 'POST'))
@login_required
def createPatient():
    form_mva = Patient_mva()
    form_other = Patient_other()
    return render_template('patient/create.html',
            form_mva = form_mva,
            form_other = form_other,
            layout_code = current_user.invoice_layout,
            page_title = 'Create new patient')


@patient_bp.route('/invoice/continue', methods=('GET', 'POST'))
@login_required
def Continue():
    return render_template('patient/continue.html',
            page_title = 'Continue previous invoice')


@patient_bp.route('/invoice/new', methods=('GET', 'POST'))
@login_required
def newInvoice():
    if request.method == 'POST':
        patient_info = request.form.to_dict()
        patient_name = request.form['patient_name']
        medical_aid = request.form['medical_aid']
        date_created = request.form['date_created']
        tariff = request.form['tariff']
        item_modifiers = []
        invoice_index = get_index(current_user.uuid, medical_aid, date_created)
        invoice_file_url = InvoicePath(date_created,
                medical_aid,
                patient_name,
                invoice_index,
                current_user.first_name,
                current_user.practice_name)
        invoice_file_url = invoice_file_url.generate()
        invoice_id = InvoiceName(medical_aid, date_created, invoice_index, item_modifiers)
        invoice_id = invoice_id.generate()
        patient_info['invoice_id'] = invoice_id
        patient_info['invoice_file_url'] = invoice_file_url
        patient_info['invoice_layout'] = current_user.invoice_layout
        newWork(current_user.uuid, 'invoice_draft', json.dumps(patient_info))
        form = getTreatmentForm(tariff)
        status = 'new_draft'
    else:
        tariff = request.args.get('tariff')
        status = request.args.get('status')
        form = getTreatmentForm(tariff)
    return render_template('patient/' + tariff[:-5] + '.html',
                status = status,
                form = form)

@patient_bp.route('/invoice/<medical_aid>/<year>/<index>')
@login_required
def Invoice(medical_aid, year, index):
    invoice_id = medical_aid + "/" + year + "/" + index
    invoice = getSingleInvoice(current_user.uuid, invoice_id)
    treatments = getItems(current_user.uuid, invoice_id)
    newWork(current_user.uuid, 'invoice_tab', invoice_id)
    for i in treatments:
        for o in i:
            if isinstance(i[o], datetime2.datetime):
                d = datetime.strptime(i[o].__str__(), '%Y-%m-%d %H:%M:%S')
                date = d.strftime('%d.%m.%Y')
                i[o] = date

    for o, i in invoice.items():
        if i == 'None':
           invoice[o] = ''
        if isinstance(i, datetime2.datetime):
            d = datetime.strptime(i.__str__(), '%Y-%m-%d %H:%M:%S')
            date = d.strftime('%d.%m.%Y')
            invoice[o] = date
    invoice['treatments'] = treatments
    form = getTreatmentForm(invoice['tariff'])
    return render_template('patient/' + invoice['tariff'][:-5] + '.html',
            invoice = json.dumps(invoice),
            status = invoice['status'],
            form = form)


@patient_bp.route('/last-five')
def lastFiveTabs():
    work_quality = request.args.get('work_type')
    last_five = lastFive(current_user.uuid, work_quality)
    return json.dumps(last_five)


@patient_bp.route('/invoice/generate', methods=['POST'])
def NewInvoice():
    if request.form:
        status = {}
        try:
            status = insertInvoice(current_user.uuid, request.form)
        except Exception as e:
            status['db_status'] = 'Error'
            status['db_description'] = 'Exit code: ' + str(e)
            return json.dumps(status)
        method = None
        if status['db_status'] == 'Success' and request.form.get('method'):
            user = checkUser(current_user.id)
            res_dict = {
                "user" : user,
                "invoice": request.form,
                "treatments": request.form.getlist('treatments'),
                "descriptions": request.form.getlist('description'),
                "units": request.form.getlist('units'),
                "post_values": request.form.getlist('post_value'),
                "dates": request.form.getlist('date'),
                "modifiers": request.form.getlist('modifier')
                  }
            to_json = json.dumps(res_dict)
            try:
                subprocess.check_output([os.getenv("LIBPYTHON"), os.getenv("APP_URL")
                + '/swriter/main.py', to_json])
            except subprocess.CalledProcessError as e:
                status['swriter_status'] = 'Error'
                if e.returncode == 1:
                    status['swriter_description'] =  'NoConnectException: Connector : could not connect to socket (Connection refused)'
                else:
                    status['swriter_description'] = 'Exit code: ' + e.returncode
                return json.dumps(status)
            status['swriter_status'] = 'Success'
            status['swriter_description'] = 'Invoice file created'
        return json.dumps(status)
    return json.dumps({'status': 'Fatal error. Could not read form data.'})

