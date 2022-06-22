from db import db
from flask import session

def get_newest():
    sql = """SELECT links.link_id, NULL AS post_id, links.user_id AS owner_id, title, url, links.created_at,
             COUNT(comments.comment_id) AS count_comments,
             (SELECT COALESCE(SUM(CASE WHEN positive THEN 1 ELSE -1 END), 0) FROM likes WHERE likes.link_id=links.link_id) AS count_likes,
             sub_name, users.name
             FROM links
             LEFT JOIN comments ON comments.link_id=links.link_id
             JOIN subforums ON subforums.sub_id=links.subforum_id
             JOIN users ON users.id=links.user_id
             GROUP BY links.link_id, sub_name, users.name
             UNION SELECT NULL AS link_id, text_posts.post_id, text_posts.user_id AS owner_id, title, NULL AS url, text_posts.created_at,
             COUNT(comments.comment_id) AS count_comments,
             (SELECT COALESCE(SUM(CASE WHEN positive THEN 1 ELSE -1 END), 0) FROM likes WHERE likes.post_id=text_posts.post_id) AS count_likes,
             sub_name, users.name
             FROM text_posts
             LEFT JOIN comments ON comments.post_id=text_posts.post_id
             JOIN subforums ON subforums.sub_id=text_posts.subforum_id
             JOIN users ON users.id=text_posts.user_id
             GROUP BY text_posts.post_id, sub_name, users.name
             ORDER BY created_at DESC"""

    results = db.session.execute(sql)
    contents = results.fetchall()
    return contents

def get_most_liked():
    sql = """SELECT links.link_id, NULL AS post_id, links.user_id AS owner_id, title, url, links.created_at,
             COUNT(comments.comment_id) AS count_comments,
             (SELECT COALESCE(SUM(CASE WHEN positive THEN 1 ELSE -1 END), 0) FROM likes WHERE likes.link_id=links.link_id) AS count_likes,
             sub_name, users.name
             FROM links
             LEFT JOIN comments ON comments.link_id=links.link_id
             JOIN subforums ON subforums.sub_id=links.subforum_id
             JOIN users ON users.id=links.user_id
             GROUP BY links.link_id, sub_name, users.name
             UNION SELECT NULL AS link_id, text_posts.post_id, text_posts.user_id AS owner_id, title, NULL AS url, text_posts.created_at,
             COUNT(comments.comment_id) AS count_comments,
             (SELECT COALESCE(SUM(CASE WHEN positive THEN 1 ELSE -1 END), 0) FROM likes WHERE likes.post_id=text_posts.post_id) AS count_likes,
             sub_name, users.name
             FROM text_posts
             LEFT JOIN comments ON comments.post_id=text_posts.post_id
             JOIN subforums ON subforums.sub_id=text_posts.subforum_id
             JOIN users ON users.id=text_posts.user_id
             GROUP BY text_posts.post_id, sub_name, users.name
             ORDER BY count_likes DESC"""

    results = db.session.execute(sql).fetchall()
    return results