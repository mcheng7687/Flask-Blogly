from app import app
from unittest import TestCase
from flask import session
from models import db, User, Post, PostTag, Tag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()


class BloglyTestCase(TestCase):
    """Test all functions in blogly app.py"""

    def setUp(self):
        """Clean up any users in database and add new user"""
        User.query.delete()
        user = User(id=2, first_name = "Goofy", last_name = "Goof", image_url = "https://static.wikia.nocookie.net/disney/images/2/27/Goofy_transparent.png")

        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """Clean up any database transactions"""
        db.session.rollback()

    def test_homepage(self):
        """Test home page redirected to users page"""
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code,302)
            self.assertEqual(res.location, "http://localhost/users")

    def test_users_page(self):
        """Test users page"""
        with app.test_client() as client:
            res = client.get("/users")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code,200)
            self.assertIn('Users:',html)
            self.assertIn('Goofy Goof',html)

    def test_new_user(self):
        """Test new user page"""
        with app.test_client() as client:
            res = client.get("/users/new")
            html = res.get_data(as_text = True)       

            self.assertEqual(res.status_code,200)
            self.assertIn('<form action="/users/new" method="POST">',html)

    def test_add_user(self):
        """Test add user to PostgreSQL database"""
        with app.test_client() as client:
            res = client.post("/users/new", data={'first_name':'Mickey', 'last_name':'Mouse', 'image_url':'https://static.wikia.nocookie.net/disney/images/b/bf/Mickey_Mouse_Disney_1.png'}, follow_redirects = True)
            html = res.get_data(as_text = True)       

            self.assertEqual(res.status_code,200)
            self.assertIn('Mickey Mouse</a></li>',html)

    def test_get_user(self):
        """Test user info page"""
        with app.test_client() as client:
            res = client.get("/users/2")
            html = res.get_data(as_text = True)       

            self.assertEqual(res.status_code,200)
            self.assertIn('Full Name:',html)
            self.assertIn('Goofy Goof',html)

    def test_edit_user(self):
        """Test edit user info page"""
        with app.test_client() as client:
            res = client.get("/users/2/edit")
            html = res.get_data(as_text = True)       

            self.assertEqual(res.status_code,200)
            self.assertIn('<form action="/users/2/edit" method="POST">',html)
            self.assertIn('<input type="text" name="first_name" placeholder="First Name" value="Goofy" required>',html)

    def test_edit_user_info(self):
        """Test update to user info in PostgreSQL database"""
        with app.test_client() as client:
            res = client.post("/users/2/edit", data={'first_name':'Minnie', 'last_name':'Mouse', 'image_url':'https://static.wikia.nocookie.net/disney/images/3/36/Minnie_Mouse_pose_.jpg'}, follow_redirects = True)
            html = res.get_data(as_text = True)       

            self.assertEqual(res.status_code,200)
            self.assertIn('<li><a href="/users/2"> Minnie Mouse</a></li>',html)

    def test_delete_user(self):
        """Test delete user in PostgreSQL database"""
        with app.test_client() as client:
            res = client.post("/users/2/delete", follow_redirects = True)
            html = res.get_data(as_text = True)       

            self.assertEqual(res.status_code,200)
            self.assertIn('Users:',html)

    def test_new_post(self):
        """Test new post form"""
        with app.test_client() as client:
            res = client.get("/users/2/posts/new")
            html = res.get_data(as_text = True)       

            self.assertEqual(res.status_code,200)
            self.assertIn('<h1>Add a New Post</h1>',html)

    def test_add_post(self):
        with app.test_client() as client:
            res = client.post("/users/1/posts/new", data={'title':'My BFF', 'content':'Micky is my BFF', 'user_id':'2'}, follow_redirects = True)
            html = res.get_data(as_text = True)       

            # self.assertEqual(res.status_code,200)
            # self.assertIn('Goofy Goof',html)