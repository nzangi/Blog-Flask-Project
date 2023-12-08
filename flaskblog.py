# save this as app.py
from flask import Flask
from flask import render_template

app = Flask(__name__)

posts = [
    {
        'author':'Nzangi',
        'title':'Blog post 1',
        'content':'First Blog Post',
        'date':'Dec 8 2023'
    },
    {
        'author':'Muoki',
        'title':'Blog post 2',
        'content':'Second Blog Post',
        'date':'Dec 7 2023'
    },
    {
        'author':'Kanee',
        'title':'Blog post 3',
        'content':'Third Blog Post',
        'date':'Dec 6 2023'
    },
    {
        'author':'Munyoki',
        'title':'Blog post 4',
        'content':'Fourth Blog Post',
        'date':'Dec 4 2023'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",posts=posts)


@app.route("/about")
def about():
    return render_template('about.html',title="About")


if __name__ == '__main__':
    app.run(debug=True)
