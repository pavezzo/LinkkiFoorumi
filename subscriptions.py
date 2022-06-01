from db import db
from flask import session

def new(subforum_id):
    sql = """INSERT INTO subscriptions (user_id, subforum_id, created_at)
             VALUES (:user_id, :subforum_id, NOW())"""
    db.session.execute(sql, {"user_id":session["user_id"], "subforum_id":subforum_id})
    db.session.commit()

def check_subscription(subforum_id):
    if "user_id" not in session:
        return False
    sql = """SELECT subscription_id FROM subscriptions
             WHERE subforum_id=:subforum_id AND user_id=:user_id"""
    result = db.session.execute(sql, {"subforum_id":subforum_id, "user_id":session["user_id"]})
    subbed = result.fetchone()
    if subbed:
        return True
    return False

def get_users_subscriptions():
    if "user_id" not in session:
        return False

    sql = """SELECT subforum_id, sub_name, introduction FROM subscriptions
             JOIN subforums ON subforum_id=sub_id WHERE user_id=:user_id"""
    results = db.session.execute(sql, {"user_id":session["user_id"]})
    subforums = results.fetchall()
    print(subforums)
    return subforums

def get_users_content():
    if "user_id" not in session:
        return False

    sql = """SELECT link_id, NULL AS post_id, title, url, created_at FROM links
             WHERE links.subforum_id IN (SELECT subforum_id FROM subscriptions WHERE user_id=:user_id)
             UNION SELECT NULL AS link_id, post_id, title, NULL AS url, created_at
             FROM text_posts
             WHERE text_posts.subforum_id IN (SELECT subforum_id FROM subscriptions WHERE user_id=:user_id)
             ORDER BY created_at DESC"""
    results = db.session.execute(sql, {"user_id":session["user_id"]}).fetchall()
    return results