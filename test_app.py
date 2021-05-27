from app import app
from models import db, User, Post
from unittest import TestCase

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

class HomeTestCase(TestCase):
    def test_home_redirect(self):
        with app.test_client() as client:
            res = client.get('/')

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/users')

    def test_home_page(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)

class NewUserFormTestCase(TestCase):
    def test_render_form(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Create a User</h1>", html)

class UserDetailTestCase(TestCase):
    def test_user_detail(self):
        with app.test_client() as client:
            res = client.get('/user/1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Alan Alda</h1>", html)

class NewUserTestCase(TestCase):
    def setUp(self):
        self.user_id = addBarbara()

    def tearDown(self):
        User.query.filter_by(id=self.user_id).delete()
        db.session.commit()

    def test_new_user(self):
        with app.test_client() as client:
            res = client.get(f'/user/{self.user_id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Barbara Streisand</h1>", html)

def addBarbara():
    new_user = User(
              first_name="Barbara", 
              last_name="Streisand",
              image_url="https://bit.ly/3wmPXIS")
    db.session.add(new_user)
    db.session.commit()
    return new_user.id

def addPost(user_id):
    new_post = Post(
      title = "Love",
      content = "Soft as an easy chair",
      user_id = user_id
    )
    db.session.add(new_post)
    db.session.commit()
    return new_post.id

class NewPostTestCase(TestCase):
    def setUp(self):
        self.user_id = addBarbara()
        # self.post_id = addPost(self.user_id)
    def tearDown(self):
        Post.query.filter_by(user_id=self.user_id).delete()
        User.query.filter_by(id=self.user_id).delete()
        db.session.commit()
    
    def test_new_post_form(self):
        with app.test_client() as client:
            res = client.get(f"/users/{self.user_id}/posts/new")
            user = User.query.filter_by(id=self.user_id).first()
            fname = user.first_name
            lname = user.last_name
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f"<h1>Add Post for {fname} {lname}", html)
    
    def test_new_post(self):
        with app.test_client() as client:
            title = 'I am a woman in love'
            res = client.post(
              f'/users/{self.user_id}/posts/new',
              data = {
                'title': title,
                'content': 'What do I do?',
                'user_id': self.user_id
              },
              follow_redirects=True
            )
        html = res.get_data(as_text=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn(f'>{title}</a>',html)
    
    def test_edit_post(self):
        with app.test_client() as client:
            self.post_id = addPost(self.user_id)
            new_title = "Edited Title"
            res = client.post(
              f'/posts/{self.post_id}/edit',
              data = {
                'title': new_title,
                'content': "Edited Content"
              },
              follow_redirects=True
            )
        html = res.get_data(as_text=True)
        
        self.assertEqual(res.status_code,200)
        self.assertIn(f'<h1>{new_title}</h1>',html)
  
    def test_delete_post(self):
        user = User.query.get(self.user_id)
        fname = user.first_name
        lname = user.last_name

        with app.test_client() as client:
            self.post_id = addPost(self.user_id)
            res = client.post(
              f'/posts/{self.post_id}/delete',
              follow_redirects=True
            )
        html = res.get_data(as_text=True)
        self.assertIn(f'<h1>{fname} {lname}</h1>',html)