from app import app
from flask import render_template, request, redirect, session
import users

@app.route("/")
def index():
    return "moi"

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["post"])
def register2():
    if "admin" in request.form:
        users.register(request.form["username"], request.form["password"], True)
    else:
        users.register(request.form["username"], request.form["password"])

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        if users.login(request.form["username"], request.form["password"]):
            return "toimii"
        return "ei toimi"