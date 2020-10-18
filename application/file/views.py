from flask import Blueprint, render_template
from flask_login import login_required

file_bp = Blueprint('file_bp' ,__name__, template_folder='templates')

@file_bp.route('', methods=('GET', 'POST'))
@login_required
def nextcloud():
    return render_template('file/base.html')
