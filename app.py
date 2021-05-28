"""Blogly application."""

from flask import Flask, render_template, request, redirect
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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

""" ***** USER ROUTES ***** """
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

""" ***** POST ROUTES ***** """
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

@app.route("/posts/<int:post_id>")
def view_post(post_id):
  post = Post.query.get(post_id)
  return render_template("view_post.html", post = post)

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
  post = Post.query.get(post_id)
  return render_template("edit_post.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
  post = Post.query.get(post_id)
  req = request.form

  post.title = req['title']
  post.content = req['content']
  db.session.commit()

  return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
  user = Post.query.get(post_id).user
  Post.query.filter_by(id=post_id).delete()
  db.session.commit()
  return redirect(f"/user/{user.id}")

""" ***** TAG ROUTES ***** """
@app.route("/tags")
def view_tags():
  tags = Tag.query.all()
  return render_template("view_tags.html", tags=tags)

@app.route("/tags/new")
def new_tags():
  return render_template("new_tags.html")

@app.route("/tags/new", methods=["POST"])
def create_tags():
  req = request.form
  new_tag = Tag(name=req['new_tag'])
  db.session.add(new_tag)
  db.session.commit()

  return redirect(f"/tags/{new_tag.id}")

@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
  tag = Tag.query.get(tag_id)
  return render_template("tag_detail.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
  tag = Tag.query.get(tag_id)
  return render_template("edit_tags.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
  tag = Tag.query.get(tag_id)
  req = request.form
  tag.name = req['updated_tag']
  db.session.commit()
  return redirect(f"/tags/{tag.id}")