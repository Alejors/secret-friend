from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, optional, Regexp, InputRequired, Length

from src.utils import *


class ProfileForm(FlaskForm):
  name = StringField(NAME_FIELD, validators=[InputRequired(), Length(min=NAME_LENGTH, message=NAME_FIELD_LENGTH_ERROR)])
  email = StringField(EMAIL_FIELD, render_kw={'disabled': 'disabled'})
  current_password = PasswordField('Current Password', validators=[DataRequired()])
  new_password = PasswordField('New Password', validators=[optional(), Regexp(PASSWORD_REGEX, message=PASSWORD_REQUIREMENTS)])
  repeat_password = PasswordField('Repeat New Password', validators=[optional()])
  
  def validate(self):
    if not FlaskForm.validate(self):
      return False
    if self.new_password.data and self.repeat_password.data and self.new_password.data == self.repeat_password.data:
      return True
    self.new_password.errors.append("Password and Repeat Password do not Match!")
    return False

  
  submit = SubmitField('Update Profile')