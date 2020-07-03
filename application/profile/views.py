from flask import Blueprint, render_template, Response, request, session, redirect, url_for, send_file, flash
from flask_login import current_user, login_required, fresh_login_required
from application.db_users import checkUser, updateUserLayout, updateUserPassword, updateUserPersonal, updateUserPractice, updateUserBanking
from application.forms import updateBankingForm, updatePracticeForm, updatePasswordForm, updatePersonalForm,  updateLayoutForm


profile_bp = Blueprint('profile_bp',__name__, template_folder='templates')



@profile_bp.route('/reset-password', methods=('GET', 'POST'))
@fresh_login_required
def resetPassword():
    form_password = updatePasswordForm()
    if request.method == 'POST' and form_password.validate():
        password = Password()
        hashed_password = password.set_password(form_password.password.data)
        status =  updateUserPassword(current_user.id, hashed_password)
        if status:
            flash('Password changed succesfully')
    return render_template('profile/reset_password.html', form_password=form_password,
            page_title = 'Change password')


@profile_bp.route('/reset-personal', methods=('GET', 'POST'))
@login_required
def resetPersonal():
    data = checkUser(current_user.id)
    form_personal = updatePersonalForm()
    if request.method == 'POST' and form_personal.validate():
        status = updateUserPersonal(current_user.id, form_personal.first_name.data,
                form_personal.second_name.data, form_personal.cell.data,
                form_personal.pob.data, form_personal.city.data,
                form_personal.country.data, form_personal.qualification.data,
                form_personal.title.data, form_personal.phone.data,
                form_personal.fax.data, form_personal.specialisation.data)
        if status:
            flash('Personal data updated')
    return render_template('profile/reset_personal.html',
            form_personal = form_personal,
            title = data['title'],
            first_name = data['first_name'],
            second_name = data['second_name'],
            phone = data['phone'],
            cell = data['cell'],
            fax = data['fax'],
            pob = data['pob'],
            city = data['city'],
            country = data['country'],
            qualification = data['qualification'],
            specialisation = data['specialisation'],
            page_title = 'Change personal')


@profile_bp.route('/reset-practice', methods=('GET', 'POST'))
@login_required
def resetPractice():
    data = checkUser(current_user.id)
    form_practice = updatePracticeForm()
    if request.method == 'POST' and form_practice.validate():
        status = updateUserPractice(current_user.id,
                form_practice.practice_name.data,
                form_practice.practice_number.data,
                form_practice.hpcna_number.data)
        if status:
            flash('Practice data updated')
    return render_template('profile/reset_practice.html',
            form_practice = form_practice,
            practice_name = data['practice_name'],
            practice_number = data['practice_number'],
            hpcna_number = data['hpcna_number'],
            page_title = 'Change practice info')


@profile_bp.route('/reset-banking', methods=('GET', 'POST'))
@login_required
def resetBanking():
    data = checkUser(current_user.id)
    form_banking = updateBankingForm()
    if request.method == 'POST' and form_banking.validate():
        status = updateUserBanking(current_user.id,
                form_banking.bank_holder.data,
                form_banking.bank_account.data,
                form_banking.bank_branch.data,
                form_banking.bank.data)
        if status:
            flash('Banking data updated')
    return render_template('profile/reset_banking.html',
            form_banking = form_banking,
            bank_holder = data['bank_holder'],
            bank_account = data['bank_account'],
            bank_branch = data['bank_branch'],
            bank = data['bank'],
            page_title = 'Change banking info')


@profile_bp.route('/reset-layout', methods=('GET', 'POST'))
@login_required
def resetLayout():
    data = checkUser(current_user.id)
    layout_code = data['invoice_layout']
    form_layout = updateLayoutForm()
    if request.method == 'POST' and form_layout.validate():
        status = updateUserLayout(current_user.id,
               form_layout.phone.data,
               form_layout.fax.data,
               form_layout.hospital.data,
               form_layout.diagnosis.data)
        if status:
           flash('Invoice Layout updated')
    return render_template('profile/reset_layout.html',
            form_layout = form_layout,
            layout_code = layout_code,
            page_title = 'Change Invoice Layout')
