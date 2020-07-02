from flask import Blueprint, render_template

home_bp = Blueprint('home_bp',__name__)

@home_bp.route('/', methods=('GET', 'POST'))
def home():
    return render_template('index.html', page_title = 'PANAM - Medical Software')
