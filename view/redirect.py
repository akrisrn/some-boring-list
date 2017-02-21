from flask import Blueprint, render_template, send_from_directory

from util.db import get_nav
from util.util import static_path

sbl_redirect = Blueprint('sbl_redirect', __name__)


@sbl_redirect.route('/favicon.ico')
def favicon():
    return send_from_directory(static_path(sbl_redirect), "favicon.ico")


@sbl_redirect.route('/life-game')
def life_game():
    return render_template("life-game.html", nav=get_nav())
