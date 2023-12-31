from flask import Blueprint
from flask import redirect, flash, render_template, url_for, request, abort
from flaskblog.models import Post
from flask_login import current_user, login_required
from flaskblog.posts.forms import PostForm
from flaskblog import db

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, post_content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your Post has been created!")
        return redirect(url_for('main.home'))

    return render_template('posts/new_post.html', title="New Post", form=form, legend="New Post")


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("posts/post.html", title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.post_content = form.content.data
        db.session.commit()
        flash("Your Post has been Updated!")
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.post_content

    return render_template('posts/new_post.html', title="Update Post", form=form, legend="Update Post")


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post account has been deleted successfully!", 'success')
    return redirect(url_for('main.home'))
