from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import ForeignKey

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    """ the User model """

    __tablename__ = "users"

    id = db.Column(
      db.Integer,
      primary_key = True,
      autoincrement = True)

    first_name = db.Column(
      db.String(50),
      nullable = False
    )

    last_name = db.Column(
      db.String(50),
      nullable = False
    )
    
    image_url = db.Column(
      db.String(200),
      nullable = False
    )

    posts = db.relationship('Post', backref='user', cascade="all, delete")

    @classmethod
    def get_all_users(cls):
      return cls.query.all();

class Post(db.Model):
  """ the Post model """

  __tablename__ = "posts"

  id = db.Column(
    db.Integer,
    primary_key = True,
    autoincrement = True)

  title = db.Column(
    db.String(200),
    nullable = False
  )

  content = db.Column (
    db.String(1000),
    nullable = False
  )

  created_at = db.Column (
    db.DateTime(),
    server_default=db.func.now()
  )

  user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id'),
    nullable=False
  )

class Tag(db.Model):
  """ the Tag model """

  __tablename__ = "tags"

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)

  name = db.Column(db.Text, nullable = False)

  posts = db.relationship(
    'Post',
    secondary="post_tags",
    backref='tags'
  )

class PostTag(db.Model):
  """ join table for Post and Tag models """

  __tablename__ = "post_tags"

  post_id = db.Column(
                db.Integer, 
                db.ForeignKey('posts.id'),
                primary_key=True,
                nullable=False)
  tag_id = db.Column(
                db.Integer, 
                db.ForeignKey('tags.id'),
                primary_key=True,
                nullable=False)