from db import db
from flask import session

def new(link_id, post_id, parent, comment):
    if not link_id: link_id = None
    if not post_id: post_id = None
    if not parent: parent = None
    sql = """INSERT INTO comments (user_id, post_id, link_id, comment, parent, 
             created_at) VALUES (:user_id, :post_id, :link_id, :comment, :parent,
             NOW())"""
    db.session.execute(sql, {"user_id":session["user_id"], "post_id":post_id,
            "link_id":link_id, "comment":comment, "parent":parent})
    db.session.commit()

def get_for_link(link_id):
    sql = """SELECT comment_id, comment, parent, created_at, name,
             (SELECT COALESCE(SUM(CASE WHEN positive THEN 1 ELSE -1 END), 0)
             FROM likes WHERE likes.comment_id=comments.comment_id) AS count_likes
             FROM comments 
             JOIN users ON user_id=id WHERE link_id=:link_id ORDER BY created_at"""
    results = db.session.execute(sql, {"link_id":link_id})
    comms = results.fetchall()
    return comms

def get_for_post(post_id):
    sql = """SELECT comment_id, comment, parent, created_at, name,
             (SELECT COALESCE(SUM(CASE WHEN positive THEN 1 ELSE -1 END), 0)
             FROM likes WHERE likes.comment_id=comments.comment_id) AS count_likes
             FROM comments 
             JOIN users ON user_id=id WHERE post_id=:post_id ORDER BY created_at"""
    results = db.session.execute(sql, {"post_id":post_id})
    comms = results.fetchall()
    return comms
