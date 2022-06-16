from db import db
from flask import request, session
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

def register(name, password, admin=False):
    hash = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (name, password, admin)
                 VALUES (:name, :password, :admin)"""
        db.session.execute(sql, {"name":name, "password":hash, "admin":admin})
        db.session.commit()
    except:
        return False

    login(name, password)

def login(name, password):
    sql = "SELECT id, password, admin FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if user is None:
        return False
    else:
        hash = user.password
        if check_password_hash(hash, password):
            session["name"] = name
            session["user_id"] = user.id
            session["csrf_token"] = token_hex(16)
            session["admin"] = user.admin
            return True
        else:
            return False

def logout():
    del session["name"]
    del session["user_id"]
    del session["csrf_token"]
    del session["admin"]
