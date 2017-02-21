from flask import Flask, render_template

from settings import SECRET_KEY, DEBUG
from util.db import get_nav
from util.util import version
from view.blog import sbl_blog
from view.index import sbl_index
from view.list import sbl_list
from view.login import sbl_login
from view.redirect import sbl_redirect

app = Flask(__name__)
app.register_blueprint(sbl_index)
app.register_blueprint(sbl_list, url_prefix='/list')
app.register_blueprint(sbl_blog, url_prefix='/blog')
app.register_blueprint(sbl_login)
app.register_blueprint(sbl_redirect)
app.jinja_env.filters['version'] = version

app.secret_key = SECRET_KEY
app.debug = DEBUG


@app.errorhandler(404)
def error_page(error):
    return render_template('error.html', error=error, nav=get_nav()), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')
