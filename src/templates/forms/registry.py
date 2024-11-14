from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired


class RegistryForm(FlaskForm):
  name = StringField('Nombre', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), validators.Email()])
  password = PasswordField('Contraseña', validators=[DataRequired(), validators.Regexp(r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,12}$", message="La contraseña debe tener entr 8 y 12 caracteres, al menos 1 mayúscula y al menos 1 número!")])
  
  submit = SubmitField('Registrarse')
