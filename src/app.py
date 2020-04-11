from flask import Flask, render_template, Response, request, session


app = Flask(__name__)




@app.route('/')
def hello():
    return 'Justus helllloo'

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port =4003, debug=True, threaded=True)
