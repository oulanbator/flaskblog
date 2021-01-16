from flask import Blueprint, render_template, url_for, flash, redirect, request
from flaskblog import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.users.utils import save_picture, send_reset_email
# pylint: disable=no-member

users = Blueprint('users', __name__)

# -------------------------------------------------------
# AUTHENTIFICATION

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data.lower(),
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, you are now able to log in !', 'success')
        return redirect(url_for('users.login'))
    return render_template("register.html", title="Register", form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            """
            -----------------------------------------------------------------------
            Warning: You MUST validate the value of the next parameter. 
            If you do not, your application will be vulnerable to open redirects.
            For an example implementation of is_safe_url see this Flask Snippet :
            https://web.archive.org/web/20190128010142/http://flask.pocoo.org/snippets/62/
            >> The snippet :

            from urllib.parse import urlparse, urljoin

            def is_safe_url(target):
                ref_url = urlparse(request.host_url)
                test_url = urlparse(urljoin(request.host_url, target))
                return test_url.scheme in ('http', 'https') and \
                    ref_url.netloc == test_url.netloc
                    
            >> More documentation on stack overflow
            https://stackoverflow.com/questions/60532973/how-do-i-get-a-is-safe-url-function-to-use-with-flask-and-how-does-it-work
            -----------------------------------------------------------------------

            if not is_safe_url(next_page):
                return flask.abort(400)
            """
            return redirect(next_page or url_for('main.home'))
            # return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccesfull, please check email and password !', 'danger')
    return render_template("login.html", title="Login", form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# -------------------------------------------------------
# ACCOUNT MANAGEMENT AND ACTIVITY

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    #Vérifie si le formulaire est valide
    if form.validate_on_submit():
        #change et commit les valeurs
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", 
        title="Account",
        image_file=image_file, 
        form=form)

@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)

# -------------------------------------------------------
# RESET PASSWORD

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been send with instructions to reset your password !", "info")
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", form=form, title='Reset Password')

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is invalid or expired token", "warning")
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated, you are now able to log in !', 'success')
        return redirect(url_for('users.login'))
    return render_template("reset_token.html", form=form, title='Reset Password')