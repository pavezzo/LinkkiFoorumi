from db import db
from flask import request, session
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

def register(name, password, admin=False):
    print(name, password, admin)
    hash = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (name, password, admin)
                 VALUES (:name, :password, :admin)"""
        db.session.execute(sql, {"name":name, "password":hash, "admin":admin})
        db.session.commit()
    except:
        return False

def login(name, password):
    sql = "SELECT id, password FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash = user.password
        if check_password_hash(hash, password):
            session["name"] = name
            session["user_id"] = user.id
            session["csrf_token"] = token_hex(16)
            return True
        else:
            return False

def logout():
    del session["name"]
    del session["user_id"]
    del session["csrf_token"]

def get_userid(name):
    sql = "SELECT id FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    id = result.fetchone()
    return id[0]

def get_user_by_id(id):
    sql = "SELECT name FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()

    if not user:
        return False
    
    return user[0]

    
