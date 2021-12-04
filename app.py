"""Blogly application."""

from flask import Flask, render_template, redirect, session, request
from models import db, connect_db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

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

    first = request.form['first_name']
    last = request.form['last_name']
    url = request.form['image_url']

    user = User(first_name = first, last_name = last, image_url = url)

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<id>")
def get_user(id):
    """Getting specified user information"""

    user = User.query.get_or_404(id)

    return render_template("user_info.html",user=user)

@app.route("/users/<id>/edit")
def edit_user(id):
    """Edit specified user information"""

    user = User.query.get_or_404(id)

    return render_template("edit_user.html",user=user)

@app.route("/users/<id>/edit", methods=["POST"])
def edit_user_database(id):
    """Edit specified user information in database"""

    user = User.query.get(id)

    first = request.form['first_name']
    last = request.form['last_name']
    url = request.form['image_url']

    user.updateInfo(first, last, url)

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<id>/delete", methods=["POST"])
def delete_user(id):
    """Deletes specified user in database"""

    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
