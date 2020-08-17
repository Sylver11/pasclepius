from flask import Blueprint, render_template, Response, request, session, redirect, url_for, flash
from application.forms import RegistrationForm, LoginForm
from application.db_users import addUser,checkUser
from flask_login import current_user, login_user, logout_user, login_required
from application.models import User, Password
from werkzeug.urls import url_parse
import requests
import os
import json
from oauthlib.oauth2 import WebApplicationClient
client = WebApplicationClient(os.getenv("GOOGLE_CLIENT_ID"))


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
    #form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))
    #if form.validate_on_submit():
    #    data = checkUser(form.email.data)
    #    user = User(form.email.data)
    #    if data is None or not user.check_password(data['password'], form.password.data):
    #        flash('Invalid username or password')
    #        return redirect(url_for('auth_bp.login'))
    #    login_user(user, remember=form.remember_me.data)
    #    next_page = request.args.get('next')
    #    if not next_page or url_parse(next_page).netloc != '':
    #        next_page = url_for('home_bp.home')
    #    return redirect(next_page)
    return render_template('auth/login.html', page_title = 'Login')

def get_google_provider_cfg():
    return requests.get("https://accounts.google.com/.well-known/openid-configuration").json()

@auth_bp.route("/login/google")
def loginGoogle():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@auth_bp.route("/login/google/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code)

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(os.getenv('GOOGLE_CLIENT_ID'), os.getenv('GOOGLE_CLIENT_SECRET')),)

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
        if checkUser(users_email) is None:
            flash('You do not have an account with us. To use the application you need to register first.')
            return redirect(url_for('auth_bp.login'))
        user = User(users_email)
        login_user(user, remember=True)
        return redirect(url_for('home_bp.home'))

    else:
        flash('Your Google account is not verified.')
        return redirect(url_for('auth_bp.login'))


#@auth_bp.route('/fresh-login', methods=['GET', 'POST'])
#def freshLogin():
#    form = LoginForm(request.form)
#    if form.validate_on_submit():
#        data = checkUser(form.email.data)
#        user = User(form.email.data)
#        if data is None or not user.check_password(data['password'], form.password.data):
#            flash('Invalid username or password')
#            return redirect(url_for('auth_bp.login'))
#        login_user(user, remember=True)
#        next_page = request.args.get('next')
#if not next_page or url_parse(next_page).netloc != '':
#            next_page = url_for('home_bp.home')
#        return redirect(next_page)
#    return render_template('auth/login.html', form=form, page_title = 'Fresh login')


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth_bp.login'))
