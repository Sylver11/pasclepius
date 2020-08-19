from flask import Blueprint, render_template, Response, request, session, redirect, url_for, send_file, flash
from flask_login import current_user, login_required, fresh_login_required
from application.db_users import checkUser, checkConnections, getAssistants, addUser, updateUser, getPractice, updateInvoice, updateUser, updatePractice, mergeUserPractice
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
    if request.method == 'POST':
        status = updateUser(current_user.id,
                first_name = request.form['first_name'],
                second_name = request.form['second_name'])
        if status:
            return json.dumps("success")
    user = checkUser(current_user.id)
    return render_template('profile/personal.html', user = user)


@profile_bp.route('/practice', methods=('GET', 'POST'))
@login_required
def resetPractice():
    practice = ''
    if current_user.practice_role =='assistant':
        if request.method == 'POST':
            updateUser(current_user.id,
                    current_practice_uuid = request.form['practice_uuid'],
                    current_practice_role = 'assistant')
            return json.dumps("success")
        else:
            practice = checkConnections(current_user.uuid)

    elif(current_user.practice_role == 'admin'):
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
        else:
            practice = getPractice(practice_uuid = current_user.practice_uuid)

    return render_template('profile/practice.html',
            practice = practice)


@profile_bp.route('/invoice', methods=('GET', 'POST'))
@login_required
def resetLayout():
    practice = getPractice(practice_uuid = current_user.practice_uuid)
    layout_code = practice['invoice_layout']
    if request.method == 'POST':
        status = updateInvoice(current_user.practice_uuid,
               request.form.get('phone'),
               request.form.get('fax'),
               request.form.get('hospital'),
               request.form.get('diagnosis'))
        if status:
            return json.dumps("success")
    return render_template('profile/invoice.html',
            layout_code = layout_code)


@profile_bp.route('/assistant', methods=('GET', 'POST'))
def assistant():
    if current_user.practice_role !='admin':
        return 'Unauthorised'
    if request.method == 'POST':
        newUser = checkUser(request.form['email']) 
        if not newUser:
            addUser(request.form['first_name'],
                request.form['second_name'],
                request.form['email'])
        newUser = checkUser(request.form['email']) 
        mergeUserPractice(current_user.practice_uuid,
            current_user.practice_name,
            newUser['uuid_text'],
            newUser['email'],
            newUser['first_name'],
            'assistant')
        return json.dumps("success")
    assistants = getAssistants(current_user.practice_uuid)
    return render_template('profile/assistant.html', assistants = assistants)


@profile_bp.route('/select', methods=('GET', 'POST'))
def select():
    if current_user.practice_role !='assistant':
        return 'Unauthorised'

    if request.method == 'POST':
        status = addUser(request.form['first_name'],
                request.form['second_name'],
                request.form['email'])
        newUser = checkUser(request.form['email']) 
        mergeUserPractice(current_user.practice_uuid,
            current_user.practice_name,
            newUser['uuid_text'],
            'assistant')
        if status:
            return json.dumps("success")

    available_practices = checkConnections(current_user.uuid)
    print(available_practices)
    return render_template('profile/select.html', available_practices =
            available_practices)

