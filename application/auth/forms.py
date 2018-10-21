from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Käyttäjätunnus", [validators.Regexp(regex="^[a-zA-Z0-9_]*$", message="Käyttäjätunnus voi sisältää vain kirjaimia ja numeroita sekä alaviivan"), validators.Length(min=2, message="Käyttäjätunnuksen tulee olla vähintään 2 merkkiä pitkä")])
    password = PasswordField("Salasana", [validators.Regexp(regex="^[a-zA-Z0-9!@#\\-.+,/\"]*$", message="Salasana voi sisältää vain kirjaimia ja numeroita sekä joitain erikoismerkkejä"), validators.Length(min=4, message="Salasanan tulee olla vähintään 4 merkkiä pitkä")])

    class Meta:
        csrf = False

class ChangePasswordForm(FlaskForm):
    password_current = PasswordField("Nykyinen salasana", [validators.Regexp(regex="^[a-zA-Z0-9!@#\\-.+,/\"]*$", message="Salasana voi sisältää vain kirjaimia ja numeroita sekä joitain erikoismerkkejä"), validators.Length(min=4, message="Salasanan tulee olla vähintään 4 merkkiä pitkä")])
    password_new = PasswordField("Uusi salasana", [validators.Regexp(regex="^[a-zA-Z0-9!@#\\-.+,/\"]*$", message="Salasana voi sisältää vain kirjaimia ja numeroita sekä joitain erikoismerkkejä"), validators.Length(min=4, message="Salasanan tulee olla vähintään 4 merkkiä pitkä")])

    class Meta:
        csrf = False
