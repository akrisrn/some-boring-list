from flask import Blueprint, render_template

sbl_index = Blueprint('sbl_index', __name__)


@sbl_index.route('/')
def index():
    return render_template("index.html")
