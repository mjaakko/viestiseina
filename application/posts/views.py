from application import app
from flask import render_template, request

@app.route("/posts/new/")
@login_required
def posts_form():
    return render_template("posts/new.html")

@app.route("/posts/", methods=["POST"])
@login_required
def posts_create():
    post = Post(request.form.get("name"), None)

    db.session().add(post)
    db.session().commit()
  
    return "hello world!"
