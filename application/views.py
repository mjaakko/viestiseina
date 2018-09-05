from flask import render_template
from application import app

@app.route("/")
def index():
	render_template("index.html")


