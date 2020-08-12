import os
from flask import Blueprint, request, session, send_file, jsonify
from application.forms import getTreatmentForm
from application.db_tariffs import getTreatmentByItem, getValueTreatments, getMultipleValues, getTreatmentByGroup, liveSearchTreatments
from application.db_invoice import get_index, getInvoiceURL, getSingleInvoice, getItems
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



#@api_bp.route('/live-search',methods=['GET','POST'])
#@login_required
#def liveSearchPatient():
#    patient_name = request.args.get('patient_name')
#    data = liveSearch(current_user.uuid, patient_name##)
#    value_json = json.dumps(data)
#    return value_json


@api_bp.route('/live-search-treatment',methods=['GET','POST'])
@login_required
def liveSearchTreatment():
    tariff = request.args.get('tariff')
    treatment = request.args.get('treatment')
#    tariff = session.get('PATIENT')['tariff']
    data, data2, data3, data4 = liveSearchTreatments(treatment, tariff)
    value_json = json.dumps({'treatments' : data, 'procedures': data2,
        'categories': data3, 'items': data4})
    return value_json



@api_bp.route('/get-value',methods=['GET','POST'])
@login_required
def getValue():
    item = request.args.get('item', 0, type=int)
    tariff = request.args.get('tariff')
    treatment_items = getValueTreatments(item, tariff)
    return json.dumps(treatment_items)


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
    return json.dumps(invoice_items,
                sort_keys=True,
                default=str)


@api_bp.route('/download-invoice/<random>')
@login_required
def downloadInvoice(random):
    patient_name = session.get('PATIENT')['patient_name']
    date = session.get('PATIENT')['date']
    invoice_file_url = getInvoiceURL(current_user.uuid, patient_name, date)
    path = str(invoice_file_url['invoice_file_url']) + ".odt"
    return send_file(path, as_attachment=True)

