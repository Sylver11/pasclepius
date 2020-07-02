from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import os

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.refresh_view = 'freshLogin'
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
  #  SECRET_KEY =  os.getenv("SECRET_KEY")
)

    with application.app_context():
        from . import views
        from .account import views
        application.register_blueprint(views.account_bp, url_prefix='/account')
        from .profile import views
        application.register_blueprint(views.profile_bp, url_prefix='/profile')
        return application

