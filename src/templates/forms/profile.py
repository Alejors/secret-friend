from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, optional, Regexp, InputRequired, Length

from src.utils import *


class ProfileForm(FlaskForm):
  name = StringField(NAME_FIELD, validators=[InputRequired(), Length(min=NAME_LENGTH, message=NAME_FIELD_LENGTH_ERROR)])
  email = StringField(EMAIL_FIELD, render_kw={'disabled': 'disabled'})
  current_password = PasswordField('Current Password', validators=[DataRequired()])
  new_password = PasswordField('New Password', validators=[optional(), Regexp(PASSWORD_REGEX, message=PASSWORD_REQUIREMENTS)])
  
  submit = SubmitField('Update Profile')