from pymysql import connect
from xpinyin import Pinyin

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, SBL_BLOG_SECRET_TAG
from .util import logged


def get_nav():
    secret = "WHERE tag NOT LIKE '%%%s%%'" % SBL_BLOG_SECRET_TAG
    if logged():
        secret = ""
    conn = get_connect()
    cur = conn.cursor()
    list_data = []
    cur.execute("SELECT date_format(addDate,'%Y') FROM list GROUP BY date_format(addDate,'%Y') DESC;")
    years = cur.fetchall()
    for year in years:
        cur.execute("SELECT group_concat(m) FROM "
                    "(SELECT date_format(addDate,'%%m') AS m FROM list WHERE addDate LIKE '%s%%' "
                    "GROUP BY date_format(addDate,'%%m')) t" % year)
        months = cur.fetchall()[0][0].split(",")
        list_data.append([year[0], months])
    cur.execute("SELECT tag FROM list GROUP BY tag;")
    list_data = [list_data, split_tag(cur.fetchall())]
    blog_data = []
    cur.execute("SELECT date_format(addDate,'%Y') FROM blog GROUP BY date_format(addDate,'%Y') DESC;")
    years = cur.fetchall()
    for year in years:
        cur.execute("SELECT group_concat(m) FROM "
                    "(SELECT date_format(addDate,'%%m') AS m FROM blog WHERE addDate LIKE '%s%%' "
                    "GROUP BY date_format(addDate,'%%m')) t" % year)
        months = cur.fetchall()[0][0].split(",")
        blog_data.append([year[0], months])
    cur.execute("SELECT tag FROM blog %s GROUP BY tag;" % secret)
    blog_data = [blog_data, split_tag(cur.fetchall())]
    cur.close()
    conn.close()
    return list_data, blog_data


def split_tag(tag):
    return sorted(set([t for ta in tag for t in ta[0].split(";")]), key=Pinyin().get_initials)


def get_list(year, month, tag):
    and_tag = ""
    if tag:
        and_tag = "AND tag LIKE '%%%s%%' " % convert(tag)[0]
    and_data = "AND %s LIKE '%d-%s%%' "
    and_add_date = ""
    and_com_date = ""
    if year:
        if not month:
            month = ""
        and_add_date = and_data % ("addDate", year, month)
        and_com_date = and_data % ("comDate", year, month)
    conn = get_connect()
    cur = conn.cursor()
    cur.execute("SELECT id,name,addDate,tag "
                "FROM list "
                "WHERE state=0 %s%s"
                "ORDER BY addDate,name;" % (and_add_date, and_tag))
    todo = cur.fetchall()
    cur.execute("SELECT id,name,comDate,score,isReview,tag "
                "FROM list "
                "WHERE state=1 %s%s"
                "ORDER BY comDate DESC,name;" % (and_com_date, and_tag))
    done = cur.fetchall()
    cur.execute("SELECT id,name,addDate,isReview,tag "
                "FROM list "
                "WHERE state=2 %s%s"
                "ORDER BY addDate DESC,name;" % (and_add_date, and_tag))
    undo = cur.fetchall()
    cur.close()
    conn.close()
    if len(todo) + len(done) + len(undo) == 0:
        return None
    return todo, done, undo, (len(done), len(done) + len(todo))


def get_blog(year, month, tag):
    secret = "tag NOT LIKE '%%%s%%' AND " % SBL_BLOG_SECRET_TAG
    if logged():
        secret = ""
    and_tag = ""
    if tag:
        and_tag = "tag LIKE '%%%s%%' " % convert(tag)[0].replace(";", "")
    and_add_date = ""
    if year:
        if not month:
            month = ""
        and_add_date = "addDate LIKE '%d-%s%%' " % (year, month)
    and_and = ""
    if tag and year:
        and_and = "AND "
    conn = get_connect()
    cur = conn.cursor()
    cur.execute("SELECT id,title,addDate,tag "
                "FROM blog "
                "WHERE %s%s%s%s "
                "ORDER BY addDate DESC;" % (secret, and_add_date, and_and, and_tag))
    blog = cur.fetchall()
    cur.close()
    conn.close()
    return blog


def get_item(item_id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute("SELECT * "
                "FROM list "
                "WHERE id=%d" % item_id)
    item = cur.fetchone()
    cur.close()
    conn.close()
    return item


def get_post(post_id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute("SELECT * "
                "FROM blog "
                "WHERE id=%d" % post_id)
    item = cur.fetchone()
    cur.close()
    conn.close()
    return item


def add_item(name, state, addDate, comDate, score, isReview, review, tag):
    name, review, tag = convert(name, review, tag)
    conn = get_connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO list "
                "(name,state,addDate,comDate,score,isReview,review,tag) VALUES "
                "('%s', %d, '%s', '%s', %d, %d, '%s', '%s');" %
                (name, state, addDate, comDate, score, isReview, review, tag))
    conn.commit()
    cur.close()
    conn.close()


def add_post(title, content, addDate, updDate, tag):
    title, content, tag = convert(title, content, tag)
    conn = get_connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO blog "
                "(title,content,addDate,updDate,tag) VALUES "
                "('%s', '%s', '%s', '%s', '%s');" %
                (title, content, addDate, updDate, tag))
    conn.commit()
    cur.close()
    conn.close()


def edit_item(item_id, name, state, addDate, comDate, score, isReview, review, tag):
    name, review, tag = convert(name, review, tag)
    conn = get_connect()
    cur = conn.cursor()
    cur.execute("UPDATE list "
                "SET name='%s',state=%d,addDate='%s',comDate='%s',score=%d,isReview=%d,review='%s',tag='%s' "
                "WHERE id=%d;" % (name, state, addDate, comDate, score, isReview, review, tag, item_id))
    conn.commit()
    cur.close()
    conn.close()


def edit_post(post_id, title, content, addDate, updDate, tag):
    title, content, tag = convert(title, content, tag)
    conn = get_connect()
    cur = conn.cursor()
    cur.execute("UPDATE blog "
                "SET title='%s',content='%s',addDate='%s',updDate='%s',tag='%s' "
                "WHERE id=%d;" % (title, content, addDate, updDate, tag, post_id))
    conn.commit()
    cur.close()
    conn.close()


def convert(*text):
    return [t.replace('\'', "\\\'") for t in text]


def get_connect():
    return connect(host=DB_HOST,
                   port=DB_PORT,
                   user=DB_USER,
                   passwd=DB_PASSWORD,
                   db=DB_NAME,
                   charset='utf8')
