from re import sub

from flask import Blueprint, render_template, session, abort, request, redirect, url_for

from settings import SBL_BLOG_NAME, SBL_BLOG_DES, SBL_PASSWORD, SBL_BLOG_SECRET_TAG
from util.db import get_nav, get_blog, get_post, add_post, edit_post
from util.util import md, auth

sbl_blog = Blueprint('sbl_blog', __name__)


@sbl_blog.route('/')
@sbl_blog.route('/tag/<string:tag>')
def index(tag=None):
    editable = auth(session, SBL_PASSWORD)
    if not editable and tag == SBL_BLOG_SECRET_TAG:
        abort(404)
    blog = get_blog(tag)
    if not blog:
        abort(404)
    return render_template('blog/index.html', name=SBL_BLOG_NAME, des=SBL_BLOG_DES,
                           secret_tag=SBL_BLOG_SECRET_TAG, blog=blog, tag=tag, editable=editable, nav=get_nav())


@sbl_blog.route('/post/<int:post_id>')
def post_show(post_id):
    editable = auth(session, SBL_PASSWORD)
    post = get_post(post_id)
    if not post:
        abort(404)
    if not editable and post[5].find(SBL_BLOG_SECRET_TAG) != -1:
        abort(404)
    content = post[2].replace("\r", "\n")
    if not editable:
        content = sub("\s?/\*[\s\S]*\*/s?", "", content)
    content = md(content)
    post = list(post)
    post.pop(2)
    post.append(content)
    return render_template('blog/post.html', post=post, editable=editable, nav=get_nav())


@sbl_blog.route('/add', methods=['POST', 'GET'])
def add():
    if auth(session, SBL_PASSWORD):
        if request.method == 'POST':
            title = request.form["title"]
            updDate = addDate = request.form["addDate"]
            tag = request.form["tag"].replace(" ", "")
            content = request.form["content"]
            add_post(title, content, addDate, updDate, tag)
            return redirect(url_for('.index'))
        return render_template('blog/add.html', nav=get_nav())
    else:
        return redirect(url_for('sbl_login.login'))


@sbl_blog.route('/edit/<int:post_id>', methods=['POST', 'GET'])
def edit(post_id):
    if auth(session, SBL_PASSWORD):
        if request.method == 'POST':
            title = request.form["title"]
            addDate = request.form["addDate"]
            updDate = request.form["updDate"]
            tag = request.form["tag"].replace(" ", "")
            content = request.form["content"]
            edit_post(post_id, title, content, addDate, updDate, tag)
            return redirect(url_for('.post_show', post_id=post_id))
        post = get_post(post_id)
        if not post:
            abort(404)
        return render_template('blog/edit.html', post=post, nav=get_nav())
    else:
        return redirect(url_for('sbl_login.login'))
