from unittest import result
from db import db
from flask import request, session

def new(name, introduction):
    if "user_id" not in session:
        return False

    sql = """INSERT INTO subforums (owner_id, sub_name, introduction, created_at)
             VALUES (:owner_id, :sub_name, :introduction, NOW())"""

    db.session.execute(sql, {"owner_id":session["user_id"], "sub_name":name,
                       "introduction":introduction})
    db.session.commit()
    return True

def get_by_name(name):
    sql = """SELECT sub_id, owner_id, introduction, name FROM subforums
             JOIN users ON owner_id=id
             WHERE sub_name=:sub_name"""
    result = db.session.execute(sql, {"sub_name":name})
    subforum = result.fetchone()
    if subforum:
        return subforum
    return False

def get_newest(subforum_id):
    sql = """SELECT links.link_id, NULL AS post_id, title, url, links.created_at, count(comment_id) AS count_comments,
             (SELECT COALESCE(SUM(CASE WHEN positive THEN 1 ELSE -1 END), 0)
             FROM likes WHERE likes.link_id=links.link_id) AS count_likes
             FROM links
             LEFT JOIN comments ON comments.link_id=links.link_id
             WHERE subforum_id=:subforum_id
             GROUP BY links.link_id
             UNION SELECT NULL AS link_id, text_posts.post_id, title, NULL AS url, text_posts.created_at, 
             count(comment_id) AS count_comments,
             (SELECT COALESCE(SUM(CASE WHEN positive THEN 1 ELSE -1 END), 0)
             FROM likes WHERE likes.post_id=text_posts.post_id) AS count_likes
             FROM text_posts 
             LEFT JOIN comments ON comments.post_id=text_posts.post_id
             WHERE subforum_id=:subforum_id
             GROUP BY text_posts.post_id
             ORDER BY created_at DESC"""
    results = db.session.execute(sql, {"subforum_id":subforum_id})
    contents = results.fetchall()
    return contents
    