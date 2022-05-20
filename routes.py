from app import app
from flask import render_template, request, redirect, session
import users
import links
import text_posts
import all

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

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/newlink", methods=["GET", "POST"])
def newlink():
    if request.method == "GET":
        return render_template("newlink.html")
    if request.method == "POST":
        link_id = links.new(request.form["title"], request.form["link"])
        return redirect("/link/"+str(link_id))

@app.route("/link/<int:id>")
def link(id):
    result = links.view(id)
    if result:
        return render_template("link.html", title=result.title, url=result.url, date=result.created_at, name=result.name)

@app.route("/links")
def all_links():
    results = links.get_all()
    return render_template("links.html", links=results)

@app.route("/newpost", methods=["GET", "POST"])
def new_post():
    if request.method == "GET":
        return render_template("newpost.html")

    if request.method == "POST":
        post_id = text_posts.new(request.form["title"], request.form["post_content"])
        return str(post_id)

@app.route("/post/<int:id>")
def post(id):
    result = text_posts.get(id)
    if result:
        return render_template("post.html", title=result.title, post_content=result.post_content,
                name=result.name, date=result.created_at)

@app.route("/posts")
def posts():
    results = text_posts.get_all()
    print(results)
    return render_template("posts.html", text_posts=results)

@app.route("/all")
def all_newest():
    results = all.get_newest()
    return render_template("all.html", items=results)