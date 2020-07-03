from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
account_bp = Blueprint('account_bp',__name__,template_folder='templates')
from application.db_invoice import getAllInvoices, liveSearchInvoices 
import simplejson as json
from datetime import datetime
import datetime as datetime2

@account_bp.route("/", methods=['GET'])
@login_required 
def gerneral():
    invoices = getAllInvoices(current_user.uuid)
    for i in invoices:
        for o in i:
            if isinstance(i[o], datetime2.datetime):
                d = datetime.strptime(i[o].__str__(), '%Y-%m-%d %H:%M:%S')
                date = d.strftime('%d.%m.%Y')
                i[o] = date
    return render_template('account_bp/general.html',
            invoices = json.dumps(invoices))


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




@account_bp.route('/live-search-invoice',methods=['GET','POST'])
@login_required
def liveSearchTreatment():
    name = request.args.get('name')
    invoices = liveSearchInvoices(current_user.uuid, name)
    for i in invoices:
        for o in i:
            if isinstance(i[o], datetime2.datetime):
                d = datetime.strptime(i[o].__str__(), '%Y-%m-%d %H:%M:%S')
                date = d.strftime('%d.%m.%Y')
                i[o] = date
    print(json.dumps({'invoices' : invoices}))
    return json.dumps({'invoices' : invoices})

