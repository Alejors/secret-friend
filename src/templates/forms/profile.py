from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, optional, Regexp, InputRequired, Length


class ProfileForm(FlaskForm):
  name = StringField('Name', validators=[InputRequired(), Length(min=3, message="Name must be at least 3 characters long!")])
  email = StringField('Email', render_kw={'disabled': 'disabled'})
  current_password = PasswordField('Current Password', validators=[DataRequired()])
  new_password = PasswordField('New Password', validators=[optional(), Regexp(r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,12}$", message="The Password must include: 8 to 12 characters, at least 1 capital letter and at least 1 digit!")])
  
  submit = SubmitField('Update Profile')