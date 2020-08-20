from flask import Blueprint, render_template, request, redirect, url_for
#from application.forms import PracticeForm
from application.db_users import addPractice, mergeUserPractice, getPractice
from flask_login import current_user, login_required

home_bp = Blueprint('home_bp',__name__, template_folder='templates')

@home_bp.route('/', methods=('GET', 'POST'))
def home():
    return render_template('home/index.html', page_title = 'PANAM - Medical Software')


@home_bp.route('/setup', methods=('GET','POST'))
@login_required
def setup():
    ######### TODO This needs attention. If succesfully write practice to db
    ########## but fails to get the practice uuid or update the user profile
    ######### no way of fixing that on the front end
    if request.method == 'POST':
        status = addPractice(current_user.id, request.form)
        if status:
            practice = getPractice(current_user.id)
            mergeUserPractice(practice['practice_uuid'],
                    practice['practice_name'],
                    current_user.uuid,
                    current_user.id,
                    current_user.first_name,
                    'admin')
            return redirect(url_for('home_bp.home')) 
    return render_template('home/setup.html', page_title = 'Setup your account')

