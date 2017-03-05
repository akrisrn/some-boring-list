from pymysql import connect
from xpinyin import Pinyin

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, SBL_BLOG_SECRET_TAG


def get_nav():
    conn = get_connect()
    cur = conn.cursor()
    cur.execute("SELECT date_format(addDate,'%Y') FROM list GROUP BY date_format(addDate,'%Y') DESC;")
    year = cur.fetchall()
    cur.execute("SELECT tag FROM list GROUP BY tag;")
    list_tag = cur.fetchall()
    cur.execute("SELECT tag FROM blog WHERE tag NOT LIKE '%%%s%%' GROUP BY tag;" % SBL_BLOG_SECRET_TAG)
    blog_tag = cur.fetchall()
    cur.close()
    conn.close()
    list_tag = split_tag(list_tag)
    blog_tag = split_tag(blog_tag)
    return year[1:], list_tag, blog_tag


def split_tag(tag):
    return sorted(set([t for ta in tag for t in ta[0].split(";")]), key=Pinyin().get_initials)


def get_list(year, tag):
    and_tag = ""
    if tag:
        and_tag = "AND tag LIKE '%%%s%%' " % convert(tag)[0]
    and_year = ""
    if year:
        and_year = "AND addDate LIKE '%d%%' " % year
    conn = get_connect()
    cur = conn.cursor()
    cur.execute("SELECT id,name,addDate,tag "
                "FROM list "
                "WHERE state=0 %s%s"
                "ORDER BY addDate,name;" % (and_year, and_tag))
    todo = cur.fetchall()
    cur.execute("SELECT id,name,comDate,score,isReview,tag "
                "FROM list "
                "WHERE state=1 %s%s"
                "ORDER BY comDate DESC,name;" % (and_year, and_tag))
    done = cur.fetchall()
    cur.execute("SELECT id,name,addDate,isReview,tag "
                "FROM list "
                "WHERE state=2 %s%s"
                "ORDER BY addDate DESC,name;" % (and_year, and_tag))
    undo = cur.fetchall()
    cur.close()
    conn.close()
    if len(todo) + len(done) + len(undo) == 0:
        return None
    return todo, done, undo, (len(done), len(done) + len(todo))


def get_blog(tag):
    if not tag:
        tag = ""
    else:
        tag = convert(tag)[0].replace(";", "")
    conn = get_connect()
    cur = conn.cursor()
    cur.execute("SELECT id,title,addDate,tag "
                "FROM blog "
                "WHERE tag LIKE '%%%s%%' "
                "ORDER BY addDate DESC;" % tag)
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
