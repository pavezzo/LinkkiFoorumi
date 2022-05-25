from urllib.parse import urlparse
from db import db
from flask import request, session
import users

def new(sub_name, title, url):
    parsed_url = urlparse(url)

    if not parsed_url.scheme:
        url = "https://" + url

    sql = """INSERT INTO links (user_id, subforum_id, url, title, created_at)
             VALUES (:user_id, (SELECT sub_id FROM subforums WHERE sub_name=:sub_name), 
             :url, :title, NOW()) 
             RETURNING link_id"""
    result = db.session.execute(sql, {"user_id":session["user_id"], "sub_name":sub_name, "url":url, "title":title})
    link_id = result.fetchone()[0]
    db.session.commit()
    return link_id

def view(link_id):
    sql = """SELECT title, url, created_at, name FROM links JOIN users ON user_id=id
             WHERE link_id=:link_id"""
    result = db.session.execute(sql, {"link_id":link_id})
    link = result.fetchone()
    if link:
        return link
    return False

def get_all():
    sql = "SELECT link_id, title, url, created_at FROM links ORDER BY created_at DESC"
    results = db.session.execute(sql)
    links = results.fetchall()

    return links