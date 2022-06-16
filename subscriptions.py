from db import db
from flask import session

def new(subforum_id):
    sql = """INSERT INTO subscriptions (user_id, subforum_id, created_at)
             VALUES (:user_id, :subforum_id, NOW())"""
    db.session.execute(sql, {"user_id":session["user_id"], "subforum_id":subforum_id})
    db.session.commit()

def unsubscribe(subforum_id):
    sql = "DELETE FROM subscriptions WHERE user_id=:user_id AND subforum_id=:subforum_id"
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
    return subforums

def get_users_content():
    if "user_id" not in session:
        return False

    sql = """SELECT links.link_id, NULL AS post_id, links.user_id AS owner_id, title, url, links.created_at, count(comment_id) AS count_comments,
             (SELECT COALESCE(SUM(CASE WHEN positive THEN 1 ELSE -1 END), 0)
             FROM likes WHERE likes.link_id=links.link_id) AS count_likes,
             sub_name, users.name
             FROM links
             LEFT JOIN comments ON comments.link_id=links.link_id
             JOIN subforums ON subforums.sub_id=links.subforum_id
             JOIN users ON users.id=links.user_id
             WHERE links.subforum_id IN (SELECT subforum_id FROM subscriptions WHERE user_id=:user_id)
             GROUP BY links.link_id, sub_name, users.name
             UNION SELECT NULL AS link_id, text_posts.post_id, text_posts.user_id AS owner_id, title, NULL AS url, text_posts.created_at, count(comment_id) AS count_comments,
             (SELECT COALESCE(SUM(CASE WHEN positive THEN 1 ELSE -1 END), 0)
             FROM likes WHERE likes.post_id=text_posts.post_id) AS count_likes,
             sub_name, users.name
             FROM text_posts
             LEFT JOIN comments ON comments.post_id=text_posts.post_id
             JOIN subforums ON subforums.sub_id=text_posts.subforum_id
             JOIN users ON users.id=text_posts.user_id
             WHERE text_posts.subforum_id IN (SELECT subforum_id FROM subscriptions WHERE user_id=:user_id)
             GROUP BY text_posts.post_id, sub_name, users.name
             ORDER BY created_at DESC"""
    results = db.session.execute(sql, {"user_id":session["user_id"]}).fetchall()
    return results

def get_users_content_top():
    if "user_id" not in session:
        return False

    sql = """SELECT links.link_id, NULL AS post_id, links.user_id AS owner_id, title, url, links.created_at, count(comment_id) AS count_comments,
             (SELECT COALESCE(SUM(CASE WHEN positive THEN 1 ELSE -1 END), 0)
             FROM likes WHERE likes.link_id=links.link_id) AS count_likes,
             sub_name, users.name
             FROM links
             LEFT JOIN comments ON comments.link_id=links.link_id
             JOIN subforums ON subforums.sub_id=links.subforum_id
             JOIN users ON users.id=links.user_id
             WHERE links.subforum_id IN (SELECT subforum_id FROM subscriptions WHERE user_id=:user_id)
             GROUP BY links.link_id, sub_name, users.name
             UNION SELECT NULL AS link_id, text_posts.post_id, text_posts.user_id AS owner_id, title, NULL AS url, text_posts.created_at, count(comment_id) AS count_comments,
             (SELECT COALESCE(SUM(CASE WHEN positive THEN 1 ELSE -1 END), 0)
             FROM likes WHERE likes.post_id=text_posts.post_id) AS count_likes,
             sub_name, users.name
             FROM text_posts
             LEFT JOIN comments ON comments.post_id=text_posts.post_id
             JOIN subforums ON subforums.sub_id=text_posts.subforum_id
             JOIN users ON users.id=text_posts.user_id
             WHERE text_posts.subforum_id IN (SELECT subforum_id FROM subscriptions WHERE user_id=:user_id)
             GROUP BY text_posts.post_id, sub_name, users.name
             ORDER BY count_likes DESC"""

    results = db.session.execute(sql, {"user_id":session["user_id"]}).fetchall()
    return results
