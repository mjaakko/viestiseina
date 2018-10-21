from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators

class PostForm(FlaskForm):
    content = TextAreaField("Viestin sisältö", [validators.Length(min=3)])

    class Meta:
        csrf = False

class SearchForm(FlaskForm):
    content = StringField("Viestin sisältö", [validators.required(), validators.Length(min=3)])
    user = StringField("Käyttäjä", [validators.optional(), validators.Length(min=2)])

    class Meta:
        csrf = False
