import os
from flask import Blueprint, request, session, jsonify
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
from application import db
from application.db_workbench import newWork, removeWork
import sys
from backports.datetime_fromisoformat import MonkeyPatch
if sys.version_info[1] < 7:
    MonkeyPatch.patch_fromisoformat()

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
    try:
        user = current_user.practice_uuid
        id = request.args.get('id')
        title = request.args.get('title')
        color = request.args.get('color')
        text_color = request.args.get('text_color')
        start = request.args.get('start')
        end = request.args.get('end')
        if arg == 'retrieve':
            _CalendarEntries = db.session.query(Calendar).\
                    filter(Calendar.practice_uuid == user,
                            Calendar.start >= start,
                            Calendar.end <= end).\
                                    all()
            return jsonify(_CalendarEntries)
        if arg=='add':
            _AddNewAppointment = Calendar(practice_uuid=user,
                    title=title,
                    start=datetime.fromisoformat(start),
                    end=datetime.fromisoformat(end),
                    color=color,
                    text_color=text_color)
            db.session.add(_AddNewAppointment)
            db.session.commit()
            return jsonify(_AddNewAppointment.id)
        if arg == 'detail':
            _CalendarEntries = db.session.query(Calendar).\
                    filter(Calendar.practice_uuid == user,
                            Calendar.id == id).\
                                    all()
            return jsonify(_CalendarEntries)
        if arg == 'update':
            db.session.query(Calendar).\
                    filter(Calendar.id == id).\
                    update({Calendar.start:datetime.fromisoformat(start),
                        Calendar.end:datetime.fromisoformat(end)})
            db.session.commit()
            return jsonify("success")
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        errorMessage = template.format(type(ex).__name__, ex.args)
        return jsonify(errorMessage), 500


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

