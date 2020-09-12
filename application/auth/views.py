from flask import Blueprint, render_template, request, redirect, url_for, flash
from application.db_users import addUser,checkUser
from flask_login import current_user, login_user, logout_user, login_required
from application.models import User
import requests
import os
import json
from oauthlib.oauth2 import WebApplicationClient

client = WebApplicationClient(os.getenv("GOOGLE_CLIENT_ID"))


auth_bp = Blueprint('auth_bp',__name__, template_folder='templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))
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
        users_name = userinfo_response.json()["given_name"]
        users_surname = userinfo_response.json()["family_name"]
        if checkUser(users_email) is None:
            status = addUser(users_name, users_surname, users_email)
            if not status :
                flash('You do not have an account with us and we were not able to create one for you. Please contact the system administrator')
                return redirect(url_for('auth_bp.login'))
            user = User(users_email)
            login_user(user, remember=True)
            return redirect(url_for('home_bp.setup'))
        user = User(users_email)
        login_user(user, remember=True)
        return redirect(url_for('home_bp.home'))

    else:
        flash('Your Google account is not verified.')
        return redirect(url_for('auth_bp.login'))


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth_bp.login'))
