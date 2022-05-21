from flask import session

def valid_csrf(token):
    return session["csrf_token"] == token