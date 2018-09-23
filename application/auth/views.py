from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(name=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "Virheellinen käyttäjätunnus tai salasana")


    print("User " + user.name + " logged in")	
    login_user(user)
    return redirect(url_for("index"))    

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))    

@app.route("/auth/register", methods = ["GET","POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", form = LoginForm())

    form = LoginForm(request.form)

    user_exists = User.query.filter_by(name=form.username.data).first()
    if user_exists:
        return render_template("auth/registerform.html", form = form,
                               error = "Valittu käyttäjänimi on jo käytössä")

    user = User(name=form.username.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()

    # Login with newly added user
    user = User.query.filter_by(name=form.username.data, password=form.password.data).first()
    login_user(user)

    return redirect(url_for("index"))    
