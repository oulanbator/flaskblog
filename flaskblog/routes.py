from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
# pylint: disable=no-member

posts = [
    {
        "author": "Tor",
        "title": "First post",
        "content": "Talking about my first blog",
        "date_posted": "19/12/2020"
    },
    {
        "author": "Rémi",
        "title": "Second post",
        "content": "Talking about my second blog",
        "date_posted": "20/12/2020"
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", posts=posts)

@app.route('/about')
def about():
    return render_template("about.html", title="About")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
            >> More documentation on stack overflow
            https://stackoverflow.com/questions/60532973/how-do-i-get-a-is-safe-url-function-to-use-with-flask-and-how-does-it-work
            -----------------------------------------------------------------------

            if not is_safe_url(next_page):
                return flask.abort(400)
            """
            return redirect(next_page or url_for('home'))
            # return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccesfull, please check email and password !', 'danger')
    return render_template("login.html", title="Login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template("account.html", title="Account")