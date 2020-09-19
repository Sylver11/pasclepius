from flask import Flask
from flask_login import LoginManager
import os

login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'
login_manager.refresh_view = 'auth_bp.freshLogin'

from application.models import User
from application.db_users import checkUser, getPractice

@login_manager.user_loader
def load_user(id):
    data = checkUser(id)
    if data:
        practice = getPractice(practice_uuid = data['current_practice_uuid'])
        if practice:
            return User(id,
                    data["first_name"],
                    data["uuid_text"],
                    data["current_practice_uuid"],
                    practice['practice_name'],
                    practice['id'],
                    practice['practice_admin'],
                    practice['invoice_layout'],
                    practice['namaf_profession'],
                    data['current_practice_role'])
        return User(id, data['first_name'], data['uuid_text'])


def create_app():
    application = Flask(__name__)
    application.secret_key = os.getenv("SECRET_KEY")
    application.config['SESSION_TYPE'] = 'filesystem'
    application.config['REMEMBER_COOKIE_DURATION'] = 2592000
    application.config.update(
)
    login_manager.init_app(application)

    with application.app_context():
        from .home import views
        application.register_blueprint(views.home_bp)
        from .api import views
        application.register_blueprint(views.api_bp)
        from .account import views
        application.register_blueprint(views.account_bp, url_prefix='/account')
        from .profile import views
        application.register_blueprint(views.profile_bp, url_prefix='/profile')
        from .patient import views
        application.register_blueprint(views.patient_bp, url_prefix='/patient')
        from .auth import views
        application.register_blueprint(views.auth_bp, url_prefix='/auth')
        return application

