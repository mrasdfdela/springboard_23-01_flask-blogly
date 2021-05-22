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

    @classmethod
    def get_all_users(cls):
      return cls.query.all();