#!/Users/justus/Code/personal/pasclepius/env/bin/python3
#import sys
#import os

#python_home = os.getenv('PYTHON_HOME')

#activator = python_home + '/bin/activate_this.py'
#with open(activator) as f:
#    exec(f.read(), {'__file__': activator})

#sys.path.insert(0, os.getenv("APP_URL"))
#sys.path.append(os.getenv('PYTHON_LIB'))

from application import create_app
application = create_app()

if __name__ == '__main__':
    application.secret_key = os.getenv("SECRET_KEY")
    application.config['SESSION_TYPE'] = 'filesystem'
    application.run(host='0.0.0.0', port =4003, debug=True, threaded=True)
