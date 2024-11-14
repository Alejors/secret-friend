from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ParticipantForm(FlaskForm):
  name = StringField('Nombre', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired()])