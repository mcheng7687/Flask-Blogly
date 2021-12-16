"""Blogly application."""

from flask import Flask, render_template, redirect, session, request
from models import db, connect_db, User, Post, Tag, PostTag
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

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
    tags = Tag.query.all()

    return render_template("new_post.html", user_id=user_id, tags=tags)


@app.route("/users/<user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Add new post for specified user"""

    title = request.form["title"]
    content = request.form["content"]

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    tag_ids = request.form.getlist("tags")

    if tag_ids != None:
        add_tags_to_database(tag_ids, post.id)

    return redirect(f"/users/{user_id}")

@app.route("/posts/<post_id>")
def view_post(post_id):
    """View specified post"""

    post = Post.query.get_or_404(post_id)
    user = User.query.get(post.user_id)
    tags = post.tags

    return render_template("view_post.html", user=user, post=post, tags=tags)

@app.route("/posts/<post_id>/edit")
def edit_post(post_id):
    """Show edit post form"""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    tags = Tag.query.all()
    select_tags = post.tags
    
    return render_template("edit_post.html", user=user, post=post, tags=tags, select_tags=select_tags)


@app.route("/posts/<post_id>/edit", methods=["POST"])
def edit_post_database(post_id):
    """Edit post from specified user"""

    title = request.form["title"]
    content = request.form["content"]

    post = Post.query.get_or_404(post_id)
    post.updatePost(title, content)
    

    db.session.add(post)
    db.session.commit()

    tag_ids = request.form.getlist("tags")
    
    add_tags_to_database(tag_ids, post.id)

    return redirect(f"/users/{post.user_id}")

@app.route("/posts/<post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Deletes specified post from user in database"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/tags")
def show_all_tags():
    """Show all tags"""

    tags = Tag.query.all()

    return render_template("all_tags.html", tags=tags)

@app.route("/tags/new")
def new_tag():
    """Show new tag form"""
    return render_template("new_tag.html")

@app.route ("/tags/new", methods=["POST"])
def add_tag_to_database():
    """Add new tag to database"""
    
    name = request.form["name"]

    tag = Tag(name = name)

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<tag_id>")
def retrive_tag(tag_id):
    """Show tag info"""

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template("tag_info.html", tag=tag, posts=posts)

@app.route("/tags/<tag_id>/edit")
def edit_tag(tag_id):
    """Show edit tag form"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("edit_tag.html", tag=tag)

@app.route("/tags/<tag_id>/edit", methods=["POST"])
def edit_tag_database(tag_id):
    """Edit tag in database"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete tag in database"""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")

def add_tags_to_database(tag_ids, post_id):
    for tag_id in tag_ids:
        post_tag = PostTag(post_id=post_id, tag_id=tag_id)
        db.session.add(post_tag)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()