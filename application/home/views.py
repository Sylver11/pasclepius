from flask import Blueprint, render_template, request, redirect, url_for
from application.db_users import addPractice, mergeUserPractice, getPractice, removeEntry
from flask_login import current_user, login_required
import subprocess
import os

home_bp = Blueprint('home_bp',__name__, template_folder='templates')

@home_bp.route('/', methods=('GET', 'POST'))
def home():
    return render_template('home/index.html', page_title = 'PANAM - Medical Software')


@home_bp.route('/setup', methods=('GET','POST'))
@login_required
def setup():
    if request.method == 'POST':
        status = addPractice(current_user.id, request.form)
        if status:
            practice = getPractice(current_user.id)
            if practice is None:
                return render_template('home/setup.html', page_title = 'Setup your account')
            mergeUserPractice(practice['practice_uuid'],
                practice['practice_name'],
                current_user.uuid,
                current_user.id,
                current_user.first_name,
                'admin')
            try:
                subprocess.call([os.getenv('SYSTEM_BASH'),
                    os.getenv("APP_URL") + "/bin/add_user.sh",
                    os.getenv("PHP"),
                    os.getenv("OC_DIR"),
                    str(current_user.id),
                    current_user.uuid,
                    current_user.first_name,
                    practice['practice_uuid']])
            except:
                status = removeEntry(practice['practice_uuid'],
                        'practice_uuid', 'practices')
                status = removeEntry(practice['practice_uuid'],
                        'practice_uuid', 'practice_connections')
                return render_template('home/setup.html', page_title = 'Setup your account')
            try:
                subprocess.call([os.getenv('SYSTEM_BASH'), os.getenv('APP_URL') + '/bin/add_shared_dir.sh',
                    os.getenv('PHP'),
                    os.getenv('OC_DIR'),
                    practice['practice_name'],
                    practice['practice_uuid'],
                    str(practice['id'])])
                return redirect(url_for('home_bp.home'))
            except:
                status = removeEntry(practice['practice_uuid'],
                        'practice_uuid', 'practices')
                status = removeEntry(practice['practice_uuid'],
                        'practice_uuid', 'practice_connections')
                return render_template('home/setup.html', page_title = 'Setup your account')
    return render_template('home/setup.html', page_title = 'Setup your account')

