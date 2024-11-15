from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp


class RegistryForm(FlaskForm):
  name = StringField('Nombre', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email(message="Email no es válido.")])
  password = PasswordField('Contraseña', validators=[DataRequired(), Regexp(r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,12}$", message="La contraseña debe tener entre 8 y 12 caracteres, al menos 1 mayúscula y al menos 1 número!")])
  
  submit = SubmitField('Registrarse')
