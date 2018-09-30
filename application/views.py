from flask import redirect, url_for
from application import app

@app.route("/")
def index():
	return redirect(url_for("posts_index"), 301)


