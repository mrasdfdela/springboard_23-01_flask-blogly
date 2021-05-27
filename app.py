"""Blogly application."""

from flask import Flask, render_template, request, redirect
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = "jerrys_secret"
# debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route("/")
def home():
  return redirect("/users")


@app.route("/users")
def user_listing():
  users = User.get_all_users()
  return render_template("users.html", users=users)


@app.route("/users/new")
def new_user_form():
  return render_template("new_user.html")


@app.route("/users/new", methods=['POST'])
def new_user_post():
  req = request.form
  first_name = req['first_name']
  last_name = req['last_name']
  image_url = req['image_url']

  user = User(first_name=first_name, last_name=last_name, image_url=image_url)
  db.session.add(user)
  db.session.commit()
  return redirect(f"/user/{user.id}>")


@app.route("/user/<int:user_id>")
def user_detail(user_id):
  user = User.query.get(user_id)
  return render_template("user_detail.html",user=user)


@app.route("/user/<int:user_id>/edit")
def edit_user_form(user_id):
  user = User.query.get(user_id)
  return render_template("edit_user.html",user=user)


@app.route("/user/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
  req = request.form
  first_name = req['first_name']
  last_name = req['last_name']
  image_url = req['image_url']

  user = User.query.get(user_id)
  user.first_name = first_name
  user.last_name = last_name
  user.image_url = image_url

  db.session.commit()
  return redirect(f"/user/{user.id}")


@app.route("/user/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
  User.query.filter_by(id=user_id).delete()

  db.session.commit()
  return redirect(f"/users")

@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
  user = User.query.get(user_id)
  return render_template("new_post.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post(user_id):
  req = request.form
  title = req['title']
  content = req['content']

  new_post = Post(title=title, content=content,user_id=user_id)
  db.session.add(new_post)
  db.session.commit()
  return redirect(f"/user/{user_id}")