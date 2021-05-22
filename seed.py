from models import User, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

user1 = User(first_name="Alan", last_name="Alda", image_url="https://tinyurl.com/bdph3ut8")
user2 = User(first_name="Lucille", last_name="Ball", image_url="https://tinyurl.com/ec5yurc")
user3 = User(first_name="Alan", last_name="Thicke", image_url="https://tinyurl.com/s55pv7b4")

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

db.session.commit()