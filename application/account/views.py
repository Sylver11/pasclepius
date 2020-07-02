from flask import Blueprint, render_template
from flask_login import current_user, login_required
account_bp = Blueprint('account_bp',__name__,template_folder='templates')


@account_bp.route("/", methods=['GET'])
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
