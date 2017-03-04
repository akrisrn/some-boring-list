from os.path import join

from flask import Blueprint
from markdown import markdown
from pymdownx import extra, github, mark, caret

from settings import SBL_VERSION


def md(text):
    return markdown(text, extensions=[
        extra.ExtraExtension(),
        github.GithubExtension(),
        mark.makeExtension(),
        caret.makeExtension(),
        'markdown.extensions.toc'
    ])


def auth(session, password):
    if session.get('password') == password:
        return True
    else:
        return False


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
