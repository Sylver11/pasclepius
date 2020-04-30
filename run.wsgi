#!/usr/local/bin/python3
import sys
import os
sys.path.insert(0, os.getenv("APP_URL"))

from application import create_app

application = create_app()

if __name__ == '__main__':
    application.secret_key = os.getenv("SECRET_KEY")
    application.config['SESSION_TYPE'] = 'filesystem'
    application.run(host='0.0.0.0', port =4003, debug=True, threaded=True)
