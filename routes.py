from app import app
from flask import render_template, request, redirect, session
import users
import links

@app.route("/")
def index():
    return render_template("index.html")

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
            return redirect("/")
        return "ei toimi"

@app.route("/newlink", methods=["GET", "POST"])
def newlink():
    if request.method == "GET":
        return render_template("newlink.html")
    if request.method == "POST":
        link_id = links.new(request.form["title"], request.form["link"])
        if link_id:
            return str(link_id)
        return redirect("/links")

@app.route("/link/<int:id>")
def link(id):
    result = links.view(id)
    if result:
        name = users.get_user_by_id(result.user_id)
        print(result)
        return render_template("link.html", title=result.title, url=result.url, date=result.created_at, name=name)

@app.route("/links")
def all_links():
    results = links.get_all()
    return render_template("links.html", links=results)
