import os
from flask import Blueprint, request, session, send_file, jsonify
from application.forms import getTreatmentForm
from application.db_tariffs import getTreatmentByItem, getValueTreatments, getMultipleValues, getTreatmentByGroup, liveSearchTreatments
from application.db_invoice import get_index, add_invoice, getInvoiceURL, getSingleInvoice, updateInvoice, liveSearch, getItems
from application.db_users import checkUser
from application.url_generator import InvoicePath
from application.name_generator import InvoiceName
from flask_login import current_user, login_required
from datetime import datetime
import datetime as datetime2
from decimal import *
import subprocess
import simplejson as json

from application.db_workbench import newWork, removeWork

api_bp = Blueprint('api_bp',__name__)


@api_bp.route('/generate-invoice', methods=['POST'])
def generateInvoice():
    print(request.form)
    user = checkUser(current_user.id)
    patient = session.get('PATIENT')
    form = getTreatmentForm(patient['tariff'])
    if request.form:
        item_dates = request.form.getlist('date')
        item_numbers = request.form.getlist('treatments')
        item_modifiers = request.form.getlist('modifier')
        item_values = request.form.getlist('value')
        item_descriptions = getTreatmentByItem(item_numbers, patient['tariff'])
        date_invoice = request.form.getlist('date_invoice')
        invoice_file_url = invoice_id = status = None
        if 'invoice_file_url' in patient:
            invoice_file_url = patient['invoice_file_url']
            invoice_id = patient['invoice_id']
            status = updateInvoice(user, patient, date_invoice, item_numbers, item_descriptions, item_values, item_dates, item_modifiers)
        else:
            index = get_index(current_user.uuid, patient['medical_aid'], patient['date_created'])
            invoice_file_url = InvoicePath(patient, index, user)
            invoice_file_url = invoice_file_url.generate()
            invoice_id = InvoiceName(patient, index, item_modifiers)
            invoice_id = invoice_id.generate()
            status = add_invoice(user, patient, invoice_id, invoice_file_url, date_invoice, item_numbers, item_descriptions, item_values, item_dates, item_modifiers)
        if status:
            res_dict = {
                    "user" : user,
                    "patient" : patient,
                    "item_numbers" : item_numbers,
                    "item_descriptions" : item_descriptions,
                    "item_values" : item_values,
                    "item_dates" : item_dates,
                    "item_modifiers" : item_modifiers,
                    "invoice_file_url" : invoice_file_url,
                    "invoice_id" : invoice_id,
                    "date_invoice" : date_invoice
                    }
            to_json = json.dumps(res_dict)
            subprocess.call([os.getenv("LIBPYTHON"), os.getenv("APP_URL") +
                            '/swriter/main.py', to_json])
            return jsonify("success")
        else:
            return jsonify('Error: Entry already exists. Have a look at past invoices to continue this invoice.')
       # return jsonify('error')
    return jsonify('error')


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

#TODO delete this part also try to get getValue and getTreatmentName moved and 
#then removed
#@api_bp.route('/set-known-invoice',methods=['GET','POST'])
#def knownInvoice():
#    invoice_items = request.args.get('invoice_items')
#    invoice_id = request.args.get('invoice_id')
#    invoice =  getSingleInvoice(current_user.uuid, invoice_id)
#    json_data = json.loads(invoice_items)
#    invoice['treatments'] = json_data
#    for o, i in invoice.items():
#        if i == 'None':
#           invoice[o] = ''
#        if isinstance(i, datetime2.datetime):
#            d = datetime.strptime(i.__str__(), '%Y-%m-%d %H:%M:%S')
#            date = d.strftime('%d.%m.%Y')
#            invoice[o] = date
#    session["PATIENT"] = invoice
#    print(invoice)
#    return json.dumps({'message': 'New User Created!'})


@api_bp.route('/get-value',methods=['GET','POST'])
@login_required
def getValue():
    #tariff = session.get('PATIENT')["tariff"]
    item = request.args.get('item', 0, type=int)
    tariff = request.args.get('tariff')
    value = getValueTreatments(item, tariff)
    value_json = json.dumps({'value' : value['value_cent'], 'description' :
        value['description']})
    return value_json


@api_bp.route('/add-job',methods=['GET','POST'])
def newJob():
    work_type = request.args.get('work_type')
    work_quality = request.args.get('work_quality')
    status = newWork(current_user.uuid, work_type, work_quality)
    return json.dumps(status)



@api_bp.route('/remove-job',methods=['GET','POST'])
def removeJob():
    work_type = request.args.get('work_type')
    work_quality = request.args.get('work_quality')
    status = removeWork(current_user.uuid, work_type, work_quality)
    return json.dumps(status)

@api_bp.route('/get-invoice-items',methods=['GET','POST'])
def getTreatmentName():
    invoice_id = request.args.get('invoice_id')
    uuid = request.args.get('uuid')
    invoice_items = getItems(uuid, invoice_id)
    for i in invoice_items:
        for o in i:
            if isinstance(i[o], datetime2.datetime):
                d = datetime.strptime(i[o].__str__(), '%Y-%m-%d %H:%M:%S')
                date = d.strftime('%d.%m.%Y')
                i[o] = date
    return json.dumps(invoice_items)


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
