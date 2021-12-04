from app import app
from unittest import TestCase
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test all User class in models.py"""

    def setUp(self):
        """Clean up any users in database"""
        User.query.delete()

    def tearDown(self):
        """Clean up any database transactions"""
        db.session.rollback()

    def test_get_fullname(self):
        """Method to obtain full name using method and property"""
        user = User(first_name = "Mickey", last_name = "Mouse", image_url = "https://static.wikia.nocookie.net/disney/images/b/bf/Mickey_Mouse_Disney_1.png/revision/latest/scale-to-width-down/270?cb=20180813011713")

        self.assertEqual(user.get_fullname(),"Mickey Mouse")
        self.assertEqual(user.full_name,"Mickey Mouse")
    
    def test_updateInfo(self):
        """Method to update personal info including first and last name and image URL"""
        user = User(first_name = "Minnie", last_name = "Mouse", image_url = "https://static.wikia.nocookie.net/disney/images/3/36/Minnie_Mouse_pose_.jpg/revision/latest?cb=20170709133603")

        user.updateInfo("Donald","Duck","https://static.wikia.nocookie.net/disney/images/d/db/Donald_Duck_Iconic.png/revision/latest?cb=20160905174817")

        self.assertEqual(user.first_name,"Donald")
        self.assertEqual(user.last_name,"Duck")
        self.assertEqual(user.image_url,"https://static.wikia.nocookie.net/disney/images/d/db/Donald_Duck_Iconic.png/revision/latest?cb=20160905174817")