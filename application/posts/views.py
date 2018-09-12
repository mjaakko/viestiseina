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
