from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    """Initialize the core application."""
    load_dotenv()
    application = Flask(__name__)
    application.secret_key = "hellllllll"
    #os.getenv("SECRET_KEY")
   # application.config['SESSION_TYPE'] = 'filesystem'
    application.config.update(
    #Set the secret key to a sufficiently random value
  #  SECRET_KEY =  os.getenv("SECRET_KEY")
)

    with application.app_context():
        from . import forms
        from . import db_utils
        from . import database_io
        from . import views
        from . import url_generator
        from . import database_invoice
        return application

