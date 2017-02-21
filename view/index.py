from flask import Blueprint, render_template

from util.db import get_nav

sbl_index = Blueprint('sbl_index', __name__)


@sbl_index.route('/')
def index():
    return render_template("index.html", nav=get_nav())
