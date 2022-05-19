from urllib.parse import urlparse
from db import db
from flask import request, session
import users

def new(title, url):
    if "name" not in session:
        return False

    parsed_url = urlparse(url)

    if not parsed_url.scheme:
        url = "https://" + url

    sql = """INSERT INTO links (user_id, url, title, created_at)
             VALUES (:user_id, :url, :title, NOW()) RETURNING link_id"""
    result = db.session.execute(sql, {"user_id":session["user_id"], "url":url, "title":title})
    link_id = result.fetchone()[0]
    db.session.commit()
    return link_id

def view(id):
    sql = "SELECT title, url, user_id, created_at FROM links WHERE link_id=:link_id"
    result = db.session.execute(sql, {"link_id":id})
    link = result.fetchone()
    if link:
        return link

def get_all():
    sql = "SELECT title, url, created_at FROM links ORDER BY created_at DESC"
    results = db.session.execute(sql)
    links = results.fetchall()

    return links