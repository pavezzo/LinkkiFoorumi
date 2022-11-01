from db import db
from flask import session
from sqlalchemy import exc
import users
import utils

def new(sub_name, title, post_content):
    try:
        sql = """INSERT INTO text_posts (user_id, subforum_id, title, post_content, created_at)
                 VALUES (:user_id, (SELECT sub_id FROM subforums WHERE sub_name=:sub_name),
                 :title, :post_content, NOW()) RETURNING post_id"""
        result = db.session.execute(sql, {"user_id":session["user_id"], "sub_name":sub_name, "title":title, 
                                    "post_content":post_content})
        post_id = result.fetchone()[0]
        db.session.commit()
        return post_id
    except:
        return False

def get(post_id):
    sql = """SELECT post_id, user_id, title, post_content, created_at, name,
            (SELECT COALESCE(SUM(CASE WHEN positive THEN 1 ELSE -1 END), 0)
            FROM likes WHERE likes.post_id=:post_id) AS count_likes
            FROM text_posts JOIN users ON user_id=id
            WHERE post_id=:post_id"""
    result = db.session.execute(sql, {"post_id":post_id})
    post = result.fetchone()
    if post:
        return post
    return False

def get_all():
    sql = """SELECT post_id, title, created_at FROM text_posts ORDER BY created_at
             DESC"""
    results = db.session.execute(sql)
    posts = results.fetchall()

    return posts

def delete(post_id):
    sql = "DELETE FROM text_posts WHERE post_id=:post_id"
    db.session.execute(sql, {"post_id":post_id})
    db.session.commit()
