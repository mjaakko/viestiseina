from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from application import app, db, requires_role
from application.auth.models import User, Role
from application.auth.forms import ChangePasswordForm, LoginForm

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

@app.route("/auth/change_password", methods = ["GET","POST"])
@login_required
def auth_password_change():
    if request.method == "GET":
    	return render_template("auth/change_password_form.html", form = ChangePasswordForm())

    form = ChangePasswordForm(request.form)
    if not form.validate():
        return render_template("auth/change_password_form.html", form = form)

    if current_user.password == form.password_current.data:
        current_user.password = form.password_new.data

        db.session.add(current_user)
        db.session.commit()

        return redirect(url_for("user_view", user_id = current_user.id))
    else:
        return render_template("auth/change_password_form.html", form = form,
                               error = "Nykyinen salasana ei ole oikein")
       
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

@app.route("/user/<user_id>/remove_mod_role")
@login_required
@requires_role("ADMIN")
def remove_mod_role(user_id):
    user = User.query.get(user_id)
    for user_role in user.roles:
        if user_role.name == "MODERATOR":
            user.roles.remove(user_role)

            db.session.add(user)
            db.session.commit() 

            break

    return redirect(url_for("user_view", user_id = user_id))

@app.route("/user/<user_id>/remove_user")
@login_required
@requires_role("ADMIN")
def remove_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("posts_index"))

@app.route("/users")
def users_index():
    users = User.query.all()
    return render_template("auth/list.html", users = users)

