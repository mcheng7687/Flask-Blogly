from app import app
from unittest import TestCase
from models import db, User, Post, PostTag, Tag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test User class in models.py"""

    def setUp(self):
        """Clean up any users in database"""
        User.query.delete()

    def tearDown(self):
        """Clean up any database transactions"""
        db.session.rollback()

    def test_get_fullname(self):
        """Method to obtain full name using method and property"""
        user = User(first_name = "Mickey", last_name = "Mouse", image_url = "https://static.wikia.nocookie.net/disney/images/b/bf/Mickey_Mouse_Disney_1.png")

        self.assertEqual(user.get_fullname(),"Mickey Mouse")
        self.assertEqual(user.full_name,"Mickey Mouse")
    
    def test_updateInfo(self):
        """Method to update personal info including first and last name and image URL"""
        user = User(first_name = "Minnie", last_name = "Mouse", image_url = "https://static.wikia.nocookie.net/disney/images/3/36/Minnie_Mouse_pose_.jpg")

        user.updateInfo("Donald","Duck","https://static.wikia.nocookie.net/disney/images/d/db/Donald_Duck_Iconic.png")

        self.assertEqual(user.first_name,"Donald")
        self.assertEqual(user.last_name,"Duck")
        self.assertEqual(user.image_url,"https://static.wikia.nocookie.net/disney/images/d/db/Donald_Duck_Iconic.png")

class PostModelTestCase(TestCase):
    """Test Post class in models.py"""

    def setUp(self):
        """Clean up any posts in database"""
        User.query.delete()
        Post.query.delete()

        user1 = User(id = 1, first_name = "Mickey", last_name = "Mouse", image_url = "https://static.wikia.nocookie.net/disney/images/b/bf/Mickey_Mouse_Disney_1.png")
        user2 = User(id = 2, first_name = "Minnie", last_name = "Mouse", image_url = "https://static.wikia.nocookie.net/disney/images/3/36/Minnie_Mouse_pose_.jpg")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        """Clean up any database transactions"""
        db.session.rollback()

    def test_get_all_user_posts(self):
        """Test class method to get all specified user's posts"""
        # user = User(id = 1, first_name = "Minnie", last_name = "Mouse", image_url = "https://static.wikia.nocookie.net/disney/images/3/36/Minnie_Mouse_pose_.jpg")
        post1 = Post(id = 1, title = "Where am I?", content = "With Waldo", user_id = 1)
        post2 = Post(id = 2, title = "Do I love Minnie?", content = "I do", user_id = 1)

        # db.session.add(user)
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()

        user = User.query.filter_by(first_name = "Minnie").one()

        posts = Post.get_all_user_posts(user.id)

        self.assertEqual(posts[0].title,"Where am I?")
        self.assertEqual(posts[0].content,"With Waldo")
        self.assertEqual(posts[1].title,"Do I love Minnie?")
        self.assertEqual(posts[1].content,"I do")

    def test_updatePost(self):
        """Test method to update post"""

        post = Post(title = "PB&J", content = "I love peanut butter and jelly", user_id = 1)

        # db.session.add(post)
        # db.session.commit()

        # post = Post.query.one()
        post.updatePost("Sandwiches", "I love ham sandwiches")

        self.assertEqual(post.title,"Sandwiches")
        self.assertEqual(post.content,"I love ham sandwiches")

class PostTagModelTestCase(TestCase):
    """Test PostTag class in models.py"""

    def setUp(self):
        """Clean up any users, posts, tags, and post-tags in database"""
        User.query.delete()
        Post.query.delete()
        Tag.query.delete()        
        PostTag.query.delete()

    def tearDown(self):
        """Clean up any database transactions"""
        db.session.rollback()

    def test_PostTag_class(self):
        """Test M2M relationship"""
        
        post1 = Post(id = 1, title = "Pluto", content = "Mouse's best friend", user_id = 1)
        post2 = Post(id = 2, title = "My wife", content = "Minnie is the love of my life", user_id = 1)
        post3 = Post(id = 3, title = "Where is his pants?", content = "Donald is always missing pants", user_id = 2)

        tag1 = Tag(id = 1, name = "Truth")
        tag2 = Tag(id = 2, name = "BFF")
        tag3 = Tag(id = 3, name = "Love")

        post_tag1 = PostTag(post_id = 1, tag_id = 1)
        post_tag2 = PostTag(post_id = 1, tag_id = 2)
        post_tag3 = PostTag(post_id = 2, tag_id = 2)
        post_tag4 = PostTag(post_id = 2, tag_id = 3)
        post_tag5 = PostTag(post_id = 3, tag_id = 1)

        # db.session.add(user1)
        # db.session.add(user2)
        # post1, post2, post3, tag1, tag2, tag3, post_tag1, post_tag2, post_tag3, post_tag4, post_tag5)
        # db.session.commit()