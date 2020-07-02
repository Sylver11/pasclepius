import os
#from flask import current_app as app
from flask import Blueprint, render_template, Response, request, session, jsonify, redirect, url_for, send_file, flash
from werkzeug.urls import url_parse
from application.forms import updateBankingForm, updatePracticeForm,Patient_mva, Patient_psemas, Patient_other,getTreatmentForm, RegistrationForm, LoginForm, updatePasswordForm, updatePersonalForm,  updateLayoutForm
from application.database_io import getTreatmentByItem, getValueTreatments, getMultipleValues, getTreatmentByGroup, liveSearchTreatments
from application.database_invoice import get_index, add_invoice, getInvoiceURL, getSingleInvoice, updateInvoice, liveSearch
from application.database_users import addUser,checkUser, updateUserLayout, updateUserPassword, updateUserPersonal, updateUserPractice, updateUserBanking
from application.url_generator import InvoicePath
from application.name_generator import InvoiceName
from application.models import User, Password
from flask_login import current_user, login_user, logout_user, UserMixin, login_required, fresh_login_required
#from . import login_manager
from datetime import datetime
import datetime as datetime2
from jinja2 import Template
from decimal import *
import subprocess
import simplejson as json

#@login_manager.user_loader
#def load_user(id):
#    data = checkUser(id)
#    if data:
#        return User(id, data["first_name"], data["uuid_text"])                        




api_bp = Blueprint('api_bp',__name__)


####TODO: Reset data queries need to be fitted with MASTER_POS_WAIT######




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
    medical = session.get('PATIENT')['medical']
    status = False
    url = ''
    invoice_name = ''
    form = getTreatmentForm(tariff)
    if form.treatments.data:
        treatment_list = getTreatmentByItem(treatments, tariff)
        data = checkUser(current_user.id)
        if 'url' in session['PATIENT']:
            url = session.get('PATIENT')['url']
            invoice_name = session.get('PATIENT')['invoice']
            status = updateInvoice(layout, current_user.uuid,
                    modifiers, treatments, prices, dates,
                    patient, date_invoice)
        else:
            date_created = session.get('PATIENT')['date_created']
            index = get_index(current_user.uuid, medical, date_created)
            url = InvoicePath(patient, index, data)
            url = url.generate()
            invoice_name = InvoiceName(patient, index, modifiers)
            invoice_name = invoice_name.generate()
            status = add_invoice(layout, patient, invoice_name, url, modifiers,
                    treatments, prices, dates, date_invoice, current_user.uuid)
        if status:
            res_dict = {'layout' : layout,
                    "treatments" : treatments,
                    "treatment_list" : treatment_list,
                    "prices" : prices,
                    "dates" : dates,
                    "patient" : patient,
                    "modifiers" : modifiers,
                    "url" : url,
                    "invoice_name" : invoice_name,
                    "date_invoice" : date_invoice,
                    "data" : data}
            to_json = json.dumps(res_dict)
            subprocess.call([os.getenv("LIBPYTHON"), os.getenv("APP_URL") +
                            '/swriter/main.py', to_json])
            return jsonify(result='success')
        else:
            return jsonify(result='Error: Entry already exists. Have a look at past invoices to continue this invoice.')
    return jsonify(result='error')


@api_bp.route('/live-search',methods=['GET','POST'])
@login_required
def liveSearchPatient():
    name = request.args.get('username')
    data = liveSearch(current_user.uuid, name)
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
    name = session.get('PATIENT')['name']
    date = session.get('PATIENT')['date']
    url = getInvoiceURL(current_user.uuid, name, date)
    path = str(url['url']) + ".odt"
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
