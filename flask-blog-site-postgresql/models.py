from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy with no parameters. Will be configured later with the Flask app.
db = SQLAlchemy()


class Post(db.Model):
    """
    Represents a post in the blog.

    Attributes:
       id (Integer): Unique identifier for the post.
       title (String): Title of the post, limited to 100 characters, cannot be null.
       content (Text): Content of the post, cannot be null.
       image_url (String): URL of an image associated with the post, limited to 500 characters.
       user_id (Integer): Foreign key linking to the user who created the post.
       comments (relationship): Defines a one-to-many relationship with the Comment model.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Post {self.id}'


class User(db.Model):
    """
    Represents a user in the blog.

    Attributes:
        id (Integer): Unique identifier for the user.
        email (String): Email of the user, must be unique, limited to 100 characters, cannot be null.
        password (String): Hashed password for the user, limited to 500 characters, cannot be null.
        is_blacklisted (Boolean): Flag to indicate if the user is blacklisted.
        is_admin (Boolean): Flag to indicate if the user is an admin.
        comments (relationship): Defines a one-to-many relationship with the Comment model.
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100),unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    is_blacklisted = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __repr__(self):
        return f'User {self.email}'

    def set_password(self,password):
        """
        Sets the user's password, which is stored as a hash.

        Args:
            password (str): The plaintext password to hash and store.
        """

        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks the given password against the user's stored password hash.

        Args:
            password (str): The plaintext password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """

        return check_password_hash(self.password, password)


class Comment(db.Model):
    """
    Represents a comment on a post in the blog.

    Attributes:
        id (Integer): Unique identifier for the comment.
        text (Text): Content of the comment, cannot be null.
        user_id (Integer): Foreign key linking to the user who created the comment.
        post_id (Integer): Foreign key linking to the post the comment belongs to.
        created_at (DateTime): Timestamp of when the comment was created.
    """

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Comment {self.id}>'