import os
from flask import Blueprint, request, session, send_file
from application.forms import getTreatmentForm
from application.db_tariffs import getTreatmentByItem, getValueTreatments, getMultipleValues, getTreatmentByGroup, liveSearchTreatments
from application.db_invoice import get_index, add_invoice, getInvoiceURL, getSingleInvoice, updateInvoice, liveSearch
from application.db_users import checkUser
from application.url_generator import InvoicePath
from application.name_generator import InvoiceName
from flask_login import current_user, login_required
from datetime import datetime
import datetime as datetime2
from decimal import *
import subprocess
import simplejson as json


api_bp = Blueprint('api_bp',__name__)


@api_bp.route('/generate-invoice', methods=['POST'])
@login_required
def generateInvoice():
    data = checkUser(current_user.id)
    layout = data['invoice_layout']
    dates = request.form.getlist('date')
    treatments = request.form.getlist('treatments')
    modifiers = request.form.getlist('modifier')
    prices = request.form.getlist('price')
    date_invoice = request.form.getlist('date_invoice')
    tariff = session.get('PATIENT')["tariff"]
    patient = session.get('PATIENT')
    medical_aid = session.get('PATIENT')['medical_aid']
    status = False
    invoice_file_url = ''
    invoice_id = ''
    form = getTreatmentForm(tariff)
    if form.treatments.data:
        treatment_list = getTreatmentByItem(treatments, tariff)
        data = checkUser(current_user.id)
        if 'invoice_file_url' in session['PATIENT']:
            invoice_file_url = session.get('PATIENT')['invoice_file_url']
            invoice_id = session.get('PATIENT')['invoice_id']
            status = updateInvoice(layout, current_user.uuid,
                    modifiers, treatments, prices, dates,
                    patient, date_invoice)
        else:
            date_created = session.get('PATIENT')['date_created']
            index = get_index(current_user.uuid, medical_aid, date_created)
            invoice_file_url = InvoicePath(patient, index, data)
            invoice_file_url = invoice_file_url.generate()
            invoice_id = InvoiceName(patient, index, modifiers)
            invoice_id = invoice_id.generate()
            status = add_invoice(layout, patient, invoice_id, invoice_file_url, modifiers,
                    treatments, prices, dates, date_invoice, current_user.uuid)
        if status:
            res_dict = {'layout' : layout,
                    "treatments" : treatments,
                    "treatment_list" : treatment_list,
                    "prices" : prices,
                    "dates" : dates,
                    "patient" : patient,
                    "modifiers" : modifiers,
                    "invoice_file_url" : invoice_file_url,
                    "invoice_id" : invoice_id,
                    "date_invoice" : date_invoice,
                    "data" : data}
            to_json = json.dumps(res_dict)
            subprocess.call([os.getenv("LIBPYTHON"), os.getenv("APP_URL") +
                            '/swriter/main.py', to_json])
            return json.dumps({'result':'success'})
        else:
            return json.dumps({'result':'Error: Entry already exists. Have a look at past invoices to continue this invoice.'})
        return json.dumps({'result':'error'})


@api_bp.route('/live-search',methods=['GET','POST'])
@login_required
def liveSearchPatient():
    patient_name = request.args.get('patient_name')
    data = liveSearch(current_user.uuid, patient_name)
    value_json = json.dumps(data)
    return value_json


@api_bp.route('/live-search-treatment',methods=['GET','POST'])
@login_required
def liveSearchTreatment():
    treatment = request.args.get('treatment')
    tariff = session.get('PATIENT')['tariff']
    data, data2, data3, data4 = liveSearchTreatments(treatment, tariff)
    value_json = json.dumps({'treatments' : data, 'procedures': data2,
        'categories': data3, 'items': data4})
    return value_json


@api_bp.route('/set-known-invoice',methods=['GET','POST'])
@login_required
def knownInvoice():
    patient = request.args.get('patient')
    date_created = request.args.get('date_created')
    data =  getSingleInvoice(current_user.uuid, patient, date_created)
    for o, i in data.items():
        if i == 'None':
           data[o] = ''
        if isinstance(i, datetime2.datetime):
            d = datetime.strptime(i.__str__(), '%Y-%m-%d %H:%M:%S')
            date = d.strftime('%d.%m.%Y')
            data[o] = date
    session["PATIENT"] = data
    return data


@api_bp.route('/get-value',methods=['GET','POST'])
@login_required
def getValue():
    tariff = session.get('PATIENT')["tariff"]
    item = request.args.get('item', 0, type=int)
    value = getValueTreatments(item, tariff)
    value_json = json.dumps({'value' : Decimal(value['value']), 'description' :
        value['description']}, use_decimal=True)
    return value_json


@api_bp.route('/get-values',methods=['GET','POST'])
@login_required
def getValues():
    tariff = session.get('PATIENT')["tariff"]
    items = session.get('PATIENT')['treatments']
    value_list = getMultipleValues(items, tariff)
    value_list = json.dumps(value_list)
    return value_list


@api_bp.route('/get-treatment-name',methods=['GET','POST'])
@login_required
def getTreatmentName():
    items = request.args.get('items')
    tariff = request.args.get('tariff')
    treatment_list = getTreatmentByGroup(items, tariff)
    value_json = json.dumps({'treatments':treatment_list})
    return value_json


@api_bp.route('/download-invoice/<random>')
@login_required
def downloadInvoice(random):
    patient_name = session.get('PATIENT')['patient_name']
    date = session.get('PATIENT')['date']
    invoice_file_url = getInvoiceURL(current_user.uuid, patient_name, date)
    path = str(invoice_file_url['invoice_file_url']) + ".odt"
    return send_file(path, as_attachment=True)


@api_bp.route('/update-session', methods=['GET'])
def updateSession():
    if 'GET' == request.method:
        description = request.args.get('description')
        item = request.args.get('item')
        session_data = session['PATIENT']
        session_data[description] = item
        session['PATIENT'] = session_data
        return json.dumps('success')


@api_bp.route('/session')
def sessionValues():
    return str(session.get('PATIENT'))
