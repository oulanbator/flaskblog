from flask import Blueprint, render_template, request
from flaskblog.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # Pagination : récupérer arguments de l'URL (1 = default) : ?page=1, 2, 3, ...
    page = request.args.get('page', 1, type=int)
    # Avoir les posts dans l'ordre inverse (le dernier en premier) : order_by(Post.date_posted.desc())
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)

@main.route('/about')
def about():
    return render_template("about.html", title="About")