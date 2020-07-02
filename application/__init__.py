from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import os

login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'
login_manager.refresh_view = 'auth_bp.freshLogin'
#from application.models import User
#from application.database_users import checkUser

#@login_manager.user_loader
#def load_user(id):
#    data = checkUser(id)
#    if data:
#        return User(id, data["first_name"], data["uuid_text"])


def create_app():
    load_dotenv()
    application = Flask(__name__)
    login_manager.init_app(application)
    application.secret_key = os.getenv("SECRET_KEY")
    application.config['SESSION_TYPE'] = 'filesystem'
    application.config.update(
)

    with application.app_context():
       # from . import views
        from .home import views
        application.register_blueprint(views.home_bp, url_prefix='/')
        from .api import views
        application.register_blueprint(views.api_bp, url_prefix='/')
        from .account import views
        application.register_blueprint(views.account_bp, url_prefix='/account')
        from .profile import views
        application.register_blueprint(views.profile_bp, url_prefix='/profile')
        from .patient import views
        application.register_blueprint(views.patient_bp, url_prefix='/patient')
        from .auth import views
        application.register_blueprint(views.auth_bp, url_prefix='/auth')
        return application

