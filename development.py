from application import create_app
from dotenv import load_dotenv
import os

load_dotenv()
application = create_app()

if __name__ == '__main__':
    application.secret_key = os.getenv("SECRET_KEY")
    application.config['SESSION_TYPE'] = 'filesystem'
    application.config['LOGIN_DISABLED'] = True
    application.run(host='0.0.0.0', port =4003, debug=True, threaded=True)
