from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, InputRequired


class PostForm(FlaskForm):
    """
    Form class for creating a new post.
        - title: Title of the post, required field.
        - content: Content of the post, required field.
        - image_url: URL of an image for the post, optional field.
        - submit: Submit button for the form.
    """

    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])
    image_url = StringField('Image URL')  # This is the field for the image URL
    submit = SubmitField('Create Post')


class CommentForm(FlaskForm):
    """
    Form class for submitting a comment.
        - text: Text of the comment, required field.
        - submit: Submit button for the form.
    """

    text = StringField('Comment', validators=[InputRequired()])
    submit = SubmitField('Post Comment')


class RegistrationForm(FlaskForm):
    """
    Form class for user registration.
        - email: Email address of the user, required field and validated for email format.
        - password: Password for the account, required field with length constraints.
        - submit: Submit button for the form.
    """

    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=50)])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """
    Form class for user login.
        - email: Email address of the user, required field and validated for email format.
        - password: Password for the account, required field with length constraints.
        - submit: Submit button for the form.
    """

    email = StringField('Email',validators=[InputRequired(), Email()])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=5,max=50)])
    submit = SubmitField('Login')
