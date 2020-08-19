from flask import Blueprint, render_template, request, redirect, url_for
from application.forms import PracticeForm
from application.db_users import addPractice, mergeUserPractice, getPractice
from flask_login import current_user, login_required

home_bp = Blueprint('home_bp',__name__, template_folder='templates')

@home_bp.route('/', methods=('GET', 'POST'))
def home():
    return render_template('home/index.html', page_title = 'PANAM - Medical Software')


@home_bp.route('/setup', methods=('GET','POST'))
@login_required
def setup():
    form = PracticeForm()
    ######### TODO This needs attention. If succesfully write practice to db
    ########## but fails to get the practice uuid or update the user profile
    ######### no way of fixing that on the front end
    if request.method == 'POST' and form.validate():
        status = addPractice(current_user.id,
                form.phone.data, form.practice_email.data, form.cell.data,
                         form.fax.data, form.pob.data,
                         form.city.data, form.country.data,
                         form.bank_holder.data, form.bank_account.data,
                         form.bank.data, form.bank_branch.data,
                         form.practice_number.data, form.practice_name.data,
                         form.hpcna_number.data, form.qualification.data,
                         form.specialisation.data)
        if status:
            practice = getPractice(current_user.id)
            mergeUserPractice(practice['practice_uuid'],
                    practice['practice_name'],
                    current_user.uuid,
                    current_user.id,
                    current_user.first_name,
                    'admin')
            return redirect(url_for('home_bp.home')) 
    return render_template('home/setup.html', form=form, page_title = 'Setup your account')

