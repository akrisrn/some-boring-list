from datetime import datetime
from re import sub

from flask import Blueprint, render_template, abort, request, redirect, url_for

from config import SBL_BLOG_SECRET_TAG
from util.db import get_blog, get_post, add_post, edit_post
from util.util import md, logged, auth

sbl_blog = Blueprint('sbl_blog', __name__)


@sbl_blog.route('/')
@sbl_blog.route('/date/<int:year>/')
@sbl_blog.route('/date/<int:year>/<string:month>/')
@sbl_blog.route('/tag/<string:tag>/')
@sbl_blog.route('/date/<int:year>/tag/<string:tag>/')
@sbl_blog.route('/date/<int:year>/<string:month>/tag/<string:tag>/')
def index(year=None, month=None, tag=None):
    editable = logged()
    if not editable and tag == SBL_BLOG_SECRET_TAG:
        abort(404)
    if not tag and not year:
        year = datetime.now().year
    if month and month not in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
        abort(404)
    blog = get_blog(year, month, tag)
    if not blog:
        abort(404)
    return render_template('blog/index.html', secret_tag=SBL_BLOG_SECRET_TAG, blog=blog,
                           year=year, month=month, tag=tag, editable=editable)


@sbl_blog.route('/post/<int:post_id>/')
def post_show(post_id):
    editable = logged()
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
    return render_template('blog/post.html', post=post, editable=editable)


@sbl_blog.route('/add/', methods=['POST', 'GET'])
@auth
def add():
    if request.method == 'POST':
        title = request.form["title"]
        updDate = addDate = request.form["addDate"]
        tag = request.form["tag"].replace(" ", "")
        content = request.form["content"]
        add_post(title, content, addDate, updDate, tag)
        return redirect(url_for('.index'))
    return render_template('blog/add.html')


@sbl_blog.route('/edit/<int:post_id>/', methods=['POST', 'GET'])
@auth
def edit(post_id):
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
    return render_template('blog/edit.html', post=post)
