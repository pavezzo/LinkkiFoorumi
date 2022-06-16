from flask import session, abort, Response
import humanize
import datetime as dt

def valid_csrf(token=None):
    if not token:
        abort(403)
    if "csrf_token" not in session:
        abort(403)
    if not session["csrf_token"] == token:
        abort(403)

def require_login():
    if "name" not in session or "user_id" not in session:
        abort(Response("You need to be logged in to perform this function"))

def time_since(date):
    return humanize.naturaltime(dt.datetime.now() - date)