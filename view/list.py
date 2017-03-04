from datetime import datetime
from re import sub

from flask import Blueprint, abort, render_template, request, redirect, url_for, session

from settings import SBL_PASSWORD
from util.db import get_item, get_list, add_item, edit_item
from util.util import md, auth, referrer

sbl_list = Blueprint('sbl_list', __name__)


@sbl_list.route('/')
@sbl_list.route('/year/<int:year>')
@sbl_list.route('/tag/<string:tag>')
@sbl_list.route('/year/<int:year>/tag/<string:tag>')
def index(year=None, tag=None):
    editable = auth(session, SBL_PASSWORD)
    if not tag and not year:
        year = datetime.now().year
    list = get_list(year, tag)
    if not list:
        abort(404)
    return render_template('list/index.html', list=list, year=year, tag=tag, editable=editable)


@sbl_list.route('/item/<int:item_id>')
def item_show(item_id):
    editable = auth(session, SBL_PASSWORD)
    item = get_item(item_id)
    if not item:
        abort(404)
    review = item[7].replace("\r", "\n")
    if not editable:
        review = sub("\s?/\*[\s\S]*\*/s?", "", review)
    review = md(review)
    item = list(item)
    item.pop(7)
    item.append(review)
    return render_template('list/item.html', item=item, editable=editable)


@sbl_list.route('/add', methods=['POST', 'GET'])
def add():
    if auth(session, SBL_PASSWORD):
        if request.method == 'POST':
            name = request.form["name"]
            state = int(request.form["state"])
            if state == 0 or state == 2:
                addDate = request.form["addDate"]
                comDate = ""
            else:
                comDate = addDate = request.form["comDate"]
            score = int(request.form["score"])
            tag = request.form["tag"].replace(" ", "")
            review = request.form["review"]
            isReview = 0
            if review:
                isReview = 1
            add_item(name, state, addDate, comDate, score, isReview, review, tag)
            year = addDate[:4]
            if comDate:
                year = comDate[:4]
            return redirect(url_for('.index', year=year))
        return render_template('list/add.html')
    else:
        return redirect(referrer(url_for('sbl_login.login'), request.url))


@sbl_list.route('/edit/<int:item_id>', methods=['POST', 'GET'])
def edit(item_id):
    if auth(session, SBL_PASSWORD):
        if request.method == 'POST':
            name = request.form["name"]
            state = int(request.form["state"])
            addDate = request.form["addDate"]
            comDate = request.form["comDate"]
            score = int(request.form["score"])
            tag = request.form["tag"].replace(" ", "")
            review = request.form["review"]
            isReview = 0
            if review:
                isReview = 1
            edit_item(item_id, name, state, addDate, comDate, score, isReview, review, tag)
            if review:
                return redirect(url_for('.item_show', item_id=item_id))
            else:
                year = addDate[:4]
                if comDate:
                    year = comDate[:4]
                return redirect(url_for('.index', year=year))
        item = get_item(item_id)
        if not item:
            abort(404)
        return render_template('list/edit.html', item=item)
    else:
        return redirect(referrer(url_for('sbl_login.login'), request.url))
