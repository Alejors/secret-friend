from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, optional, Regexp


class ProfileForm(FlaskForm):
  name = StringField('Nombre', validators=[DataRequired()])
  email = StringField('Email', render_kw={'disabled': 'disabled'})
  current_password = PasswordField('Contraseña Actual', validators=[DataRequired()])
  new_password = PasswordField('Nueva Contraseña', validators=[optional(), Regexp(r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,12}$", message="La contraseña debe tener entr 8 y 12 caracteres, al menos 1 mayúscula y al menos 1 número!")])
  
  submit = SubmitField('Actualizar')