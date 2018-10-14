from flask import Flask, url_for
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///viestiseina.db"    
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

#
from application.auth.models import User, Role
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

# Authentication and authorization
from flask_login import LoginManager, current_user, AnonymousUserMixin
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Kirjaudu sisään ennen tämän toiminnon käyttöä"

#Anonymous user which has no roles
class Anonymous(AnonymousUserMixin):
	def has_role(self, role):
		return False

login_manager.anonymous_user = Anonymous

from functools import wraps

def requires_role(role):
	def wrapper(fn):
		@wraps(fn)
		def decorated_view(*args, **kwargs):
			if not current_user:
				return login_manager.unauthorized()
	
			if not current_user.is_authenticated():
				return login_manager.unauthorized()
	            
			authorized = current_user.has_role(role)
	
			if not authorized:
				return login_manager.unauthorized()
            
			return fn(*args, **kwargs)
		return decorated_view
	return wrapper


# 
from application import views

from application.posts import models
from application.posts import views
 
from application.auth import models 
from application.auth import views

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#Jinja filters
from datetime import datetime, tzinfo
from pytz import timezone
import pytz

helsinki_tz = timezone("Europe/Helsinki")

def format_datetime(value):
    helsinki_time = pytz.utc.localize(value, is_dst=None).astimezone(helsinki_tz)
    return helsinki_time.strftime("%d-%m-%Y %H:%M")

app.jinja_env.filters['datetime'] = format_datetime

import html

def hashtagify(post):
    def hashtagify_word(word):
        hashtag = next(filter(lambda hashtag: hashtag.name == word, post.hashtags), None)
        if hashtag is not None:
            return "<a href=\""+url_for('hashtag_view', hashtag_id = hashtag.id)+"\">"+hashtag.name+"</a>" 
        else:
            return word

    hashtagged = list(map(hashtagify_word, html.escape(post.content).split()))
    return " ".join(hashtagged)

app.jinja_env.filters['hashtagify'] = hashtagify

def pluralize(number, singular, plural):
	if number == 1:
		return str(number) + " " + singular
	else:
		return str(number) + " " + plural

app.jinja_env.filters['pluralize'] = pluralize

# Create database tables, if needed
try: 
    db.create_all()
except:
    pass

# Create roles, if needed
roles = ["USER", "MODERATOR", "ADMIN"]
for role in roles:
	role_exists = Role.query.filter_by(name=role).first()
	if not role_exists:
		db_role = Role(name=role)
		db.session.add(db_role)
		db.session.commit()

# Create demo user
exists = User.query.filter_by(name="demo").first()
if not exists:
    demo = User(name="demo", password="demo")
    db.session.add(demo)
    db.session.commit()
