from app import app
from flask import render_template, request, redirect, session, abort
import users
import links
import text_posts
import all
import utils
import comments
import subforums
import subscriptions
import likes

@app.route("/", methods=["GET"])
def index():
    results = subscriptions.get_users_content()
    return render_template("all.html", items=results)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
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
        return render_template("newlink.html", sub_name=request.args.get("subforum"))
    if request.method == "POST":
        utils.valid_csrf(request.form["csrf_token"])
        utils.require_login()
        link_id = links.new(request.form["sub_name"], request.form["title"], request.form["link"])
        return redirect("/link/"+str(link_id))

@app.route("/link/<int:id>")
def link(id):
    result = links.view(id)
    comms = comments.get_for_link(id)
    if result:
        return render_template("link.html", link_id=id, title=result.title, url=result.url, 
                        date=result.created_at, name=result.name, comments=comms)

@app.route("/links")
def all_links():
    results = links.get_all()
    return render_template("links.html", links=results)

@app.route("/newpost", methods=["GET", "POST"])
def new_post():
    if request.method == "GET":
        return render_template("newpost.html", sub_name=request.args.get("subforum"))

    if request.method == "POST":
        utils.valid_csrf(request.form["csrf_token"])
        utils.require_login()
        post_id = text_posts.new(request.form["sub_name"], request.form["title"], request.form["post_content"])
        
        return str(post_id)

@app.route("/post/<int:id>")
def post(id):
    result = text_posts.get(id)
    comms = comments.get_for_post(id)
    if result:
        return render_template("post.html", post_id=id, title=result.title, post_content=result.post_content,
                name=result.name, date=result.created_at, comments=comms)

@app.route("/posts")
def posts():
    results = text_posts.get_all()
    print(results)
    return render_template("posts.html", text_posts=results)

@app.route("/sub/all")
def all_newest():
    results = all.get_newest()
    return render_template("all.html", items=results)

@app.route("/newcomment", methods=["POST"])
def new_comment():
    utils.require_login()
    utils.valid_csrf(request.form["csrf_token"])
    comments.new(request.form["link_id"], request.form["post_id"], request.form["parent"],
                request.form["comment"])
    if request.form["link_id"]:
        link_url = "/link/" + request.form["link_id"]
        return redirect(link_url)
    if request.form["post_id"]:
        post_url = "/post/" + request.form["post_id"]
        return redirect(post_url)

@app.route("/newsubforum", methods=["GET", "POST"])
def new_subforum():
    if request.method == "GET":
        return render_template("newsubforum.html")
    if request.method == "POST":
        utils.require_login()
        utils.valid_csrf(request.form["csrf_token"])
        if subforums.new(request.form["sub_name"], request.form["introduction"]):
            return redirect("/")

@app.route("/sub/<string:name>")
def view_subforum(name):
    result = subforums.get_by_name(name)
    subbed = subscriptions.check_subscription(result.sub_id)
    if not result:
        abort(404)
    contents = subforums.get_newest(result.sub_id)
    return render_template("subforum.html", subforum_id=result.sub_id, sub_name=name, introduction=result.introduction, contents=contents, subbed=subbed)

@app.route("/newsubscription", methods=["post"])
def new_subscription():
    utils.require_login()
    utils.valid_csrf(request.form["csrf_token"])
    subscriptions.new(request.form["subforum_id"])
    url = "/sub/" + request.form["subforum"]
    return redirect(url)

@app.route("/unsubscribe", methods=["post"])
def unsubscribe():
    utils.require_login()
    utils.valid_csrf(request.form["csrf_token"])
    subscriptions.unsubscribe(request.form["subforum_id"])
    url = "/sub/" + request.form["subforum"]
    return redirect(url)

@app.route("/subscriptions", methods=["get"])
def show_subscriptions():
    utils.require_login()
    subforums = subscriptions.get_users_subscriptions()
    return render_template("subscriptions.html", subforums=subforums)

@app.route("/newlike", methods=["post"])
def newlike():
    utils.require_login()
    utils.valid_csrf(request.form["csrf_token"])
    likes.new(request.form["positive"], request.form["link_id"], request.form["post_id"], request.form["comment_id"])
    return redirect("/")