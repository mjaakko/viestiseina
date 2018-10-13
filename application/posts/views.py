from application import app, db, login_manager
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required 
from application.posts.models import Post, Hashtag
from application.posts.forms import PostForm

@app.route("/posts", methods=["GET"])
def posts_index():
    return render_template("posts/list.html", posts = Post.query.filter_by(parent_id=None).order_by(Post.create_time.desc()).all(), form = PostForm(), show = False)

@app.route("/posts/", methods=["POST"])
@login_required
def posts_create():
    form = PostForm(request.form)

    if not form.validate():
        return render_template("posts/list.html", posts = Post.query.filter_by(parent_id=None).order_by(Post.create_time.desc()).all(), form = form, show = True)

    post = Post(current_user.id, form.content.data, None)
  
    db.session().add(post)
    db.session().commit()
  
    return redirect(url_for("posts_index"))

@app.route("/posts/update/<post_id>/")
@login_required
def posts_update_form(post_id):
    post = Post.query.get(post_id)

    form = PostForm()
    form.content.data = post.content

    return render_template("posts/update.html", form = form, post_id = post.id)

@app.route("/posts/update/<post_id>/", methods=["POST"])
@login_required
def posts_update(post_id):
    form = PostForm(request.form)

    if not form.validate():
        return render_template("posts/update.html", form = form, post_id = post_id)

    post = Post.query.get(post_id)
    if not (post.user_id is current_user.id or current_user.has_role("MODERATOR")):
        return login_manager.unauthorized()

    post.content = form.content.data

    db.session().commit()

    return redirect(url_for("posts_index"))

@app.route("/posts/delete/<post_id>/")
@login_required
def posts_delete(post_id):
    post = Post.query.get(post_id)
    if not (post.user_id is current_user.id or current_user.has_role("MODERATOR")):
        return login_manager.unauthorized()

    db.session.query(Post).filter(Post.id==post_id).delete()
    db.session.commit()

    return redirect(url_for("posts_index"))

@app.route("/hashtags")
def hashtags_index():
    counts = Hashtag.get_total_hashtag_counts()

    return render_template("hashtags/list.html", counts = counts)

@app.route("/hashtags/<hashtag_id>/")
def hashtag_view(hashtag_id):
    return render_template("hashtags/posts_with_hashtag.html", posts = Post.query.filter(Post.hashtags.any(id=hashtag_id)).order_by(Post.create_time.desc()).all())
