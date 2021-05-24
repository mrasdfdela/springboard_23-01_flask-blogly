from app import app
from models import db, User
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

class NewFormTestCase(TestCase):
    def test_render_form(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Create a User</h1>", html)

class DetailTestCase(TestCase):
    def test_user_detail(self):
        with app.test_client() as client:
            res = client.get('/user/1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Alan Alda</h1>", html)

class NewTestCase(TestCase):
    def setUp(self):
        new_user = User(
          first_name="Barbara", 
          last_name="Streisand",
          image_url="https://bit.ly/3wmPXIS")
        db.session.add(new_user)
        db.session.commit()
        self.pet_id = new_user.id

    def tearDown(self):
        User.query.filter_by(id=self.pet_id).delete()
        db.session.commit()

    def test_new_user(self):
        with app.test_client() as client:
            res = client.get(f'/user/{self.pet_id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Barbara Streisand</h1>", html)