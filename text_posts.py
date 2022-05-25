from db import db
from flask import session
import users
import utils

def new(sub_name, title, post_content):
    sql = """INSERT INTO text_posts (user_id, subforum_id, title, post_content, created_at)
             VALUES (:user_id, (SELECT sub_id FROM subforums WHERE sub_name=:sub_name),
             :title, :post_content, NOW()) RETURNING post_id"""
    result = db.session.execute(sql, {"user_id":session["user_id"], "sub_name":sub_name, "title":title, 
                                "post_content":post_content})
    post_id = result.fetchone()[0]
    db.session.commit()
    return post_id

def get(post_id):
    sql = """SELECT title, post_content, created_at, name FROM text_posts JOIN users ON user_id=id
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