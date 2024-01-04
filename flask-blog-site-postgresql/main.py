import os  # Interacting with the operating system

# Flask framework and extensions
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_bootstrap import Bootstrap4  # Bootstrap 4 integration for Flask
from flask_moment import Moment  # Handling dates and times in templates
from flask_talisman import Talisman  # Security headers for Flask

# Application modules
from forms import PostForm, CommentForm, LoginForm, RegistrationForm  # Form handling
from models import Post, User, Comment, db  # Database models


def create_app():
    """
    Create and configure the Flask application instance.

    Initializes the Flask application with necessary configurations.
    Sets the secret key and the database URI from environment variables.


    Returns:
        app: The initialized Flask application instance.
    """

    app = Flask(__name__)

    # SECRET_KEY: A secret key used by Flask for securely signing the session cookie.
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI: Database URI for SQLAlchemy to connect to the database.
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

    db.init_app(app)  # Initializing the database with the app.
    bootstrap = Bootstrap4(app)  # Initializing Bootstrap4 with the app for front-end styling.
    moment = Moment(app) # Initializing Moment with the app for handling dates and times.
    Talisman(app, content_security_policy=None) # Initializing Talisman for enhanced security headers.

    # Error handler for 404 Not Found
    @app.errorhandler(404)
    def not_found_error(error):
        """
        Handle 404 Not Found errors by displaying a custom page.

        Args:
            error: The error object.

        Returns:
            Response object with custom 404 page and status code.
        """

        return render_template('404.html'), 404

    # Error handler for 500 Internal Server Error
    @app.errorhandler(500)
    def internal_error(error):
        """
        Handle 500 Internal Server Error by performing a rollback and displaying a custom page.

        Args:
            error: The error object.

        Returns:
            Response object with custom 500 page and status code.
        """

        db.session.rollback()
        return render_template('500.html'), 500

    # Context processor to inject the admin status into templates
    @app.context_processor
    def inject_admin_status():
        is_admin = False
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            is_admin = user is not None and user.is_admin
        return dict(is_admin=is_admin)

    # Create all database tables
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        """
        Route for the home page. Retrieves all posts from the database
        and displays them on the index page.
        """

        posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template('index.html', posts=posts)

    @app.route('/about')
    def about():
        """
        Route for the about page. Info about the project
        and a link to the GitHub repository.
        """

        return render_template('about.html')

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        """
        Login route. Handles user authentication.
        Redirects to home if the user is already logged in.
        On successful login, redirects to the home page.
        On failure, flashes an error message.
        """

        if 'user_id' in session:
            return redirect(url_for('home'))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                session['user_id'] = user.id
                return redirect(url_for('home'))
            else:
                flash('Invalid email or password', 'danger')
        return render_template('login.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """
        Registration route. Handles new user registration.
        Redirects to home if the user is already logged in.
        On successful registration, redirects to the login page.
        On failure, flashes an error message.
        """

        if 'user_id' in session:
            return redirect(url_for('home'))

        form = RegistrationForm()

        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()

            if existing_user:
                flash('Email address already in use!', 'danger')
                return render_template('register.html', form=form)

            is_first_user = User.query.count() == 0

            new_user = User(
                email=form.email.data,
                is_admin=is_first_user
            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html', form=form)

    @app.route('/logout')
    def logout():
        """
        Logout route. Clears the user session and redirects to the home page.
        """

        session.pop('user_id',None)
        return redirect(url_for('home'))

    @app.route('/post_<int:post_id>', methods=['GET', 'POST'])
    def get_post(post_id):
        """
        Route for displaying a specific post and its comments.
        Handles comment submission.
        On successful comment submission, redirects to the same post page.
        On failure, flashes an error message.
        Blocks users from posting more than one comment to avoid spam.
        Prevents blacklisted users from commenting.
        """

        post = Post.query.get_or_404(post_id)
        comments = Comment.query.filter_by(post_id=post.id).join(User).all()
        form = CommentForm()

        user = None
        if 'user_id' in session:
            user = User.query.get(session['user_id'])

        is_admin = user is not None and user.is_admin

        if form.validate_on_submit() and 'user_id' in session:
            if user.is_blacklisted:
                flash("You are blocked from commenting.", "danger")
                return redirect(url_for('get_post', post_id=post_id))

            if not is_admin:
                existing_comment = Comment.query.filter_by(user_id=session['user_id'], post_id=post.id).first()
                if existing_comment:
                    flash('You have already commented on this post', 'info')
                    return redirect(url_for('get_post', post_id=post_id))

            comment = Comment(text=form.text.data, user_id=session['user_id'], post_id=post.id)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been added.', 'success')
            return redirect(url_for('get_post', post_id=post_id))

        return render_template('post.html', user=user, post=post, comments=comments, form=form, is_admin=is_admin)

    @app.route('/create_post', methods=['GET', 'POST'])
    def create_post():
        """
        Route for creating new posts. Restricted to logged-in admins.
        Displays a form for post creation. On successful post creation,
        flashes a success message and redirects to the home page.
        """

        if 'user_id' not in session:
            flash('You need to be logged in to create posts.', 'info')
            return redirect(url_for('login'))

        current_user = User.query.get(session['user_id'])
        if current_user is None or not current_user.is_admin:
            flash('Only admins can create posts.', 'danger')
            return redirect(url_for('home'))

        form = PostForm()
        if form.validate_on_submit():
            new_post = Post(title=form.title.data, content=form.content.data, image_url=form.image_url.data)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully.', 'success')
            return redirect(url_for('home'))

        return render_template('create_post.html', form=form)

    @app.route('/delete_comment/<int:post_id>/<int:comment_id>')
    def delete_comment(post_id, comment_id):
        """
        Route to delete a comment. Users can only delete their own comments.
        On successful deletion, flashes a success message and redirects to the post page.
        """

        if 'user_id' not in session:
            flash('You need to be logged in to delete comments.', 'danger')
            return redirect(url_for('login'))

        comment = Comment.query.get_or_404(comment_id)
        if comment.user_id != session['user_id']:
            flash('You can only delete your own comments.', 'danger')
            return redirect(url_for('get_post', post_id=post_id))

        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted.', 'success')
        return redirect(url_for('get_post', post_id=post_id))

    @app.route('/delete_post/<int:post_id>',methods=['GET','POST'])
    def delete_post(post_id):
        """
        Route to delete a post. Restricted to logged-in admins.
        On successful deletion, flashes a success message and redirects to the home page.
        """

        if 'user_id' not in session:
            flash('You need to be logged in delete posts.','info')
            return redirect(url_for('login'))

        current_user = User.query.get(session['user_id'])
        if current_user is None or not current_user.is_admin:
            flash('Only admins can delete posts.','danger')
            return redirect(url_for('home'))

        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully.','success')
        return redirect(url_for('home'))

    @app.route('/edit_post/<int:post_id>',methods=['GET','POST'])
    def edit_post(post_id):
        """
        Route to edit a post. Restricted to logged-in admins.
        Displays a form pre-filled with post data. On successful edit,
        flashes a success message and redirects to the updated post page.
        """

        post = Post.query.get_or_404(post_id)

        if 'user_id' not in session:
            flash('You need to be logged in to edit posts','info')
            return redirect(url_for('login'))

        current_user = User.query.get(session['user_id'])
        if current_user is None or not current_user.is_admin:
            flash('Only admins can edit posts.','danger')
            return redirect(url_for('home'))

        form = PostForm(obj=post)

        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            post.image_url = form.image_url.data
            db.session.commit()
            flash('Post updated successfully.','success')
            return redirect(url_for('get_post',post_id=post.id))

        return render_template('edit_post.html',form=form,post=post)

    @app.route('/admin', methods=['GET', 'POST'])
    def admin_control():
        """
        Admin control panel route. Restricted to logged-in admins.
        Displays a list of all users and allows admin to block/unblock any user from commenting.
        """

        if 'user_id' not in session:
            flash("You must be logged in to access this page.", "danger")
            return redirect(url_for('login'))

        user = User.query.get(session['user_id'])
        if not user.is_admin:
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for('home'))

        users = User.query.all()
        return render_template('admin_control.html', users=users)

    @app.route('/toggle_blacklist/<int:user_id>')
    def toggle_blacklist(user_id):
        """
        Route to toggle the blacklist status of a user.
        Restricted to logged-in admins. Redirects to the admin control panel.
        """

        if 'user_id' not in session or not User.query.get(session['user_id']).is_admin:
            flash("Unauthorized access.", "danger")
            return redirect(url_for('home'))

        user = User.query.get_or_404(user_id)
        user.is_blacklisted = not user.is_blacklisted
        db.session.commit()
        return redirect(url_for('admin_control'))

    return app


# Create an instance of the Flask application.
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


