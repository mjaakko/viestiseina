from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators

class PostForm(FlaskForm):
    content = TextAreaField("Viestin sisältö", [validators.Length(min=3)])
 
    class Meta:
        csrf = False
