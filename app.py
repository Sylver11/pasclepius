from flask import Flask, render_template, Response, request, session, jsonify
from jinja2 import Template
from forms import Sample, addTreatment, ExpensesForm, MyForm, NewOrderForm
import json

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def contact():
    form = Sample()
    #if form.validate_on_submit():
     #   if form.flist.data:
          #  for item in form.flist.data:
                    # do stuff

    return render_template('index.html', form=form)


@app.route('/add-product', methods=['POST'])
def add_product():
    form = NewOrderForm()
    if form.quantity.data:
        for item in form.quantity.data:
            newOrder = Order(qty = item)
            db.session.add(newOrder)
            db.session.commit()
        return jsonify(result='success')
    return jsonify(result='error')

@app.route('/add-product-test')
def add_product_test():
    form = NewOrderForm()
    set_choices = [(set.id, set.friendly_name)
    for set in Set.query.order_by(Set.friendly_name).all()]
    return render_template('index.html', form=form, set_choices=set_choices)

@app.route("/newqualification/<welder_id>", methods=['GET', 'POST'])
def newqualification(welder_id=None):
    form = MyForm()

        #writemethod.

    return render_template('index.html', title='xyz', form=form)

@app.route("/modifywps", methods=['POST', 'GET'])
def modifywps():
    application_standard_id = request.args.get('std') # gets value from the getJson()

   # process it however you want.. 

    return


@app.route('/add-treatment',methods=('GET','POST'))
def adding():
    response = request.get_json()
    print(response)
    a,b,c = [response[k] for k in ('a', 'b','c')]
    message = response.values()
    addTreatment(response)
    print(a)
    return jsonify(response)
  #  addTreatment(key)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port =4003, debug=True, threaded=True)
