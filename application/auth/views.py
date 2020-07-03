from flask import Blueprint, render_template, Response, request, session, redirect, url_for, flash
from application.forms import RegistrationForm, LoginForm
from application.db_users import addUser,checkUser
from flask_login import current_user, login_user, logout_user, login_required
from application.models import User, Password
from werkzeug.urls import url_parse

auth_bp = Blueprint('auth_bp',__name__, template_folder='templates')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.email.data, form.first_name.data)
        password = user.set_password(form.password.data)
        status = addUser(form.title.data, form.first_name.data,
                         form.second_name.data,
                         form.email.data, password,
                         form.phone.data, form.cell.data,
                         form.fax.data, form.pob.data,
                         form.city.data, form.country.data,
                         form.bank_holder.data, form.bank_account.data,
                         form.bank.data, form.bank_branch.data,
                         form.practice_number.data, form.practice_name.data,
                         form.hpcna_number.data, form.qualification.data,
                         form.specialisation.data)
        if status:
            return redirect(url_for('auth_bp.login'))
    return render_template('auth/register.html', form=form, page_title = 'Register')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))
    if form.validate_on_submit():
        data = checkUser(form.email.data)
        user = User(form.email.data)
        if data is None or not user.check_password(data['password'], form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth_bp.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home_bp.home')
        return redirect(next_page)
    return render_template('auth/login.html', form=form, page_title = 'Login')


@auth_bp.route('/fresh-login', methods=['GET', 'POST'])
def freshLogin():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        data = checkUser(form.email.data)
        user = User(form.email.data)
        if data is None or not user.check_password(data['password'], form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth_bp.login'))
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home_bp.home')
        return redirect(next_page)
    return render_template('auth/login.html', form=form, page_title = 'Fresh login')


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth_bp.login'))
