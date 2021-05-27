from flask_sqlalchemy import SQLAlchemy

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

    posts = db.relationship('Post', backref='posts', cascade="all, delete")

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