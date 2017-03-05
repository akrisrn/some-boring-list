from functools import wraps
from os.path import join

from flask import Blueprint, session, redirect, url_for, request
from markdown import markdown
from pymdownx import extra, github, mark, caret

from config import SBL_PASSWORD, SBL_VERSION


def md(text):
    return markdown(text, extensions=[
        extra.ExtraExtension(),
        github.GithubExtension(),
        mark.makeExtension(),
        caret.makeExtension(),
        'markdown.extensions.toc'
    ])


def logged():
    if session.get('password') == SBL_PASSWORD:
        return True
    else:
        return False


def auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if logged():
            return func(*args, **kwargs)
        else:
            return redirect(url_for('sbl_login.login', ref=request.url))

    return wrapper


def static_path(app, *path):
    if isinstance(app, Blueprint):
        return join(app.root_path, '../static', *path)
    else:
        return join(app.root_path, 'static', *path)


def version(url):
    return "%s?v=%s" % (url, SBL_VERSION)


def cdn(name):
    if name == "jquery":
        return "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"
    elif name == "jquery-raty":
        return "https://cdnjs.cloudflare.com/ajax/libs/raty/2.7.1/jquery.raty.min.js"
    elif name == "jquery-raty-css":
        return "https://cdnjs.cloudflare.com/ajax/libs/raty/2.7.1/jquery.raty.min.css"
    elif name == "pace":
        return "https://cdnjs.cloudflare.com/ajax/libs/pace/1.0.2/pace.min.js"
    elif name == "pace-css":
        return "https://cdnjs.cloudflare.com/ajax/libs/pace/1.0.2/themes/blue/pace-theme-flash.min.css"
    elif name == "github-markdown-css":
        return "https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/2.4.1/github-markdown.min.css"
