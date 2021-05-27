from models import User, Post, db
from app import app

db.drop_all()
# Post.__table__.drop(db.engine)
# db.session.commit()
# User.__table__.drop(db.engine)
db.create_all()

user1 = User(first_name="Alan", last_name="Alda", image_url="https://tinyurl.com/bdph3ut8")
user2 = User(first_name="Lucille", last_name="Ball", image_url="https://tinyurl.com/ec5yurc")
user3 = User(first_name="Alan", last_name="Thicke", image_url="https://tinyurl.com/s55pv7b4")

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

db.session.commit()

post1 = Post(
  title="Hello world!", 
  content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam elementum orci massa, nec elementum nisi suscipit ut. Aliquam vitae dignissim.",
  user_id=1
  )

db.session.add_all([post1])
db.session.commit()