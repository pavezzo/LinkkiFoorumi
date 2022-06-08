from flask import session
from db import db

def new(positive, link_id=None, post_id=None, comment_id=None):
    if not link_id: link_id = None
    if not post_id: post_id = None
    if not comment_id: comment_id = None

    sql = """UPDATE likes SET positive=:positive
             WHERE user_id=:user_id AND (link_id=:link_id OR post_id=:post_id OR comment_id=:comment_id)
             RETURNING like_id"""

    result = db.session.execute(sql, {"positive":positive, "user_id":session["user_id"], "link_id":link_id, "post_id":post_id,
                "comment_id":comment_id})
    db.session.commit()
    exists = result.fetchone()
    
    if exists:
        return 

    sql = """INSERT INTO likes (user_id, link_id, post_id, comment_id, positive)
             VALUES (:user_id, :link_id, :post_id, :comment_id, :positive)
             RETURNING like_id"""
    db.session.execute(sql, {"user_id":session["user_id"], "link_id":link_id, "post_id":post_id,
                "comment_id":comment_id, "positive":positive})
    db.session.commit()