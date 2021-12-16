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
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(20),
                     nullable = False)
    last_name = db.Column(db.String(20),
                     nullable = False)
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

class Post (db.Model):
    """Post class"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.String(),
                        nullable = False)
    content = db.Column(db.String(),
                        nullable = False)
    created_at = db.Column(db.DateTime, default = db.func.current_timestamp())
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'))
    user = db.relationship('User', 
                        backref = 'posts')
    tags = db.relationship('Tag',
                        secondary = 'post_tag',
                        backref = 'posts')

    @classmethod
    def get_all_user_posts(cls, user_id):
        return cls.query.filter(Post.user_id == user_id).order_by(Post.created_at.desc()).all()

    def updatePost(self, new_title, new_content):
        self.title = new_title
        self.content = new_content
        self.created_at = db.func.current_timestamp()

    def __repr__(self):
        return f"<Post object id={self.id} title={self.title} content={self.content}>"

class Tag (db.Model):
    """Tag class"""

    __tablename__="tags"

    id = db.Column(db.Integer,
                primary_key = True,
                autoincrement = True)
    name = db.Column(db.String(),
                    nullable = False)

    def __repr__(self):
        return f"<Tag object id={self.id} name={self.name}>"

class PostTag (db.Model):
    """Post/Tag class to join Post and Tag classes"""

    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer,
            db.ForeignKey('posts.id'),
            primary_key = True)
    tag_id = db.Column(db.Integer,
            db.ForeignKey('tags.id'),            
            primary_key = True)