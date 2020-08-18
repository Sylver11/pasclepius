from flask import Blueprint, render_template, Response, request, session, redirect, url_for, send_file, flash
from flask_login import current_user, login_required, fresh_login_required
from application.db_users import checkUser, getPractice, updateInvoice, updateUser, updatePractice
from application.forms import PracticeForm,  UserForm, InvoiceForm
import json

profile_bp = Blueprint('profile_bp',__name__, template_folder='templates')



@profile_bp.route('/')
@fresh_login_required
def base():
    return render_template('profile/base.html', 
            page_title = 'Edit Profile')


@profile_bp.route('/personal', methods=('GET', 'POST'))
@login_required
def resetPersonal():
    data = checkUser(current_user.id)
    form_personal = UserForm()
    if request.method == 'POST' and form_personal.validate():
        status = updateUser(current_user.id, form_personal.first_name.data,
                form_personal.second_name.data)
        if status:
            flash('Personal data updated')
    return render_template('profile/personal.html',
           form_personal = form_personal,
                first_name = data['first_name'],
                second_name = data['second_name'],
                page_title = 'Change personal')


@profile_bp.route('/practice', methods=('GET', 'POST'))
@login_required
def resetPractice():
    practice = getPractice(practice_uuid = current_user.practice_uuid)
    form_practice = PracticeForm()
    if request.method == 'POST':
        status = updatePractice(current_user.practice_uuid,
                request.form.get('practice_email'),
                request.form.get('practice_name'),
                request.form.get('practice_number'),
                request.form.get('hpcna_number'),
                request.form.get('cell'),
                request.form.get('pob'),
                request.form.get('city'),
                request.form.get('country'),
                request.form.get('qualification'),
                request.form.get('phone'),
                request.form.get('fax'),
                request.form.get('specialisation'),
                request.form.get('bank_holder'),
                request.form.get('bank_account'),
                request.form.get('bank_branch'),
                request.form.get('bank'))
        if status:
            return json.dumps("success")
    return render_template('profile/practice.html',
            form_practice = form_practice,
            practice_email = practice['practice_email'],
            practice_name = practice['practice_name'],
            practice_number = practice['practice_number'],
            hpcna_number = practice['hpcna_number'],
            bank_account = practice['bank_account'],
            bank_holder = practice['bank_holder'],
            bank_branch = practice['bank_branch'],
            bank = practice['bank'],
            phone = practice['phone'],
            cell = practice['cell'],
            fax = practice['fax'],
            pob = practice['pob'],
            city = practice['city'],
            country = practice['country'],
            qualification = practice['qualification'],
            specialisation = practice['specialisation'],
            page_title = 'Change practice info')


@profile_bp.route('/invoice', methods=('GET', 'POST'))
@login_required
def resetLayout():
    practice = getPractice(practice_uuid = current_user.practice_uuid)
    layout_code = practice['invoice_layout']
    form_layout = InvoiceForm()
    if request.method == 'POST' and form_layout.validate():
        status = updateInvoice(current_user.id,
               form_layout.phone.data,
               form_layout.fax.data,
               form_layout.hospital.data,
               form_layout.diagnosis.data)
        if status:
           flash('Invoice Layout updated')
    return render_template('profile/invoice.html',
            form_layout = form_layout,
            layout_code = layout_code,
            page_title = 'Change Invoice Layout')
