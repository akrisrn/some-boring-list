from flask import Blueprint, render_template, redirect, url_for, request, session

from config import SBL_PASSWORD
from util.util import logged

sbl_login = Blueprint('sbl_login', __name__)


@sbl_login.route('/login/', methods=['POST', 'GET'])
def login():
    referrer = request.referrer
    if not referrer or referrer.split('/')[-1] == url_for(".login")[1:]:
        referrer = ""
    if logged():
        if referrer:
            return redirect(referrer)
        else:
            return redirect(url_for('sbl_index.index'))
    error = False
    if request.method == 'POST':
        referrer = request.form['referrer']
        if not referrer:
            referrer = request.args.get('ref')
        if request.form['password'] == SBL_PASSWORD:
            session['password'] = SBL_PASSWORD
            if referrer:
                return redirect(referrer)
            else:
                return redirect(url_for('sbl_index.index'))
        else:
            error = True
    return render_template('login.html', referrer=referrer, error=error)


@sbl_login.route('/logout/')
def logout():
    session.pop('password', None)
    referrer = request.referrer
    if referrer:
        return redirect(referrer)
    else:
        return redirect(url_for('sbl_index.index'))
