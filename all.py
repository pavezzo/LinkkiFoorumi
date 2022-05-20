from db import db
from flask import session

def get_newest():
    sql = """SELECT link_id, NULL AS post_id, title, url, created_at FROM links
             UNION SELECT NULL AS link_id, post_id, title, NULL AS url, created_at
             FROM text_posts
             ORDER BY created_at DESC"""

    results = db.session.execute(sql)
    contents = results.fetchall()
    return contents