from flask_login import current_user, login_required
from flask import render_template, Blueprint, request, session, redirect
from application.db_users import checkUser
from application.forms import Patient_mva, Patient_psemas, Patient_other,getTreatmentForm
from application.db_invoice import queryInvoice, getPatient, getSingleInvoice, getItems
from datetime import datetime
import datetime as datetime2

patient_bp = Blueprint('patient_bp',__name__,
        template_folder='templates', static_folder='static')


@patient_bp.route('/new-patient', methods=('GET', 'POST'))
@login_required
def newPatient():
    data = checkUser(current_user.id)
    layout_code = data['invoice_layout']
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
    return render_template('patient/create.html',
            form_mva = form_mva,
            form_psemas = form_psemas,
            form_other = form_other,
            layout_code = layout_code,
            page_title = 'Create new patient')

@patient_bp.route('/continue', methods=('GET', 'POST'))
@login_required
def Continue():
    return render_template('patient/continue.html',
            page_title = 'Continue previous invoice')

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


@patient_bp.route('/<patient>/new-invoice')
@login_required
def newInvoice(patient):
    medical_aid = (session.get('PATIENT')["medical_aid"])
    tariff = (session.get('PATIENT')["tariff"])
    form = getTreatmentForm(tariff)
    data = checkUser(current_user.id)
    layout_code = data['invoice_layout']
    return render_template('patient/invoice.html',
                dates = None,
                treatments = None,
                form = form,
                patient = patient,
                layout_code = layout_code,
                page_title = 'New ' + medical_aid + ' invoice')





@patient_bp.route('/<patient>/continue-invoice')
@login_required
def continueInvoice(patient):
    data = checkUser(current_user.id)
    layout_code = data['invoice_layout']
    medical_aid = (session.get('PATIENT')["medical_aid"])
    tariff = (session.get('PATIENT')["tariff"])
    form = getTreatmentForm(tariff) 
    return render_template('patient/invoice.html',
                form = form,
                layout_code = layout_code,
                page_title = 'Continue ' + medical_aid + ' invoice')




@patient_bp.route('/set-known-invoice',methods=['GET','POST'])
def knownInvoice():
    invoice_id = request.args.get('invoice_id')
    invoice =  getSingleInvoice(current_user.uuid, invoice_id)
    treatments = getItems(current_user.uuid, invoice_id)
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
    session["PATIENT"] = invoice
    return 'success'
