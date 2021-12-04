"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User (db.Model):
    """User class"""

    __tablename__ = "user"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(20),
                     nullable=False)
    last_name = db.Column(db.String(20),
                     nullable=False)
    image_url = db.Column(db.String())

    def __repr__(self):
        return f'<User object id={self.id} first={self.first_name} last={self.last_name} URL={self.image_url}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_fullname(self):
        return f'{self.first_name} {self.last_name}'

    def updateInfo(self,new_first,new_last,new_url):
        self.first_name = new_first
        self.last_name = new_last
        self.image_url = new_url