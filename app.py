"""Blogly application."""

from flask import Flask, render_template, request
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = "jerrys_secret"
# debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route("/")
def user_listing():
  users = User.get_all_users()
  return render_template("users.html", users=users)

@app.route("/new_user")
def new_user():
  return render_template("new_user.html")