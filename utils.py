from flask import session, abort

def valid_csrf(token):
    if "csrf_token" not in session:
        abort(403)
    if not session["csrf_token"] == token:
        abort(403)

def require_login():
    if "name" not in session or "user_id" not in session:
        abort(403)