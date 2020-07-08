from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from application.db_invoice import getAllInvoices, liveSearchInvoices, updateSubmitted, updateCredit, getInvoiceByInvoiceName, queryR
import simplejson as json
from datetime import datetime
import datetime as datetime2


account_bp = Blueprint('account_bp',
        __name__,
        template_folder='templates',
        static_folder='static')


@account_bp.route("/", methods=['GET','POST'])
@login_required
def gerneral():
    return render_template('account_bp/general.html')

@account_bp.route("/invoices-due", methods=['GET'])
@login_required
def due():
    return render_template('account_bp/due.html')


@account_bp.route("/invoices-not-submitted", methods=['GET'])
@login_required
def unsubmitted():
    return render_template('account_bp/not_submitted.html')


@account_bp.route("/settings", methods=['GET'])
@login_required
def settings():
    return render_template('account_bp/settings.html')


@account_bp.route("/invoice/<medical_aid>/<year>/<index>", methods=['GET'])
def singleInvoice(medical_aid, year, index):
    invoice_id = medical_aid + "/" + year + "/" + index
    invoice = getInvoiceByInvoiceName(current_user.uuid, invoice_id)
    for o, i in invoice.items():
         if isinstance(i, datetime2.datetime):
             d = datetime.strptime(i.__str__(), '%Y-%m-%d %H:%M:%S')
             date = d.strftime('%d.%m.%Y')
             invoice[o] = date
    return render_template('account_bp/invoice.html',
            invoice_json = json.dumps(invoice),
            invoice = invoice)


@account_bp.route('/live-search-invoice',methods=['GET','POST'])
def liveSearchTreatment():
    patient_name = request.args.get('patient_name')
    invoices = liveSearchInvoices(current_user.uuid, patient_name)
    for i in invoices:
        for o in i:
            if isinstance(i[o], datetime2.datetime):
                d = datetime.strptime(i[o].__str__(), '%Y-%m-%d %H:%M:%S')
                date = d.strftime('%d.%m.%Y')
                i[o] = date
    return json.dumps({'invoices' : invoices})

@account_bp.route('/submit-invoice',methods=['GET'])
def submitInvoice():
    invoice_id = request.args.get('invoice_id')
    status = updateSubmitted(current_user.uuid, invoice_id)
    if status:
        return json.dumps(invoice_id + " was succesfully submitted")
    else:
        return json.dumps("Something went wrong. Please contact the system administrator")


@account_bp.route('/add-credit-invoice',methods=['GET'])
def addCreditInvoice():
    invoice_id = request.args.get('invoice_id')
    credit = request.args.get('new_credit')
    status = updateCredit(current_user.uuid, invoice_id, credit)
    if status:
        return json.dumps(invoice_id + " added credit")
    else:
        return json.dumps('Could not add debit to invoice account. Please contact the system administator')


@account_bp.route('/all-invoices/<c_option>/<r_option>/<focus>/<order>/<start>/<range>',methods=['GET'])
def allInvoices(c_option, r_option, focus, order, start, range):
    invoices = getAllInvoices(current_user.uuid, c_option,
            r_option, focus, order, start, range)
    for i in invoices:
        for o in i:
            if isinstance(i[o], datetime2.datetime):
                d = datetime.strptime(i[o].__str__(), '%Y-%m-%d %H:%M:%S')
                date = d.strftime('%d.%m.%Y')
                i[o] = date
    return render_template('account_bp/all_invoices.html',
            invoices_json = json.dumps(invoices))



@account_bp.route('/check-r-option',methods=['GET'])
def checkR():
    c_option = request.args.get('c_option')
    r_option = queryR(current_user.uuid, c_option)
    return json.dumps({'c_option': c_option, 'r_option' : r_option})






