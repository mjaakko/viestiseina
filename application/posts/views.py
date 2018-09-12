from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.posts.models import Post
from application.posts.forms import PostForm

@app.route("/posts", methods=["GET"])
def posts_index():
    return render_template("posts/list.html", posts = Post.query.filter_by(parent_id=None).all())

@app.route("/posts/new/")
@login_required
def posts_form():
    return render_template("posts/new.html", form = PostForm())

@app.route("/posts/update/<post_id>/")
@login_required
def posts_update(post_id):
    post = Posts.query.get(post_id)

    return render_template("posts/update.html", form = PostForm(post.content), post_id = post.id)

@app.route("/posts/update/<post_id>/", methods=["POST"])
@login_required
def posts_update(post_id):
    form = PostForm(request.form)

    if not form.validate():
        return render_template("posts/update.html", form = form, post_id = post_id)

    post = Posts.query.get(post_id)
    post.content = form.content.data

    db.session().commit()

    return redirect(url_for("posts_index"))

@app.route("/posts/", methods=["POST"])
@login_required
def posts_create():
    form = PostForm(request.form)

    if not form.validate():
        return render_template("posts/new.html", form = form)

    post = Post(current_user.id, form.content.data, None)
  
    db.session().add(post)
    db.session().commit()
  
    return redirect(url_for("posts_index"))
