from flask import Blueprint, render_template, redirect, url_for, request, session

from settings import SBL_PASSWORD
from util.util import auth

sbl_login = Blueprint('sbl_login', __name__)


@sbl_login.route('/login', methods=['POST', 'GET'])
def login():
    if auth(session, SBL_PASSWORD):
        return redirect(url_for('sbl_index.index'))
    error = False
    if request.method == 'POST':
        if request.form['password'] == SBL_PASSWORD:
            session['password'] = SBL_PASSWORD
            return redirect(url_for('sbl_index.index'))
        else:
            error = True
    return render_template('login.html', error=error)


@sbl_login.route('/logout')
def logout():
    session.pop('password', None)
    return redirect(url_for('sbl_index.index'))
