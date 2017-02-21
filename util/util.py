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
