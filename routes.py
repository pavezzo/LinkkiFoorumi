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
    return render_template("all.html", items=results, index=True)

@app.route("/top", methods=["GET"])
def index_top():
    results = subscriptions.get_users_content_top()
    return render_template("all.html", items=results, index=True)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        if len(request.form["username"]) < 4 or len(request.form["password"]) < 4:
            return render_template("error.html", error="too short username or password")

        if "admin" in request.form:
            if users.register(request.form["username"], request.form["password"], True):
                return redirect("/")
            else:
                return render_template("error.html", error="username is already taken")
        else:
            if users.register(request.form["username"], request.form["password"], False):
                return redirect("/")
            else:
                return render_template("error.html", error="username already taken")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        if users.login(request.form["username"], request.form["password"]):
            return redirect("/")
        else:
            return render_template("error.html", error="invalid username or password")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/newlink", methods=["GET", "POST"])
def newlink():
    if request.method == "GET":
        subs = subforums.get_subforums()
        return render_template("newlink.html", default=request.args.get("subforum"), subs=subs)

    if request.method == "POST":
        utils.require_login()
        utils.valid_csrf(request.form["csrf_token"])
        link_id = links.new(request.form["sub_name"], request.form["title"], request.form["link"])
        if link_id:
            return redirect("/link/"+str(link_id))
        else:
            return render_template("error.html", error="invalid submission")

@app.route("/link/<int:id>")
def link(id):
    result = links.get(id)

    if not result:
        return render_template("error.html", error="link doesn't exist")

    comms = comments.get_for_link(id)
    return render_template("link.html", link=result, comments=comms)

@app.route("/newpost", methods=["GET", "POST"])
def new_post():
    if request.method == "GET":
        subs = subforums.get_subforums()
        return render_template("newpost.html", default=request.args.get("subforum"), subs=subs)

    if request.method == "POST":
        utils.require_login()
        utils.valid_csrf(request.form["csrf_token"])
        post_id = text_posts.new(request.form["sub_name"], request.form["title"], request.form["post_content"])
        if post_id:
            return redirect("/post/" + str(post_id))
        else:
            return render_template("error.html", error="invalid submission")

@app.route("/post/<int:id>")
def post(id):
    result = text_posts.get(id)

    if not result:
        return render_template("error.html", error="post doesn't exist")

    comms = comments.get_for_post(id)
    return render_template("post.html", post=result, comments=comms)

@app.route("/sub/all")
def all_newest():
    results = all.get_newest()
    return render_template("all.html", items=results)

@app.route("/sub/all/top")
def all_top():
    results = all.get_most_liked()
    return render_template("all.html", items=results)

@app.route("/newcomment", methods=["POST"])
def new_comment():
    utils.require_login()
    utils.valid_csrf(request.form["csrf_token"])
    if comments.new(request.form["link_id"], request.form["post_id"], request.form["parent"],
                request.form["comment"]):
        return redirect(request.referrer)
    else:
        return render_template("error.html", error="invalid submission")

@app.route("/newsubforum", methods=["GET", "POST"])
def new_subforum():
    if request.method == "GET":
        return render_template("newsubforum.html")
    if request.method == "POST":
        utils.require_login()
        utils.valid_csrf(request.form["csrf_token"])
        if subforums.new(request.form["sub_name"], request.form["introduction"]):
            return redirect("/sub/" + str(request.form["sub_name"]))
        else:
            return render_template("error.html", error="Invalid specifications. Maybe the subforum already exists?")

@app.route("/sub/<string:name>")
def view_subforum(name):
    result = subforums.get_by_name(name)
    if not result:
        abort(404)
    subbed = subscriptions.check_subscription(result.sub_id)
    contents = subforums.get_newest(result.sub_id)
    return render_template("subforum.html", subforum_id=result.sub_id, sub_name=name, introduction=result.introduction, contents=contents, subbed=subbed)

@app.route("/sub/<string:name>/top")
def view_subforum_top(name):
    result = subforums.get_by_name(name)
    subbed = subscriptions.check_subscription(result.sub_id)
    if not result:
        abort(404)
    contents = subforums.get_top(result.sub_id)
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
    return redirect(request.referrer)

@app.route("/subscriptions", methods=["get"])
def show_subscriptions():
    utils.require_login()
    subforums = subscriptions.get_users_subscriptions()
    return render_template("subscriptions.html", items=subforums)

@app.route("/newlike", methods=["post"])
def newlike():
    utils.require_login()
    utils.valid_csrf(request.form["csrf_token"])
    if likes.new(request.form["positive"], request.form["link_id"], request.form["post_id"], request.form["comment_id"]):
        return redirect(request.referrer)
    else:
        return render_template("error.html", error="Invalid like form")

@app.route("/deletepost", methods=["post"])
def deletepost():
    utils.require_login()
    utils.valid_csrf(request.form["csrf_token"])
    post = text_posts.get(request.form["post_id"])

    if not post:
        return render_template("error.html", error="Post doesn't exist")

    if post.user_id == session["user_id"] or session["admin"]:
        text_posts.delete(request.form["post_id"])
        return redirect(request.referrer)
    else:
        return render_template("error.html", error="You don't have the rights to delete this post")

@app.route("/deletelink", methods=["post"])
def deletelink():
    utils.require_login()
    utils.valid_csrf(request.form["csrf_token"])
    link = links.get(request.form["link_id"])

    if not link:
        return render_template("error.html", error="Link doesn't exist")

    if link.user_id == session["user_id"] or session["admin"]:
        links.delete(request.form["link_id"])
        return redirect("/")
    else:
        return render_template("error.html", error="You don't have the rights to delete this link")

@app.route("/deletecomment", methods=["post"])
def deletecomment():
    utils.require_login()
    utils.valid_csrf(request.form["csrf_token"])
    comment = comments.get(request.form["comment_id"])

    if not comment:
        return render_template("error.html", error="Comment doesn't exist")
    
    if comment.user_id == session["user_id"] or session["admin"]:
        comments.delete(request.form["comment_id"])
        return redirect(request.referrer)
    else:
        return render_template("error.html", error="You don't have the rights to delete this comment")

@app.route("/subforums", methods=["get"])
def get_subforums():
    subs = subforums.get_subforums()
    return render_template("subforums.html", items=subs)
