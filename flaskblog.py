from flask import Flask, render_template, url_for
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)