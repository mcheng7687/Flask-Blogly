"""Blogly application."""

from flask import Flask, render_template, redirect, session, request
from models import db, connect_db, User, Post


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()


@app.route("/")
def home():
    """Home page"""
    return redirect("/users")


@app.route("/users")
def get_all_users():
    """Webpage with users listed"""

    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template("users.html", users=users)


@app.route("/users/new")
def new_user():
    """Show new user form"""

    return render_template("new_user.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Add new user to database and redirect to users page"""

    first = request.form["first_name"]
    last = request.form["last_name"]
    url = request.form["image_url"]

    user = User(first_name=first, last_name=last, image_url=url)

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<id>")
def get_user(id):
    """Getting specified user information"""

    user = User.query.get_or_404(id)
    posts = Post.get_all_user_posts(id)

    return render_template("user_info.html", user=user, posts=posts)


@app.route("/users/<id>/edit")
def edit_user(id):
    """Edit specified user information"""

    user = User.query.get_or_404(id)

    return render_template("edit_user.html", user=user)


@app.route("/users/<id>/edit", methods=["POST"])
def edit_user_database(id):
    """Edit specified user information in database"""

    user = User.query.get_or_404(id)

    first = request.form["first_name"]
    last = request.form["last_name"]
    url = request.form["image_url"]

    user.updateInfo(first, last, url)

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<id>/delete", methods=["POST"])
def delete_user(id):
    """Deletes specified user in database"""

    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<user_id>/posts/new")
def new_post(user_id):
    """Show new post form"""

    return render_template("new_post.html", user_id=user_id)


@app.route("/users/<user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Add new post for specified user"""

    title = request.form["title"]
    content = request.form["content"]

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<post_id>")
def view_post(post_id):
    """View specified post"""

    post = Post.query.get_or_404(post_id)
    user = User.query.get(post.user_id)

    return render_template("view_post.html", user=user, post=post)

@app.route("/posts/<post_id>/edit")
def edit_post(post_id):
    """Show edit post form"""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    
    return render_template("edit_post.html", user=user, post=post)


@app.route("/posts/<post_id>/edit", methods=["POST"])
def edit_post_database(post_id):
    """Edit post from specified user"""

    title = request.form["title"]
    content = request.form["content"]

    post = Post.query.get_or_404(post_id)
    post.updatePost(title, content)
    user_id = post.user_id

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Deletes specified post from user in database"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")