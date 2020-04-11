from flask import Flask, render_template, Response, request, session
from jinja2 import Template
from forms import Sample


app = Flask(__name__)




@app.route('/', methods=('GET', 'POST'))
def contact():
    form = Sample()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port =4003, debug=True, threaded=True)
