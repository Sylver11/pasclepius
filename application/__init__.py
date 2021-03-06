from flask import Flask
from flask_login import LoginManager
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder
import datetime as datetime2

login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'
login_manager.refresh_view = 'auth_bp.freshLogin'

db = SQLAlchemy()

class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if type(o) == datetime2.timedelta:
            return str(o)
        elif type(o) == datetime2.datetime:
            return o.isoformat()
        else:
            return super().default(o)

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
                    data['current_practice_role'],
                    practice['practice_folder_id'])
        return User(id, data['first_name'], data['uuid_text'])


def create_app():
    application = Flask(__name__)
    CORS(application)
    application.secret_key = os.getenv("SECRET_KEY")
    application.jinja_env.globals['HTTP_MODE'] = os.getenv('HTTP_MODE')
    application.jinja_env.globals['NEXTCLOUD_DOMAIN_FULL'] = os.getenv('NEXTCLOUD_DOMAIN_FULL')
    application.jinja_env.globals['PASCLEPIUS_DOMAIN'] = os.getenv('PASCLEPIUS_DOMAIN')
    application.config['SESSION_TYPE'] = 'filesystem'
    application.config['REMEMBER_COOKIE_DURATION'] = 2592000
    application.config['CORS_HEADERS'] = 'Content-Type'
    application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_CONN_STRING")
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    application.config.update()
    application.json_encoder = CustomJSONEncoder
    login_manager.init_app(application)
    db.init_app(application)
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
        db.create_all()
        return application
