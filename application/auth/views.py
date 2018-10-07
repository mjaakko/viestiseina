from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

from application import app, db, requires_role
from application.auth.models import User, Role
from application.auth.forms import LoginForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    if not form.validate():
        return render_template("auth/loginform.html", form = form)


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
    if not form.validate():
        return render_template("auth/registerform.html", form = form)


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

@app.route("/user/<user_id>")
def user_view(user_id):
    user = User.query.filter_by(id = user_id).first()
    return render_template("auth/user.html", user = user)

@app.route("/user/<user_id>/give_mod_role")
@login_required
@requires_role("ADMIN")
def give_mod_role(user_id):
    user = User.query.get(user_id)
    user.roles.append(Role.query.filter_by(name="MODERATOR").first())

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("user_view", user_id = user_id))
