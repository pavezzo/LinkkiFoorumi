from urllib.parse import urlparse
from db import db
from flask import request, session
import users

def new(sub_name, title, url):
    parsed_url = urlparse(url)

    if not parsed_url.scheme:
        url = "https://" + url

    try:
        sql = """INSERT INTO links (user_id, subforum_id, url, title, created_at)
                 VALUES (:user_id, (SELECT sub_id FROM subforums WHERE sub_name=:sub_name), 
                 :url, :title, NOW()) 
                 RETURNING link_id"""
        result = db.session.execute(sql, {"user_id":session["user_id"], "sub_name":sub_name, "url":url, "title":title})
        link_id = result.fetchone()[0]
        db.session.commit()
        return link_id
    except:
        return False

def get(link_id):
    sql = """SELECT link_id, user_id, title, url, created_at, name,
             (SELECT COALESCE(SUM(CASE WHEN positive THEN 1 ELSE -1 END), 0)
             FROM likes WHERE likes.link_id=:link_id) AS count_likes
             FROM links JOIN users ON user_id=id
             WHERE link_id=:link_id"""
    result = db.session.execute(sql, {"link_id":link_id})
    link = result.fetchone()
    if link:
        print(link)
        return link
    return False

def delete(link_id):
    sql = "DELETE FROM links WHERE link_id=:link_id"
    db.session.execute(sql, {"link_id":link_id})
    db.session.commit()