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
    sql = """SELECT sub_id, owner_id, introduction, created_at, name FROM subforums
             JOIN users ON owner_id=id WHERE sub_name=:sub_name"""
    result = db.session.execute(sql, {"sub_name":name})
    subforum = result.fetchone()
    if subforum:
        return subforum
    return False

def get_newest(subforum_id):
    sql = """SELECT link_id, NULL AS post_id, title, url, created_at FROM links
             WHERE subforum_id=:subforum_id
             UNION SELECT NULL AS link_id, post_id, title, NULL AS url, created_at
             FROM text_posts WHERE subforum_id=:subforum_id
             ORDER BY created_at DESC"""
    results = db.session.execute(sql, {"subforum_id":subforum_id})
    contents = results.fetchall()
    return contents
    