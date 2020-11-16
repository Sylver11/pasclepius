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
from application.models import Calendar
from application.db_workbench import newWork, removeWork

api_bp = Blueprint('api_bp',__name__)


@api_bp.route('/live-search-treatment',methods=['GET','POST'])
@login_required
def liveSearchTreatment():
    tariff = request.args.get('tariff')
    treatment = request.args.get('treatment')
    data, data2, data3, data4 = liveSearchTreatments(treatment, tariff)
    value_json = json.dumps({'treatments' : data, 'procedures': data2,
        'categories': data3, 'items': data4})
    return value_json


@api_bp.route('/calendar-events/<arg>',methods=['GET','POST'])
def calendarEvents(arg):
    print(arg)
    if arg == 'retrieve':
        start = request.args.get('start')
        end = request.args.get('end')
        print(end)
        print(start)
        calendar_items = Calendar()
        calendar_items.query.filter(Calendar.start_event <= start,
                Calendar.end_event >= end).all()
        print(calendar_items.id)

        print(calendar_items)
        print('retrieve runs')
        test_data = [{"id":"1",
            "title": "Event 1",
            "start": "2020-11-08T09:00:00",
            "end": "2020-11-08T18:00:00"},]
        return json.dumps(test_data)
    if arg == 'update':
        print("the update runs")
        id = request.args.get('id')
        start = request.args.get('start')
        end = request.args.get('end')
        print(start)
        print(end)
        print(id)
        return json.dumps("success")


    print(start)
    print(end)
    return json.dumps(end)

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
    status = newWork(current_user.uuid, current_user.practice_uuid, work_type, work_quality)
    return json.dumps(status)



@api_bp.route('/remove-job',methods=['GET','POST'])
def removeJob():
    work_type = request.args.get('work_type')
    work_quality = request.args.get('work_quality')
    status = removeWork(current_user.uuid, current_user.practice_uuid, work_type, work_quality)
    return json.dumps(status)

@api_bp.route('/get-invoice-items',methods=['GET','POST'])
def getTreatmentName():
    invoice_id = request.args.get('invoice_id')
    practice_uuid = request.args.get('practice_uuid')
    invoice_items = getItems(practice_uuid, invoice_id)
    return json.dumps(invoice_items,
                sort_keys=True,
                default=str)

