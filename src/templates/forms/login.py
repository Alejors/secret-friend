from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from src.utils import *

class LoginForm(FlaskForm):
  email = StringField(EMAIL_FIELD, validators=[DataRequired()])
  password = PasswordField(PASSWORD_FIELD, validators=[DataRequired()])
  
  submit = SubmitField('Log In')