from flask import Flask, render_template, Response, request, session, jsonify
from jinja2 import Template
from forms import Patient, Treatment
import json

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def contact():
    form = Patient()
    #if form.validate_on_submit():
     #   if form.flist.data:
          #  for item in form.flist.data:
                    # do stuff

    return render_template('index.html', form=form)



@app.route('/patient', methods=('GET', 'POST'))
def newInvoice():
    form = Patient()
    #if form.validate_on_submit():
     #   if form.flist.data:
          #  for item in form.flist.data:
                    # do stuff

    return render_template('patient.html', form=form)



@app.route('/add-product', methods=['POST'])
def add_product():
    form = Treatment()
    if form.quantity.data:
        for item in form.quantity.data:
            newOrder = Order(qty = item)
            db.session.add(newOrder)
            db.session.commit()
        return jsonify(result='success')
    return jsonify(result='error')

@app.route('/invoice/patient/<')
def add_product_test():
    form = Treatment()
    set_choices = [('mutual', 'Mutual'),('personal#1', 'Personal #1'),('personal#2', 'Personal #2')]
    #[(set.id, set.friendly_name)
    #for set in Set.query.order_by(Set.friendly_name).all()]
    return render_template('index.html', form=form, set_choices=set_choices)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port =4003, debug=True, threaded=True)
